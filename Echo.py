from Worker import Worker
from FIPAMessage import FIPAMessage


class Echo(Worker):
    """Worker that echoes back any request as an inform message."""

    def on_message(self, message: FIPAMessage) -> None:
        super().on_message(message)
        if message.performative == "request":
            reply = f"ack: {message.content}"
            self.send(message.sender, "inform", reply)
