import asyncio
import openai

from agents.websocket.web_actor import WebActor
from messages.fipa_message import FIPAMessage

class Supervisor(WebActor):
    async def run(self) -> None:
        await self.connect()
        while True:
            user_cmd = await asyncio.to_thread(input, "Введите команду (или 'exit'): ")
            if user_cmd.lower() == "exit":
                break
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Сформулируй короткую инструкцию выполнить команду в shell."},
                    {"role": "user", "content": user_cmd},
                ],
            )
            instruction = completion.choices[0].message["content"].strip()
            await self.send("Doer", "request", instruction)
        await asyncio.sleep(1)

    async def on_message(self, message: FIPAMessage) -> None:
        await super().on_message(message)
        if message.performative == "inform":
            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Подтверди получение и кратко опиши результат выполнения."},
                    {"role": "user", "content": message.content},
                ],
            )
            print(completion.choices[0].message["content"].strip())
