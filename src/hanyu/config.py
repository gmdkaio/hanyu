"""Runtime configuration, loaded from environment variables (and a .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    token: str
    dev_guild_id: int | None
    decks_dir: Path

    @classmethod
    def from_env(cls) -> Settings:
        load_dotenv()
        token = os.environ.get("DISCORD_TOKEN", "").strip()
        if not token:
            raise RuntimeError(
                "DISCORD_TOKEN is not set. Copy .env.example to .env and add your bot token."
            )
        guild = os.environ.get("DEV_GUILD_ID", "").strip()
        decks = os.environ.get("DECKS_DIR", "").strip()
        return cls(
            token=token,
            dev_guild_id=int(guild) if guild else None,
            decks_dir=Path(decks) if decks else REPO_ROOT / "data" / "decks",
        )