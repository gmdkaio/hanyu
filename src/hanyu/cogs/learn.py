"""The `/learn` command: paginated reference embeds (tones, and later initials/finals/chart)."""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from hanyu.core.pinyin import clamp_page, to_display
from hanyu.core.pinyin_reference import INITIAL_GROUPS, SANDHI_RULES, TONES


def _tones_table_embed() -> discord.Embed:
    embed = discord.Embed(
        title="The four tones (+ neutral)",
        description=(
            "Mandarin syllables carry a pitch contour called a *tone*. Two words can be spelled "
            "with the exact same letters and mean something completely different depending on "
            "the tone, so getting it right matters just as much as getting the sounds right."
        ),
        colour=discord.Colour.red(),
    )
    for tone in TONES:
        label = f"Tone {tone.number}" if tone.number else "Neutral tone"
        example = to_display(tone.example_pinyin)
        embed.add_field(
            name=f"{label}  {tone.mark}",
            value=(f"{tone.shape}\n**{tone.example_hanzi}** ({example}) - {tone.example_meaning}"),
            inline=False,
        )
    return embed


def _sandhi_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Tone changes (tone sandhi)",
        description=(
            "A few tones shift in actual speech depending on what follows, even though you "
            "still write the base tone on the page."
        ),
        colour=discord.Colour.red(),
    )
    for title, body in SANDHI_RULES:
        embed.add_field(name=title, value=body, inline=False)
    return embed


def _initials_embeds() -> list[discord.Embed]:
    embeds = []
    for group in INITIAL_GROUPS:
        embed = discord.Embed(
            title=group.title, description=group.note, colour=discord.Colour.red()
        )
        for ex in group.examples:
            example = to_display(ex.example_pinyin)
            embed.add_field(
                name=ex.letter,
                value=f"**{ex.example_hanzi}** ({example}) - {ex.example_meaning}",
                inline=True,
            )
        embeds.append(embed)
    return embeds


TOPIC_BUILDERS = {
    "tones": lambda: [_tones_table_embed(), _sandhi_embed()],
    "initials": _initials_embeds,
}


class LearnPager(discord.ui.View):
    """Prev/Next pagination. Only the person who ran the command can page through it."""

    def __init__(self, pages: list[discord.Embed], author_id: int) -> None:
        super().__init__(timeout=180)
        self.pages = pages
        self.author_id = author_id
        self.index = 0
        self._stamp_footer()
        self._sync_buttons()

    def _stamp_footer(self) -> None:
        self.pages[self.index].set_footer(text=f"Page {self.index + 1} / {len(self.pages)}")

    def _sync_buttons(self) -> None:
        self.previous_button.disabled = self.index == 0
        self.next_button.disabled = self.index == len(self.pages) - 1

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "Run `/learn` yourself to page through this independently.", ephemeral=True
            )
            return False
        return True

    async def _go(self, interaction: discord.Interaction, delta: int) -> None:
        self.index = clamp_page(self.index + delta, len(self.pages))
        self._stamp_footer()
        self._sync_buttons()
        await interaction.response.edit_message(embed=self.pages[self.index], view=self)

    @discord.ui.button(label="◀ Prev", style=discord.ButtonStyle.secondary)
    async def previous_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self._go(interaction, -1)

    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.secondary)
    async def next_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        await self._go(interaction, 1)

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True


class Learn(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="learn", description="Learn pinyin basics.")
    @app_commands.choices(
        topic=[app_commands.Choice(name=name, value=name) for name in TOPIC_BUILDERS]
    )
    async def learn(self, interaction: discord.Interaction, topic: str) -> None:
        pages = TOPIC_BUILDERS[topic]()
        view = LearnPager(pages, author_id=interaction.user.id)
        await interaction.response.send_message(embed=pages[0], view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Learn(bot))