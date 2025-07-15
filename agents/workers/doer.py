import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from agents.base.async_fipa_agent import AsyncFIPAAgent
from messages.fipa_message import FIPAMessage

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def clean_input(text: str) -> str:
    # Remove surrogate pairs and invalid unicode
    return text.encode("utf-8", "ignore").decode("utf-8", "ignore")

class Doer(AsyncFIPAAgent):
    async def on_message(self, message: FIPAMessage) -> None:
        try:
            print("\033[1mSupervisor --> Doer:\033[0m", message, flush=True)
            if message.performative == "request":
                safe_content = clean_input(message.content)
                response = await llm.ainvoke([
                    SystemMessage(
                        content=(
                            "Convert the user's instruction into a shell command. "
                            "Respond only with the command, without any explanation, "
                            "in the same language as the instruction."
                        )
                    ),
                    HumanMessage(content=safe_content)
                ])
                cmd = response.content.strip()
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.STDOUT,
                )
                out, _ = await proc.communicate()
                output = out.decode().strip()

                await self.send(
                    message.sender,
                    "inform",
                    output
                )
                
        except Exception as e:
            print(f"[Doer][ERROR] {e}", flush=True)
            import traceback; traceback.print_exc()
