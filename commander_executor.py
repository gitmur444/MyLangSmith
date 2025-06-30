import asyncio
import openai

from websocket_bus import WebSocketMessageBus
from websocket_agent import WebSocketFIPAAgent
from fipa_acl import FIPAMessage


class CommanderAgent(WebSocketFIPAAgent):
    async def run(self) -> None:
        await self.connect()
        while True:
            user_cmd = await asyncio.to_thread(
                input, "Введите команду (или 'exit'): "
            )
            if user_cmd.lower() == "exit":
                break
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Сформулируй короткую инструкцию выполнить команду в shell."
                        ),
                    },
                    {"role": "user", "content": user_cmd},
                ],
            )
            instruction = completion.choices[0].message["content"].strip()
            await self.send("Executor", "request", instruction)
        await asyncio.sleep(1)

    async def on_message(self, message: FIPAMessage) -> None:
        await super().on_message(message)
        if message.performative == "inform":
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Подтверди получение и кратко опиши результат выполнения."
                        ),
                    },
                    {"role": "user", "content": message.content},
                ],
            )
            print(completion.choices[0].message["content"].strip())


class ExecutorAgent(WebSocketFIPAAgent):
    async def on_message(self, message: FIPAMessage) -> None:
        await super().on_message(message)
        if message.performative == "request":
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Преобразуй инструкцию пользователя в команду shell.",
                    },
                    {"role": "user", "content": message.content},
                ],
            )
            cmd = completion.choices[0].message["content"].strip()
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            out, _ = await proc.communicate()
            output = out.decode().strip()
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Опиши результат выполнения команды пользователю.",
                    },
                    {
                        "role": "user",
                        "content": f"Команда: {cmd}\nВывод: {output}",
                    },
                ],
            )
            reply = completion.choices[0].message["content"].strip()
            await self.send(message.sender, "inform", reply)


async def main() -> None:
    bus = WebSocketMessageBus()
    server_task = asyncio.create_task(bus.start())

    executor = ExecutorAgent("Executor", "ws://localhost:8765")
    await executor.connect()

    commander = CommanderAgent("Commander", "ws://localhost:8765")
    await commander.run()

    await commander.websocket.close()
    await executor.websocket.close()
    server_task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
