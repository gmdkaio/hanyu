"""Pinyin helpers.

Storage convention: pinyin is stored with tone *numbers* (``ni3 hao3``), neutral tone as ``5`` or
no digit, and ü written as ``v`` (``lv4``). Tone marks are generated only for display.

Answer normalization for quizzes (accepting ``nǐhǎo``, ``ni3hao3``, ``nihao``...) arrives in
Phase 2 and will live here too.
"""

from __future__ import annotations

from pypinyin.contrib.tone_convert import to_tone


def to_display(numbered: str) -> str:
    """Convert numbered pinyin to tone-marked pinyin: ``"ni3 hao3"`` -> ``"nǐ hǎo"``."""
    return " ".join(to_tone(syllable) for syllable in numbered.split())