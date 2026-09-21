"""General-purpose commands: /ping and /about."""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from hanyu import __version__


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Check that Hànyǔ is alive.")
    async def ping(self, interaction: discord.Interaction) -> None:
        ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! {ms} ms")

    @app_commands.command(name="about", description="About Hànyǔ (汉语).")
    async def about(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title="汉语 Hànyǔ",
            description=(
                "A Mandarin learning bot: pinyin quizzes, a travel phrase module, "
                "and (soon) hanzi practice. Simplified characters only."
            ),
            colour=discord.Colour.red(),
        )
        embed.set_footer(text=f"v{__version__}")
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))