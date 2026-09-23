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


@dataclass(frozen=True)
class InitialExample:
    letter: str
    example_hanzi: str
    example_pinyin: str  # numbered, e.g. "ba4"
    example_meaning: str


@dataclass(frozen=True)
class InitialGroup:
    title: str
    note: str
    examples: tuple[InitialExample, ...]


INITIAL_GROUPS: tuple[InitialGroup, ...] = (
    InitialGroup(
        title="Aspiration pairs: b/p, d/t, g/k",
        note=(
            "Each pair is made in the same place in the mouth. The first letter comes out with "
            "no puff of air, the second comes out with a strong puff, like the difference "
            "between the English 'spy' and 'pie'."
        ),
        examples=(
            InitialExample("b", "爸", "ba4", "dad"),
            InitialExample("p", "怕", "pa4", "afraid"),
            InitialExample("d", "大", "da4", "big"),
            InitialExample("t", "他", "ta1", "he"),
            InitialExample("g", "高", "gao1", "tall"),
            InitialExample("k", "看", "kan4", "look"),
        ),
    ),
    InitialGroup(
        title="j / q / x",
        note=(
            "Made with the tongue flat and pushed toward the front teeth. Roughly: j is like "
            "the 'j' in 'jeep', q is close to 'ch', and x is close to 'sh'."
        ),
        examples=(
            InitialExample("j", "家", "jia1", "home"),
            InitialExample("q", "七", "qi1", "seven"),
            InitialExample("x", "谢", "xie4", "thank"),
        ),
    ),
    InitialGroup(
        title="zh / ch / sh / r (retroflex)",
        note=(
            "Made with the tongue curled back toward the roof of the mouth. These are the "
            "same four sounds as z/c/s/(no r) below, just said with the tongue further back."
        ),
        examples=(
            InitialExample("zh", "中", "zhong1", "middle, China"),
            InitialExample("ch", "吃", "chi1", "eat"),
            InitialExample("sh", "是", "shi4", "to be"),
            InitialExample("r", "人", "ren2", "person"),
        ),
    ),
    InitialGroup(
        title="z / c / s",
        note=(
            "Made with the tongue flat behind the front teeth. z sounds close to the 'ds' in "
            "'kids', c sounds close to the 'ts' in 'cats'."
        ),
        examples=(
            InitialExample("z", "在", "zai4", "at"),
            InitialExample("c", "菜", "cai4", "dish, vegetable"),
            InitialExample("s", "三", "san1", "three"),
        ),
    ),
)


@dataclass(frozen=True)
class FinalExample:
    letter: str
    example_hanzi: str
    example_pinyin: str  # numbered, e.g. "nv3"
    example_meaning: str


@dataclass(frozen=True)
class FinalGroup:
    title: str
    note: str
    examples: tuple[FinalExample, ...]


FINAL_GROUPS: tuple[FinalGroup, ...] = (
    FinalGroup(
        title="ü - the rounded-lip vowel",
        note=(
            "Say 'ee', then round your lips like you're about to whistle, without moving your "
            "tongue. After j, q, x or y it's written as plain u, but still said as ü - qu is "
            "said 'qü', not 'koo'."
        ),
        examples=(
            FinalExample("ü", "女", "nv3", "woman"),
            FinalExample("u (after q)", "去", "qu4", "to go"),
            FinalExample("u (after y)", "雨", "yu3", "rain"),
        ),
    ),
    FinalGroup(
        title="The buzzed i",
        note=(
            "After zh, ch, sh, r, z, c or s, the letter i isn't the vowel 'ee' at all - it's a "
            "short buzz made with the same tongue position as the consonant before it."
        ),
        examples=(
            FinalExample("shi", "十", "shi2", "ten"),
            FinalExample("zi", "子", "zi3", "child, particle"),
            FinalExample("ci", "词", "ci2", "word"),
            FinalExample("ri", "日", "ri4", "day, sun"),
        ),
    ),
    FinalGroup(
        title="-ian sounds like 'yen'",
        note="The reflex is to say 'ee-an', but -ian is said closer to the English 'yen'.",
        examples=(
            FinalExample("tian", "天", "tian1", "sky, day"),
            FinalExample("jian", "见", "jian4", "to see"),
            FinalExample("dian", "点", "dian3", "dot, o'clock"),
        ),
    ),
    FinalGroup(
        title="Hidden vowels: ui, iu, un",
        note=(
            "These three are shortened spellings that hide a vowel in the middle: ui is really "
            "uei, iu is really iou, and un is really uen. Say the full three-letter version and "
            "the pronunciation falls out naturally."
        ),
        examples=(
            FinalExample("dui (= duei)", "对", "dui4", "correct"),
            FinalExample("liu (= liou)", "六", "liu4", "six"),
            FinalExample("chun (= chuen)", "春", "chun1", "spring"),
        ),
    ),
)