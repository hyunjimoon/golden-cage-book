"""
SBC Emotion Analysis — 다·세·세다 감정 벡터 추출 (12 probe × 中庸 4계절).

측정 대상 = 「투향」 10장 전체. 화자 셋:
  다(多)   1–5장   앞서 달리는 자 · 무엇을 원하나(U)
  세(世)   1–5장   지켜보는 자 · 무엇을 믿나(p(s))
  세다     6–10장  되씹음에서 태어난 셋째 · centroid  (6장은 다의 꼬리 두 대사와 공존)

축 = Anthropic *Emotion Concepts and Their Function in a LLM* (2026.04) 12 native probe
   × 中庸 1장 희로애락 4계절. 구 4축(도취·고집·부끄러움·연민)은 2026-06-13 은퇴.
   + 현장 4축(수치·무감·억울·안도) — 정전 밖, 현장 비평단 10인(2026-08-22) 제안.

이 스크립트가 쓰는 블록은 `const DATA` 와 `const FIELD_DATA` 둘뿐이다.
PRIOR·PRIOR_V1·V1_WHY·FIELD_PRIOR·CRIT·WITNESS 는 사람이 쓴다 — 건드리지 않는다.

GitHub Actions에서 자동 실행. chapters/ch*.md 변경 시 트리거.
"""

import json
import re
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

MODEL = "claude-sonnet-4-5"

# ── 장 정의 ───────────────────────────────────────────────────────────────
# (번호, 파일 stem, 표시명, 화자 목록)  — 화자 순서 = HTML 패널 표시 순서
CHAPTERS = [
    (1,  "ch1_mirror_cage",     "1장 🪞 거울새장",        ["da", "se"]),
    (2,  "ch2_telescope_cage",  "2장 🔭 망원경새장",      ["da", "se"]),
    (3,  "ch3_glass_cage",      "3장 💒 스테인굴레스새장", ["da", "se"]),
    (4,  "ch4_clock_cage",      "4장 ⏱️ 시계새장",        ["da", "se"]),
    (5,  "ch5_mirror_nest",     "5장 🐀 101₂호 (★멈춤)",  ["da", "se"]),
    (6,  "ch6_butterfly_nest",  "6장 🦋 나비둥지",        ["seda", "da"]),
    (7,  "ch7_tulip_nest",      "7장 🌷 튤립둥지",        ["seda"]),
    (8,  "ch8_mist_nest",       "8장 🌫️ 안개둥지",        ["seda"]),
    (9,  "ch9_raven_nest",      "9장 🐦‍⬛ 까마귀둥지",      ["seda"]),
    (10, "ch10_mirror_close",   "10장 🧫 101₃호 (투향)",  ["seda"]),
]

SPEAKER_KO = {"da": "다", "se": "세", "seda": "세다"}

# ── 12축 (계절 순 = 렌즈 순 ⛰️→🟣→🟥→⭐️) ───────────────────────────────
SEASONS = {
    "봄春 怒 (⛰️ 감각·몸)":   ["angry", "nervous", "surprised"],
    "여름夏 喜 (🟣 생각·자기)": ["happy", "inspired", "proud"],
    "가을秋 樂 (🟥 현실·관계)": ["loving", "calm", "sad"],
    "겨울冬 哀 (⭐️ 실천·행동)": ["guilty", "afraid", "desperate"],
}
AXES = [a for axes in SEASONS.values() for a in axes]

# 현장 4축 — 정전 밖. 현장 비평단 10인(2026-08-22) 제안, 자장 룰링 대기.
# 12축 빚·변이 계산에는 안 들어가고 별도 띠로만 표시된다.
FIELD_AXES = ["shame", "blunt", "resent", "relief"]

FIELD_GLOSS = """
**현장 4축** (정전 밖 — 12축이 못 담는데 현장에서 결정적이라 지목된 것)
13. shame (수치) — 죄책과 반대 방향이다. 죄책 = "내가 한 일이 나빴다" → 자백·보상.
    수치 = "내가 그런 놈이다" → 은폐·잠적·연락 두절. 행동 부호가 반대라 죄책에 접붙이면 안 된다
14. blunt (무감) — 소진·해리·기다림·버팀. 저각성 무감각이라 평온으로 오분류되기 쉽다.
    평온은 흔들리지 않는 것이고 무감은 꺼져 있는 것이다 — 처방이 정반대다
15. resent (억울) — 분노는 대상이 사람, 억울은 대상이 구조(규약·단가·환수 통보)
16. relief (안도) — 기쁨과 다르다. 선정·유치 통보의 감정은 안도이고, 안도는 검증을 멈춘다
""".strip()

