import asyncio
import websockets
print("DEBUG: websockets version:", websockets.__version__, flush=True)

from buses.websocket.web_bus import WebBus
from agents.workers.supervisor import Supervisor
from agents.workers.doer import Doer


async def main() -> None:
    bus = WebBus()
    server_task = asyncio.create_task(bus.start())
    await asyncio.sleep(0.5)  # Дать серверу время подняться

    executor = Doer("Doer", "ws://localhost:8765")
    await executor.connect()

    commander = Supervisor("Supervisor", "ws://localhost:8765")
    await commander.run()

    await commander.websocket.close()
    await executor.websocket.close()
    server_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
