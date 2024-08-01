import discord
from discord.ext import commands


async def on_ping(bot: commands.Bot, ctx: commands.Context, *args) -> None:
    reply_message = await ctx.send("⏳ Calculating response time...")
    time_took = reply_message.created_at - ctx.message.created_at

    # Build response embed
    response_embed = discord.Embed(
        title="🏓 Ping",
        color=0xee49ff
    )
    response_embed.add_field(
        name="Response Time",
        value=f"{round(time_took.total_seconds() * 1000)}ms",
        inline=False
    )
    response_embed.add_field(
        name="API Latency",
        value=f"{round(bot.latency * 1000)}ms",
        inline=False
    )

    await reply_message.edit(content="", embed=response_embed)
