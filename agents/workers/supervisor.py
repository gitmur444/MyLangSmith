import asyncio
from openai import AsyncOpenAI

from agents.websocket.web_actor import WebActor
from messages.fipa_message import FIPAMessage

client = AsyncOpenAI()

def clean_input(text: str) -> str:
    # Remove surrogate pairs and invalid unicode
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")

class Supervisor(WebActor):
    async def run(self) -> None:
        await self.connect()
        while True:
            user_cmd = await asyncio.to_thread(input, "Введите команду (или 'exit'): ")
            user_cmd = clean_input(user_cmd)
            if user_cmd.lower() == "exit":
                break
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Сформулируй короткую инструкцию выполнить команду в shell."},
                    {"role": "user", "content": user_cmd},
                ],
            )
            instruction = response.choices[0].message.content.strip()
            await self.send("Doer", "request", instruction)
        await asyncio.sleep(1)

    async def on_message(self, message: FIPAMessage) -> None:
        await super().on_message(message)
        if message.performative == "inform":
            safe_content = clean_input(message.content)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Подтверди получение и кратко опиши результат выполнения."},
                    {"role": "user", "content": safe_content},
                ],
            )
            print(response.choices[0].message.content.strip())
