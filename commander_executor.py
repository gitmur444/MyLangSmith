import asyncio

from WebBus import WebBus
from Chief import Chief
from Doer import Doer


async def main() -> None:
    bus = WebBus()
    server_task = asyncio.create_task(bus.start())

    executor = Doer("Doer", "ws://localhost:8765")
    await executor.connect()

    commander = Chief("Chief", "ws://localhost:8765")
    await commander.run()

    await commander.websocket.close()
    await executor.websocket.close()
    server_task.cancel()
