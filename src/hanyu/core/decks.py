"""Deck data model and loader.

Decks are JSON files under ``data/decks/``. Each file holds one deck::

    {
      "id": "travel-essentials",
      "name": "Travel: Essentials",
      "description": "...",
      "cards": [
        {"id": "...", "hanzi": "你好", "pinyin": "ni3 hao3", "meaning": ["hello"],
         "category": "essentials", "tags": ["hsk1", "travel"]}
      ]
    }
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class DeckError(ValueError):
    """Raised when a deck file is malformed."""


@dataclass(frozen=True)
class Card:
    id: str
    hanzi: str
    pinyin: str  # numbered, e.g. "ni3 hao3"
    meaning: tuple[str, ...]
    category: str = ""
    tags: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict, *, source: str = "?") -> Card:
        try:
            meaning = data["meaning"]
            if isinstance(meaning, str):
                meaning = [meaning]
            if not meaning:
                raise DeckError(f"{source}: card {data.get('id')!r} has no meaning")
            return cls(
                id=data["id"],
                hanzi=data["hanzi"],
                pinyin=data["pinyin"],
                meaning=tuple(meaning),
                category=data.get("category", ""),
                tags=tuple(data.get("tags", ())),
            )
        except KeyError as exc:
            raise DeckError(f"{source}: card missing field {exc}") from exc


@dataclass(frozen=True)
class Deck:
    id: str
    name: str
    description: str
    cards: tuple[Card, ...] = field(default_factory=tuple)

    @classmethod
    def from_file(cls, path: Path) -> Deck:
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise DeckError(f"{path}: invalid JSON ({exc})") from exc

        try:
            cards = tuple(Card.from_dict(c, source=str(path)) for c in raw["cards"])
            deck = cls(
                id=raw["id"], name=raw["name"], description=raw.get("description", ""), cards=cards
            )
        except KeyError as exc:
            raise DeckError(f"{path}: deck missing field {exc}") from exc

        ids = [c.id for c in deck.cards]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            raise DeckError(f"{path}: duplicate card ids {sorted(dupes)}")
        return deck


@dataclass(frozen=True)
class DeckLibrary:
    decks: dict[str, Deck]

    @classmethod
    def load(cls, root: Path) -> DeckLibrary:
        decks: dict[str, Deck] = {}
        for path in sorted(root.rglob("*.json")):
            deck = Deck.from_file(path)
            if deck.id in decks:
                raise DeckError(f"{path}: duplicate deck id {deck.id!r}")
            decks[deck.id] = deck
        return cls(decks)

    @property
    def card_count(self) -> int:
        return sum(len(d.cards) for d in self.decks.values())