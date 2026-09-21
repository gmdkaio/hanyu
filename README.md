# 汉语 Hànyǔ

A Discord bot for learning **Mandarin Chinese**: pinyin quizzes, a travel phrase module, and hanzi
practice. Inspired by [Kotoba](https://github.com/mistval/kotoba) for Japanese. **Simplified
characters only** (mainland China).

> *汉语 (hànyǔ)* means "the Chinese language".

**Status:** early development (Phase 0: foundation). See the [roadmap](docs/ROADMAP.md).

## Planned features

- **Learn tab**: initials, finals, tones, and a pinyin chart
- **Pinyin quiz**: hanzi → pinyin with adjustable tone strictness, plus a tone-only quiz
- **Travel module**: decks for essentials, money, transport, food, hotel, emergencies
- **Hanzi**: radicals, meaning quizzes, "survival signs"
- **Later**: per-user stats and spaced repetition, listening quizzes, Anki export

## Deck format

Pinyin is stored with **tone numbers** (`ni3 hao3`, neutral tone `5`, ü as `v`) and converted to
tone marks only for display. Meanings are a list so a quiz can accept several answers.

```json
{"id": "ess-0005", "hanzi": "多少钱", "pinyin": "duo1 shao5 qian2",
 "meaning": ["how much", "how much is it"], "category": "money", "tags": ["hsk1", "travel"]}
```
