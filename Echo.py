from Actor import Actor
from Signal import Signal


class Echo(Actor):
    """Actor that echoes back any request as an inform message."""

    def on_message(self, message: Signal) -> None:
        super().on_message(message)
        if message.performative == "request":
            reply = f"ack: {message.content}"
            self.send(message.sender, "inform", reply)
