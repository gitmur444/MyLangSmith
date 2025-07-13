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
        try:
            print(f"[Doer] Получено сообщение: {message}", flush=True)
            print(f"\033[1mDoer --> You:\033[0m {message.content}", flush=True)
            if message.performative == "request":
                safe_content = clean_input(message.content)
                print(f"[Doer] safe_content: {safe_content}", flush=True)
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Convert the user's instruction into a shell command. Respond only with the command, without any explanation, in the same language as the instruction."},
                        {"role": "user", "content": safe_content},
                    ],
                )
                cmd = response.choices[0].message.content.strip()
                print(f"[Doer] Сгенерирована команда: {cmd}", flush=True)
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                )
                out, _ = await proc.communicate()
                output = out.decode().strip()
                print(f"[Doer] Вывод команды: {output}", flush=True)
                response = await client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Describe the result of the shell command execution to the user in the same language as the original instruction."},
                        {"role": "user", "content": f"Команда: {cmd}\nВывод: {output}"},
                    ],
                )
                reply = response.choices[0].message.content.strip()
                print(f"[Doer] Ответ для Supervisor: {reply}", flush=True)
                await self.send(message.sender, "inform", reply)  # язык результата определяется Supervisor, исходный язык передаётся в сообщении или определяется по содержимому
                print(f"[Doer] Ответ отправлен Supervisor-у", flush=True)
        except Exception as e:
            print(f"[Doer][ERROR] {e}", flush=True)
            import traceback; traceback.print_exc()
