from discord import Message


async def on_message(message: Message) -> None:
    print(f"Message from {message.author}: {message.content}")
