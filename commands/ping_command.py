import discord


async def on_ping(client: discord.Client, interaction: discord.Interaction) -> None:
    pong_message = await interaction.channel.send("⏳ Calculating response time...")
    time_took = pong_message.created_at - interaction.created_at

    # Build response embed
    response_embed = discord.Embed(
        title="🏓 Ping",
        color=0x98aaff
    )
    response_embed.add_field(
        name="Response Time",
        value=f"{round(time_took.total_seconds() * 1000)}ms",
        inline=False
    )
    response_embed.add_field(
        name="API Latency",
        value=f"{round(client.latency * 1000)}ms",
        inline=False
    )

    await interaction.response.send_message(embed=response_embed)
    await pong_message.delete()
