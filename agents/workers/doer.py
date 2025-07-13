import asyncio
from openai import AsyncOpenAI

from agents.base.async_fipa_agent import AsyncFIPAAgent
from messages.fipa_message import FIPAMessage

client = AsyncOpenAI()

def clean_input(text: str) -> str:
    # Remove surrogate pairs and invalid unicode
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")

class Doer(AsyncFIPAAgent):
    async def on_message(self, message: FIPAMessage) -> None:
        print(
            f"{self.name} received {message.performative} from {message.sender}: {message.content}",
            flush=True,
        )
        if message.performative == "request":
            safe_content = clean_input(message.content)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Преобразуй инструкцию пользователя в команду shell."},
                    {"role": "user", "content": safe_content},
                ],
            )
            cmd = response.choices[0].message.content.strip()
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
            )
            out, _ = await proc.communicate()
            output = out.decode().strip()
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Опиши результат выполнения команды пользователю."},
                    {"role": "user", "content": f"Команда: {cmd}\nВывод: {output}"},
                ],
            )
            reply = response.choices[0].message.content.strip()
            await self.send(message.sender, "inform", reply)

