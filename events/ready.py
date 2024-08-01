from discord import Client


async def on_ready(client: Client) -> None:
    print("Logged on as", client.user)
