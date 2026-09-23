"""Static reference content for `/learn`.

Kept Discord-free on purpose, like `core.decks`: this module is just data, so it can be edited or
unit tested without touching `cogs/learn.py`. Pinyin here is stored numbered, same convention as
decks (`core.pinyin.to_display` renders it for display).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToneInfo:
    number: int  # 1-4, or 0 for neutral
    mark: str
    shape: str
    example_hanzi: str
    example_pinyin: str  # numbered, e.g. "ma1"
    example_meaning: str


TONES: tuple[ToneInfo, ...] = (
    ToneInfo(1, "¯", "high and flat", "妈", "ma1", "mom"),
    ToneInfo(2, "´", 'rising, like a question "huh?"', "麻", "ma2", "hemp"),
    ToneInfo(3, "ˇ", "low, dipping", "马", "ma3", "horse"),
    ToneInfo(4, "`", 'sharp fall, like a command "no!"', "骂", "ma4", "scold"),
    ToneInfo(0, "(none)", "light and short", "吗", "ma5", "question particle"),
)

# (title, body) pairs, shown as a second page.
SANDHI_RULES: tuple[tuple[str, str], ...] = (
    (
        "Two 3rd tones in a row",
        "The first becomes a 2nd tone in speech, though it's still written as 3rd.\n"
        "你好 (nǐ hǎo) is written with two 3rd tones, but said as *ní hǎo*.",
    ),
    (
        "不 (bù) before a 4th tone",
        "不 changes from bù to bú before another 4th tone.\n"
        "不要 is written bù yào, but said as *bú yào*.",
    ),
    (
        "一 (yī) changes tone depending on what follows",
        "Before a 4th tone, 一 becomes yí (一样 -> *yíyàng*).\n"
        "Before tones 1-3, it becomes yì (一天 -> *yìtiān*).\n"
        "Alone, or at the end of a number, it stays yī (第一 -> dìyī).",
    ),
)