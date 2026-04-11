"""
SBC Emotion Analysis — 다/세 대사에서 감정 벡터 추출.
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

CHAPTERS = [
    ("ch1_mirror_cage", "1장 거울새장"),
    ("ch2_telescope_cage", "2장 망원경새장"),
    ("ch3_stained_glass_cage", "3장 스테인드글라스새장"),
    ("ch4_clock_cage", "4장 시계새장"),
]

AXES = ["desperate", "self-deception", "detached", "guilty", "calm-uncertain", "playful"]

PROMPT_TEMPLATE = """다음은 창업소설 "황금새장을열다"의 {chapter_name} 전문이다.
두 캐릭터가 있다:
- 다(DA): 낭만으로 뛰는 사람 (아크: 엠마→타루)
- 세(SE): 분석으로 보는 사람 (아크: 살리나→리외)

이 장의 **다:**와 **세:** 대사를 모두 읽고, 각 캐릭터의 감정 상태를 6축으로 측정하라.

6축 (0~100):
1. desperate (절박)
2. self-deception (자기기만)
3. detached (초연/방관)
4. guilty (죄책/자각)
5. calm-uncertain (침착한 불확실)
6. playful (장난/유연)

또한:
- daPos: 엠마→타루 아크에서 위치 (0=엠마, 100=타루)
- sePos: 살리나→리외 아크에서 위치 (0=살리나, 100=리외)
- 각 캐릭터의 가장 감정이 드러나는 대사 1개씩 선택

반드시 아래 JSON 형식으로만 응답하라 (설명 없이):
{{
  "da": {{"desperate":N,"self-deception":N,"detached":N,"guilty":N,"calm-uncertain":N,"playful":N}},
  "se": {{"desperate":N,"self-deception":N,"detached":N,"guilty":N,"calm-uncertain":N,"playful":N}},
  "daPos": N,
  "sePos": N,
  "daQuote": "대사 원문",
  "seQuote": "대사 원문",
  "insight": "한 줄 진단"
}}

본문:
{text}
"""


def extract_dialogue(text: str) -> str:
    """Keep only lines with **다:** or **세:** and surrounding context."""
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        if "**다:**" in line or "**세:**" in line:
            # include 1 line before for context
            if i > 0 and lines[i - 1].strip():
                result.append(lines[i - 1])
            result.append(line)
    return "\n".join(result)


def analyze_chapter(client, chapter_id: str, chapter_name: str) -> dict:
    path = Path("chapters") / f"{chapter_id}.md"
    text = path.read_text(encoding="utf-8")

    # Send full text (dialogue extraction optional for shorter context)
    dialogue = extract_dialogue(text)
    if len(dialogue) < 500:
        dialogue = text  # fallback to full text

    prompt = PROMPT_TEMPLATE.format(chapter_name=chapter_name, text=dialogue)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.content[0].text.strip()
    # Extract JSON from response
    match = re.search(r"\{[\s\S]+\}", content)
    if not match:
        print(f"  Warning: Could not parse JSON for {chapter_name}")
        print(f"  Response: {content[:200]}")
        return None
    return json.loads(match.group())


def euclidean_distance(da: dict, se: dict) -> int:
    total = 0
    for axis in AXES:
        key = axis
        d = da.get(key, 0) - se.get(key, 0)
        total += d * d
    return int((total ** 0.5) / (100 * len(AXES) ** 0.5) * 100)


def update_html(results: dict):
    html_path = Path("interactive/emotion_trajectory.html")
    html = html_path.read_text(encoding="utf-8")

    # Build new DATA object
    lines = ["const DATA = {"]
    for ch_num, data in sorted(results.items()):
        da = data["da"]
        se = data["se"]
        dist = euclidean_distance(da, se)
        da_str = ",".join(f"'{k}':{v}" if "-" in k else f"{k}:{v}" for k, v in da.items())
        se_str = ",".join(f"'{k}':{v}" if "-" in k else f"{k}:{v}" for k, v in se.items())
        dq = data["daQuote"].replace("'", "\\'")
        sq = data["seQuote"].replace("'", "\\'")
        ins = data["insight"].replace("'", "\\'")
        lines.append(f"  {ch_num}: {{")
        lines.append(f"    da: {{{da_str}}},")
        lines.append(f"    se: {{{se_str}}},")
        lines.append(f"    daPos: {data['daPos']}, sePos: {data['sePos']},")
        lines.append(f"    daQuote: {{speaker:'다', text:'{dq}'}},")
        lines.append(f"    seQuote: {{speaker:'세', text:'{sq}'}},")
        lines.append(f"    insight: '{ins}',")
        lines.append(f"    distance: {dist}")
        lines.append(f"  }},")
    lines.append("};")
    new_data = "\n".join(lines)

    # Replace old DATA block
    pattern = r"const DATA = \{[\s\S]*?\n\};"
    html = re.sub(pattern, new_data, html)

    html_path.write_text(html, encoding="utf-8")
    print(f"Updated {html_path}")


def main():
    client = anthropic.Anthropic()
    results = {}

    for i, (ch_id, ch_name) in enumerate(CHAPTERS, 1):
        print(f"Analyzing {ch_name}...")
        data = analyze_chapter(client, ch_id, ch_name)
        if data:
            results[i] = data
            print(f"  da: {data['da']}")
            print(f"  se: {data['se']}")
        else:
            print(f"  FAILED — skipping")

    if len(results) == 4:
        update_html(results)
        print("Done. All 4 chapters analyzed.")
    else:
        print(f"Only {len(results)}/4 chapters succeeded. HTML not updated.")
        sys.exit(1)


if __name__ == "__main__":
    main()
