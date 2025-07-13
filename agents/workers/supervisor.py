import asyncio
import json
import re

from openai import AsyncOpenAI
from agents.base.async_fipa_agent import AsyncFIPAAgent
from messages.fipa_message import FIPAMessage

client = AsyncOpenAI()

def clean_input(text: str) -> str:
    # Remove surrogate pairs and invalid unicode
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")

class Supervisor(AsyncFIPAAgent):
    async def run(self) -> None:
        while True:
            user_cmd = await asyncio.to_thread(input, "\033[1mYou --> Supervisor:\033[0m ")
            user_cmd = clean_input(user_cmd)
            if user_cmd.lower() == "exit":
                break
            # 1. Декомпозиция и оценка необходимости shell-команд
            decomposition_messages = [
                {"role": "system", "content": "Ты — AI-ассистент. Получив запрос пользователя, декомпозируй его на подзадачи и оцени, требуется ли выполнение shell-команд для решения. Ответь строго в формате:\nNEEDS_SHELL: yes/no\nDECOMPOSITION: <коротко по пунктам на русском>"},
                {"role": "user", "content": user_cmd},
            ]
            print(f"\033[1mYou --> Supervisor:\033[0m {user_cmd}", flush=True)
            print("\033[1mSupervisor --> OpenAI:\033[0m", json.dumps(decomposition_messages, ensure_ascii=False, indent=2), flush=True)
            decomposition_response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=decomposition_messages,
            )
            ai_analysis = decomposition_response.choices[0].message.content.strip()
            print(f"\033[1mOpenAI --> Supervisor:\033[0m {ai_analysis}", flush=True)

            # Фикс: ищем NEEDS_SHELL: yes даже если есть переносы, пробелы, табы
            match = re.search(r'needs_shell\s*:\s*yes', ai_analysis, re.IGNORECASE | re.DOTALL)
            print(f"[DEBUG] ai_analysis: {repr(ai_analysis)}", flush=True)
            print(f"[DEBUG] match: {match.group(0) if match else None}", flush=True)
            if match:
                # 2. Формулировка поручения Doer-у человеческим языком
                doer_messages = [
                    {"role": "system", "content": "Ты — Supervisor, взаимодействуешь с агентом-исполнителем. На основе запроса пользователя, сформулируй вежливую и понятную просьбу к другому агенту (Doer) выполнить нужные действия в shell. Не пиши команду, а только просьбу на русском."},
                    {"role": "user", "content": user_cmd},
                ]
                print("\033[1mSupervisor --> OpenAI:\033[0m", json.dumps(doer_messages, ensure_ascii=False, indent=2), flush=True)
                doer_response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=doer_messages,
                )
                doer_instruction = doer_response.choices[0].message.content.strip()
                print(f"\033[1mOpenAI --> Supervisor:\033[0m {doer_instruction}", flush=True)
                await self.send("Doer", "request", doer_instruction)
            else:
                print("\033[1mSupervisor --> You:\033[0m Для выполнения этого запроса shell-команды не требуются.", flush=True)
        await asyncio.sleep(1)

    async def on_message(self, message: FIPAMessage) -> None:
        print(
            f"{self.name} received {message.performative} from {message.sender}: {message.content}",
            flush=True,
        )
        if message.performative == "inform":
            safe_content = clean_input(message.content)
            messages = [
                {"role": "system", "content": "Подтверди получение и кратко опиши результат выполнения."},
                {"role": "user", "content": safe_content},
            ]
            print("[OpenAI request]", json.dumps(messages, ensure_ascii=False, indent=2), flush=True)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            print(response.choices[0].message.content.strip())
