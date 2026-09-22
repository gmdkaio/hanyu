"""Build HSK vocabulary decks from drkameleon/complete-hsk-vocabulary's complete.json.

Usage:
    python scripts/build_hsk_decks.py

Download the source file first (not checked into git, see DATA_SOURCES.md):

    curl -o data/sources/hsk/complete.json \\
        https://raw.githubusercontent.com/drkameleon/complete-hsk-vocabulary/main/complete.json

For each of HSK levels 1-6 (the "new-N" tags, i.e. the 2021/HSK 3.0 standard), this writes
``data/decks/hsk/hskN.json`` with one card per word.

Each entry's "forms" are grouped by pinyin *after* normalization (lowercased, ü -> v), since the
source sometimes splits one reading into several forms - e.g. 你/妳 (a traditional-character
variant) or 安's "An1" vs "an1" (capitalized only to mark a surname sense) both share one real
pronunciation. Forms that land in the same group have their meanings merged into one card.

Words are skipped, and logged instead, when either is true:

- **Genuine polyphones**: more than one *distinct* pinyin remains after grouping (e.g. 吗 as
  ma2/ma3/ma5). The source doesn't reliably order forms by frequency, so guessing the "main"
  reading risks silently teaching the wrong one. These are candidates for the Phase 4 hanzi work,
  where each reading can be entered deliberately.
- **Malformed numeric pinyin**: missing tone digits, or a syllable count that doesn't match the
  hanzi length (usually 儿-suffixed compounds where the source's numeric field is inconsistent).

Skipped words are written to ``data/sources/hsk/skipped.json`` for manual review; nothing is
silently dropped.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = REPO_ROOT / "data" / "sources" / "hsk" / "complete.json"
OUTPUT_DIR = REPO_ROOT / "data" / "decks" / "hsk"
SKIPPED_FILE = REPO_ROOT / "data" / "sources" / "hsk" / "skipped.json"

LEVELS = [1, 2, 3, 4, 5, 6]  # "new-7" (HSK 3.0's merged 7-9 band) is intentionally excluded

# One numbered pinyin syllable: initial+final letters, then a tone digit 1-5.
SYLLABLE_RE = re.compile(r"^[a-zü]+[1-5]$")


def to_stored_pinyin(numeric: str) -> str:
    """Normalize to this project's pinyin convention: lowercase, ü written as v."""
    return numeric.lower().replace("ü", "v")


def is_well_formed(stored_pinyin: str, hanzi: str) -> bool:
    syllables = stored_pinyin.split()
    if len(syllables) != len(hanzi):
        return False
    return all(SYLLABLE_RE.match(s) for s in syllables)


def build_level(entries: list[dict], level: int) -> tuple[dict, list[dict]]:
    cards = []
    skipped = []

    # Sort by frequency (lower = more common) so decks are easy to hand-trim from the bottom later.
    level_tag = f"new-{level}"
    level_entries = [e for e in entries if level_tag in e.get("level", [])]
    level_entries.sort(key=lambda e: e.get("frequency", 10**9))

    for entry in level_entries:
        hanzi = entry["simplified"]

        # Group forms by normalized pinyin: same reading, possibly split across forms.
        groups: dict[str, list[dict]] = {}
        for form in entry["forms"]:
            pinyin = to_stored_pinyin(form["transcriptions"]["numeric"])
            groups.setdefault(pinyin, []).append(form)

        if len(groups) != 1:
            skipped.append(
                {
                    "hanzi": hanzi,
                    "reason": "genuine polyphone",
                    "pinyins": sorted(groups),
                    "level": level,
                }
            )
            continue

        (pinyin, forms_in_group) = next(iter(groups.items()))
        if not is_well_formed(pinyin, hanzi):
            skipped.append(
                {
                    "hanzi": hanzi,
                    "reason": f"malformed pinyin {pinyin!r}",
                    "level": level,
                }
            )
            continue

        meanings: list[str] = []
        for form in forms_in_group:
            for m in form["meanings"]:
                if m not in meanings:
                    meanings.append(m)
        meanings = meanings or ["(no meaning given)"]

        cards.append(
            {
                "id": f"hsk{level}-{len(cards) + 1:04d}",
                "hanzi": hanzi,
                "pinyin": pinyin,
                "meaning": meanings,
                "category": "vocabulary",
                "tags": [f"hsk{level}"],
            }
        )

    deck = {
        "id": f"hsk-{level}",
        "name": f"HSK {level}",
        "description": f"HSK level {level} vocabulary (HSK 3.0 standard). Simplified characters.",
        "cards": cards,
    }
    return deck, skipped


def main() -> None:
    if not SOURCE_FILE.exists():
        msg = (
            f"Missing {SOURCE_FILE}.\n"
            "Download it first - see the module docstring or DATA_SOURCES.md."
        )
        raise SystemExit(msg)

    entries = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_skipped = []
    for level in LEVELS:
        deck, skipped = build_level(entries, level)
        out_path = OUTPUT_DIR / f"hsk{level}.json"
        out_path.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        all_skipped.extend(skipped)
        print(f"hsk{level}: {len(deck['cards'])} cards -> {out_path.relative_to(REPO_ROOT)}")

    SKIPPED_FILE.write_text(
        json.dumps(all_skipped, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"skipped: {len(all_skipped)} words -> {SKIPPED_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()