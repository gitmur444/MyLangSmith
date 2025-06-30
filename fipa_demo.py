from Bus import Bus
from Echo import Echo


def main() -> None:
    bus = Bus()
    alice = Echo("Alice", bus)
    bob = Echo("Bob", bus)

    alice.send("Bob", "request", "Hello Bob")
    bob.send("Alice", "request", "Hello Alice")


