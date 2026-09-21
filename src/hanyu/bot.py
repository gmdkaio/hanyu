"""Bot entry point: builds the client, loads cogs and decks, syncs slash commands."""

from __future__ import annotations

import logging

import discord
from discord.ext import commands

from hanyu.config import Settings
from hanyu.core.decks import DeckLibrary

log = logging.getLogger("hanyu")

EXTENSIONS = ("hanyu.cogs.general",)


class HanyuBot(commands.Bot):
    def __init__(self, settings: Settings) -> None:
        # Slash commands only, so no privileged message-content intent is needed.
        super().__init__(command_prefix=commands.when_mentioned, intents=discord.Intents.default())
        self.settings = settings
        self.decks = DeckLibrary.load(settings.decks_dir)

    async def setup_hook(self) -> None:
        for ext in EXTENSIONS:
            await self.load_extension(ext)

        if self.settings.dev_guild_id:
            guild = discord.Object(id=self.settings.dev_guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            log.info("Synced %d commands to dev guild %s", len(synced), guild.id)
        else:
            synced = await self.tree.sync()
            log.info("Synced %d global commands", len(synced))

    async def on_ready(self) -> None:
        log.info(
            "Logged in as %s (%d decks, %d cards)",
            self.user,
            len(self.decks.decks),
            self.decks.card_count,
        )


def run() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    settings = Settings.from_env()
    HanyuBot(settings).run(settings.token, log_handler=None)