from discord import Client, Message, Intents

from data.env import Env
import events
import events.message
import events.ready


class Bot:
    def __init__(self, env: Env) -> None:
        self.env = env
        self.intents = Intents.default()
        self.intents.message_content = True
        self.client = Client(intents=self.intents)

        """
        Register event handlers
        """

        @self.client.event
        async def on_ready() -> None:
            await events.ready.on_ready(self.client)

        @self.client.event
        async def on_message(message: Message) -> None:
            await events.message.on_message(message)


    def run(self):
        self.client.run(self.env.get_token())