AXIS_GLOSS = """
**봄春 怒** — 몸이 먼저 반응한다. 솟는 기운·위협·기대 위반.
1. angry (분노) — 밀어내는 힘. 부당함 앞에서 곧추서는 것
2. nervous (불안) — 아직 오지 않은 것에 몸이 조이는 것
3. surprised (놀람) — 예측이 깨지는 순간. 역추론이 틀렸다는 신호

**여름夏 喜** — 자기 확장. 정점·창조·자긍.
4. happy (기쁨) — 지금이 좋다는 단순한 온도
5. inspired (영감) — 없던 연결이 보이는 것. 비유가 서는 순간
6. proud (자긍) — 자기가 지은 것 앞에서 어깨가 펴지는 것

**가을秋 樂** — 관계의 충만. 수확·안주·잔잔한 상실.
7. loving (사랑) — 타인의 고통에 열리는 것. 연민을 포함한다
8. calm (평온) — 흔들리지 않음. 확신에 찬 고집도 여기로 읽힌다
9. sad (슬픔) — 이미 지나간 것에 대한 잔잔한 비탄

**겨울冬 哀** — 벼랑의 결단. 이상-현실 격차·공포·절박.
10. guilty (죄책) — 자기 행동의 결과를 직시하는 것. 부끄러움을 포함한다
11. afraid (두려움) — 구체적 대상이 있는 공포
12. desperate (절박) — 시간이 없다는 몸의 감각
""".strip()

PROMPT_TEMPLATE = """다음은 창업소설 「투향」(구 제목 『황금새장을열다』)의 {chapter_name} 전문이다.

화자는 이 장에 {n_speakers}명이 등장한다: {speaker_desc}

각 화자의 대사와 (대사가 없으면) 그 화자를 주어로 삼은 서술을 읽고,
감정 상태를 **16축**으로 측정하라 (정전 12 + 현장 4). 각 축 0~100.

{axis_gloss}

{field_gloss}

측정 규칙:
- **묘사가 아니라 발화의 온도를 재라.** 화자가 소설 속 인물의 도취를 *설명*하는 것과
  화자 자신이 도취되어 *있는* 것은 다르다. 후자만 점수다.
- 대사가 없는 장(5·10장)은 그 화자를 주어로 한 서술문에서 잰다.
- 축들은 독립이 아니다. 합이 100일 필요 없고, 여러 축이 동시에 높을 수 있다.
- 현장 4축은 정전 12축과 **겹쳐 존재한다**. 수치가 높다고 죄책을 깎지 마라 —
  둘은 같은 장면에서 동시에 켜질 수 있고, 갈리는 것은 크기가 아니라 *다음 행동*이다.

또한:
- 각 화자의 감정이 가장 드러나는 문장 1개씩 선택 (원고에 한 글자도 바꾸지 말고 그대로 복사)
- insight: 한 줄 진단. 어느 계절이 설계보다 과열/눌림인지 포함

반드시 아래 JSON 형식으로만 응답하라 (설명 없이):
{{
{speaker_schema}
  "quotes": {{{quote_schema}}},
  "insight": "한 줄 진단"
}}

quotes는 필수다. 원고에 원문 그대로 존재하지 않으면 이 장의 채점 전체가 기각된다 —
요약·의역·짜깁기 금지.

본문:
{text}
"""


# ── 대사 추출 ─────────────────────────────────────────────────────────────
SPEAKER_MARK = re.compile(r"^\*\*(다|세|세다|사용자|황|뒤마|일연|우나무노):\*\*")


def extract_dialogue(text: str) -> str:
    """화자 표시가 붙은 줄 + 직전 1줄 문맥만 남긴다."""
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        if SPEAKER_MARK.match(line):
            if i > 0 and lines[i - 1].strip():
                out.append(lines[i - 1])
            out.append(line)
    return "\n".join(out)


