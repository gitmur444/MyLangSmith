from fipa_acl import FIPAAgent, MessageBus


class EchoAgent(FIPAAgent):
    """Agent that echoes back any request as an inform message."""

    def on_message(self, message):
        super().on_message(message)
        if message.performative == "request":
            reply = f"ack: {message.content}"
            self.send(message.sender, "inform", reply)


def main() -> None:
    bus = MessageBus()
    alice = EchoAgent("Alice", bus)
    bob = EchoAgent("Bob", bus)

    alice.send("Bob", "request", "Hello Bob")
    bob.send("Alice", "request", "Hello Alice")


if __name__ == "__main__":
    main()
