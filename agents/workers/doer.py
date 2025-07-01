import asyncio
import openai

from agents.websocket.web_actor import WebActor
from messages.fipa_message import FIPAMessage


class Doer(WebActor):
    async def on_message(self, message: FIPAMessage) -> None:
        await super().on_message(message)
        if message.performative == "request":
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Преобразуй инструкцию пользователя в команду shell."},
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
                    {"role": "system", "content": "Опиши результат выполнения команды пользователю."},
                    {"role": "user", "content": f"Команда: {cmd}\nВывод: {output}"},
                ],
            )
            reply = completion.choices[0].message["content"].strip()
            await self.send(message.sender, "inform", reply)
