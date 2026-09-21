# Roadmap

- [x] **Phase 0: Foundation**: bot skeleton, slash commands, config, deck format and loader, CI
- [ ] **Phase 1: Learn tab**: `/learn initials`, `/learn finals`, `/learn tones`, pinyin chart browser (paged embeds)
- [ ] **Phase 2: Pinyin quiz**: hanzi → pinyin, tone strictness levels (toneless / tones / tones + meaning), tone-only quiz, answer normalization (`ni3`, `nǐ`, `ni`, `lv`/`lü`), scoring and leaderboard
- [ ] **Phase 3: Travel module**: category decks (essentials, money, transport, food, hotel, emergencies), `/phrase` lookup
- [ ] **Phase 4: Hanzi**: radicals, hanzi → meaning, "survival signs" deck
- [ ] **Phase 5: Later**: stats + spaced repetition, listening quizzes (TTS), Anki export, role-play bot

## Design notes

- Slash commands only (no privileged message-content intent).
- Logic that doesn't need Discord lives in `hanyu.core` so it can be unit tested.
- Pinyin stored numbered, displayed with tone marks. Readings are stored per *word*, not per character (polyphones like 行 and 长).
- Simplified characters only. A separate mini-deck for Hong Kong (traditional / Cantonese) may come later.