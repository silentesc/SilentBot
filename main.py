from discord import Client, Message, Intents
import dotenv
import os


class MyClient(Client):
    async def on_ready(self):
        print("Logged on as", self.user)
    
    async def on_message(self, message: Message):
        print(f"Message from {message.author}: {message.content}")


intents = Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

dotenv.load_dotenv()

client.run(os.getenv("TOKEN"))
