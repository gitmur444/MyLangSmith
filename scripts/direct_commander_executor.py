import asyncio

from buses.base.fipa_message_bus import FipaMessageBus
from agents.workers.supervisor import Supervisor
from agents.workers.doer import Doer


async def main() -> None:
    bus = FipaMessageBus()
    doer = Doer("Doer", bus)
    supervisor = Supervisor("Supervisor", bus)
    await supervisor.run()


if __name__ == "__main__":
    asyncio.run(main())