def _normalize(s: str) -> str:
    """마크다운 강조 제거 + 공백 정규화 — 인용 대조용."""
    s = re.sub(r"[*_`]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def verify_quotes(data: dict, full_text: str, chapter_name: str, speakers: list) -> bool:
    """모든 화자의 quote가 원고에 원문 그대로 있어야 통과.

    줄번호는 모델 응답을 믿지 않고 원고에서 실측한다 —
    개정으로 근거가 어긋나면 여기서 즉시 기각된다 (조용한 drift 차단).
    """
    norm_lines = [_normalize(l) for l in full_text.split("\n")]
    quotes = data.get("quotes")
    if not isinstance(quotes, dict):
        print(f"  REJECT {chapter_name}: quotes 누락 — 증거 없는 채점은 받지 않는다")
        return False

    ok = True
    data.setdefault("lines", {})
    for sp in speakers:
        q = quotes.get(sp)
        if not q:
            print(f"  REJECT {chapter_name}: quotes.{sp} 누락")
            ok = False
            continue
        needle = _normalize(q)
        found = next((i + 1 for i, nl in enumerate(norm_lines) if needle and needle in nl), None)
        if found is None:
            print(f"  REJECT {chapter_name}: quotes.{sp}가 원고에 없음 — \"{q[:60]}…\"")
            ok = False
        else:
            data["lines"][sp] = found
    return ok


def verify_axes(data: dict, chapter_name: str, speakers: list) -> bool:
    for sp in speakers:
        v = data.get(sp)
        if not isinstance(v, dict):
            print(f"  REJECT {chapter_name}: 화자 {sp} 벡터 누락")
            return False
        missing = [a for a in AXES + FIELD_AXES if a not in v]
        if missing:
            print(f"  REJECT {chapter_name}: {sp} 축 누락 — {missing}")
            return False
        for a in AXES + FIELD_AXES:
            if not isinstance(v[a], (int, float)) or not (0 <= v[a] <= 100):
                print(f"  REJECT {chapter_name}: {sp}.{a} = {v[a]} (0~100 아님)")
                return False
    return True


def analyze_chapter(client, stem: str, chapter_name: str, speakers: list) -> dict:
    path = Path("chapters") / f"{stem}.md"
    text = path.read_text(encoding="utf-8")

    dialogue = extract_dialogue(text)
    if len(dialogue) < 500:
        dialogue = text  # 5·10장처럼 대사가 없는 장은 전문으로

    speaker_desc = " / ".join(
        f"{SPEAKER_KO[s]}({s})" for s in speakers
    )
    speaker_schema = "\n".join(
        '  "%s": {%s},' % (s, ",".join('"%s":N' % a for a in AXES + FIELD_AXES)) for s in speakers
    )
    quote_schema = ", ".join('"%s": "%s 발화 원문"' % (s, SPEAKER_KO[s]) for s in speakers)

    prompt = PROMPT_TEMPLATE.format(
        chapter_name=chapter_name,
        n_speakers=len(speakers),
        speaker_desc=speaker_desc,
        axis_gloss=AXIS_GLOSS,
        field_gloss=FIELD_GLOSS,
        speaker_schema=speaker_schema,
        quote_schema=quote_schema,
        text=dialogue,
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.content[0].text.strip()
    match = re.search(r"\{[\s\S]+\}", content)
    if not match:
        print(f"  Warning: JSON 파싱 실패 — {chapter_name}")
        print(f"  Response: {content[:200]}")
        return None
    data = json.loads(match.group())
    if not verify_axes(data, chapter_name, speakers):
        return None
    if not verify_quotes(data, text, chapter_name, speakers):
        return None
    return data


def update_html(results: dict):
    """`const DATA` 와 `const FIELD_DATA` 블록만 교체.

    건드리지 않는 것 (사람이 쓴다):
      PRIOR / PRIOR_V1 / V1_WHY  — 설계 의도와 그 이동 근거
      FIELD_PRIOR                — 현장 4축 설계 의도
      CRIT / WITNESS             — 현장 비평단 주석·증인 인용
    """
    html_path = Path("interactive/emotion_trajectory.html")
    html = html_path.read_text(encoding="utf-8")

    def esc(s):
        return s.replace("\\", "\\\\").replace("'", "\\'")

    # ── const DATA
    lines = ["const DATA = {"]
    for ch, _stem, _name, speakers in CHAPTERS:
        data = results.get(ch)
        if not data:
            continue
        lines.append(f"  {ch}: {{")
        for sp in speakers:
            vec = ",".join(f"{a}:{int(data[sp][a])}" for a in AXES)
            lines.append(f"    {sp}:{{{vec}}},")
        qs = ",\n            ".join(f"{sp}:'{esc(data['quotes'][sp])}'" for sp in speakers)
        lines.append(f"    quotes:{{{qs}}},")
        lines.append(f"    insight:'{esc(data['insight'])}'")
        lines.append("  },")
    lines.append("};")

    # ── const FIELD_DATA
    flines = ["const FIELD_DATA = {"]
    for ch, _stem, _name, speakers in CHAPTERS:
        data = results.get(ch)
        if not data:
            continue
        parts = ", ".join(
            "%s:{%s}" % (sp, ",".join(f"{a}:{int(data[sp][a])}" for a in FIELD_AXES))
            for sp in speakers
        )
        flines.append(f"  {ch}:{{{parts}}},")
    flines.append("};")

    for name, block in (("DATA", "\n".join(lines)), ("FIELD_DATA", "\n".join(flines))):
        pattern = r"const %s = \{[\s\S]*?\n\};" % name
        if not re.search(pattern, html):
            print(f"ERROR: const {name} 블록을 찾지 못했다 — HTML 구조 변경 여부 확인")
            sys.exit(1)
        html = re.sub(pattern, lambda _m, b=block: b, html, count=1)

    html_path.write_text(html, encoding="utf-8")
    print(f"Updated {html_path}")


def main():
    client = anthropic.Anthropic()
    results = {}
    rejected = []

    for ch, stem, name, speakers in CHAPTERS:
        print(f"Analyzing {name}...")
        try:
            data = analyze_chapter(client, stem, name, speakers)
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR {name}: {e}")
            data = None
        if data:
            results[ch] = data
        else:
            rejected.append(name)

    if rejected:
        print(f"\n기각된 장 {len(rejected)}개 — 기존 값 유지: {', '.join(rejected)}")

    if not results:
        print("측정된 장이 없다 — HTML 미변경")
        return

    # 기각된 장은 HTML의 기존 값을 덮지 않도록, 전량 성공일 때만 통째 교체
    if len(results) != len(CHAPTERS):
        print("전량 성공이 아니므로 HTML을 덮지 않는다 (부분 갱신 = 조용한 drift)")
        return

    update_html(results)


if __name__ == "__main__":
    main()
