"""
reader_score.py — /reader 패널로 각 장을 4 이해관계자 렌즈로 채점.

pivot-game의 📐자 과정(QUESTIONS→RUBRIC→agent→ascent→metric-evolution)을
소설에 이식(Processify). 과정 문법: pivot-game/METHOD.md.

GitHub Actions에서 chapters/ch*.md 변경 시 자동 실행 →
docs/reader_scores.json(이력) + docs/ascent.html(상승 시각화) 갱신.
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("anthropic package not installed. Run: pip install anthropic")
    sys.exit(1)

MODEL = "claude-opus-4-8"

# 10장 = 파일 · 표시명(coverage-matrix 라벨과 동일)
CHAPTERS = [
    ("ch1_mirror_cage",    "🪞1장-거울"),
    ("ch2_telescope_cage", "🔭2장-망원경"),
    ("ch3_glass_cage",     "💒3장-스테인굴레스"),
    ("ch4_clock_cage",     "⏱️4장-시계"),
    ("ch5_mirror_nest",    "🐀5장-101호"),
    ("ch6_butterfly_nest", "🦋6장-나비"),
    ("ch7_tulip_nest",     "🌷7장-튤립구근"),
    ("ch8_mist_nest",      "🌫️8장-안개"),
    ("ch9_raven_nest",     "🐦‍⬛9장-까마귀"),
    ("ch10_epilogue",      "⭐️10장-금새"),
]

# 4 이해관계자 렌즈 (=/reader 패널 축, RUBRIC.md와 동일)
LENSES = ["tech", "user", "investor", "collab"]
LENS_LABEL = {
    "tech": "🛠️기술자·실현",
    "user": "🙋사용자·욕망",
    "investor": "💰투자자·값어치",
    "collab": "🤝협력자·척도정직",
}

PROMPT_TEMPLATE = """다음은 창업소설 "황금새장을열다"의 {chapter_name} 전문이다.

너는 /reader 패널이다. 이 장이 금새 4 이해관계자를 얼마나 *계산끝내* 만족시키는지
각 렌즈로 0~3점 채점하라. 발신자(저자) 욕망이 아니라 *수신자가 실제로 원하는 것* 기준.

척도 (렌즈당 0~3):
- 0 부재: 그 렌즈가 볼 게 없음
- 1 언급: 스치듯, 알맹이 없음
- 2 응답: 답은 있으나 추상적·구체 없음
- 3 계산끝낸 응답: 답 + 메커니즘/숫자/장면 1개 + "이건 내 얘기" 공명

4 렌즈:
- tech (🛠️기술자·실현가능): 메커니즘·재현 단계·구체가 있는가. 손짓(hand-waving) 적발.
- user (🙋사용자·욕망): 수요자가 이걸 원하고 공명하는가. 공허한 위로 적발.
- investor (💰투자자·값어치): 희소자원(주의·자본) 값을 하는가. 과대포장 컷.
- collab (🤝협력자·척도정직): 자가 옳은 걸 재는가. calibration·gameable 아님.

반드시 아래 JSON 형식으로만 응답하라 (설명 없이):
{{
  "tech": N, "user": N, "investor": N, "collab": N,
  "weakest": "가장 낮은 렌즈 키 (tech/user/investor/collab)",
  "note": "한 줄 진단 — 이탈/반대 지점 (가장 값진 산출물)"
}}

본문:
{text}
"""


def score_chapter(client, ch_id: str, ch_name: str) -> dict:
    path = Path("chapters") / f"{ch_id}.md"
    if not path.exists():
        print(f"  {ch_id}.md 없음 — 건너뜀")
        return None
    text = path.read_text(encoding="utf-8")

    prompt = PROMPT_TEMPLATE.format(chapter_name=ch_name, text=text)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.content[0].text.strip()
    match = re.search(r"\{[\s\S]+\}", content)
    if not match:
        print(f"  경고: JSON 파싱 실패 — {ch_name}")
        return None
    try:
        data = json.loads(match.group())
    except json.JSONDecodeError:
        print(f"  경고: JSON 디코드 실패 — {ch_name}")
        return None
    # 0~3 클램프
    for lens in LENSES:
        v = int(data.get(lens, 0))
        data[lens] = max(0, min(3, v))
    return data


def load_history() -> list:
    p = Path("docs/reader_scores.json")
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def render_ascent_html(history: list, matrix: dict) -> str:
    """history=[{date,total,...}], matrix={ch_name:{lens:score,...}} (최신)."""
    MAXTOTAL = len(CHAPTERS) * len(LENSES) * 3  # 120
    latest = history[-1] if history else {"date": "—", "total": 0}
    pct = round(latest["total"] / MAXTOTAL * 100) if MAXTOTAL else 0

    # ascent 계단 (SVG polyline)
    pts = []
    n = max(len(history), 1)
    for i, h in enumerate(history):
        x = 70 + (690 * i / max(n - 1, 1))
        y = 360 - (h["total"] / MAXTOTAL) * 320
        pts.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(pts)
    dots = "".join(
        f'<circle cx="{p.split(",")[0]}" cy="{p.split(",")[1]}" r="3.5" fill="var(--collab)"></circle>'
        for p in pts
    )

    # 장×렌즈 매트릭스
    rows = ""
    for ch_id, ch_name in CHAPTERS:
        cells = ""
        for lens in LENSES:
            v = matrix.get(ch_name, {}).get(lens)
            if v is None:
                cells += '<td class="gap">·</td>'
            else:
                cells += f'<td class="s{v}">{v}</td>'
        rowsum = sum(matrix.get(ch_name, {}).get(l, 0) for l in LENSES)
        rows += f'<tr><th>{ch_name}</th>{cells}<td class="sum">{rowsum}</td></tr>'
    lens_head = "".join(f"<th>{LENS_LABEL[l]}</th>" for l in LENSES)

    return f"""<title>📐자 — 원고 품질 상승 추이</title>
<style>
  :root{{
    --ground:#F5F7FA; --panel:#FFF; --ink:#1B2230; --ink-soft:#5A6577;
    --line:#DCE2EB; --grid:#E7ECF3;
    --tech:#7C3AED; --user:#2563EB; --investor:#DC2626; --collab:#059669;
    --gold:#B8860B;
    --serif:Georgia,"Times New Roman",serif; --sans:system-ui,-apple-system,sans-serif;
  }}
  @media (prefers-color-scheme:dark){{:root{{
    --ground:#12161D; --panel:#1A1F28; --ink:#EAEEF4; --ink-soft:#9AA5B4;
    --line:#2A313C; --grid:#232A34;
    --tech:#A17BF0; --user:#5B92F5; --investor:#F26D6D; --collab:#34C88A; --gold:#E0B94B;
  }}}}
  :root[data-theme="dark"]{{
    --ground:#12161D; --panel:#1A1F28; --ink:#EAEEF4; --ink-soft:#9AA5B4;
    --line:#2A313C; --grid:#232A34;
    --tech:#A17BF0; --user:#5B92F5; --investor:#F26D6D; --collab:#34C88A; --gold:#E0B94B;
  }}
  *{{box-sizing:border-box}}
  body{{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);line-height:1.55}}
  .wrap{{max-width:940px;margin:0 auto;padding:44px 24px 72px}}
  .eyebrow{{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-soft);font-weight:600;margin:0 0 10px}}
  h1{{font-family:var(--serif);font-weight:600;font-size:clamp(28px,5vw,44px);line-height:1.08;margin:0 0 12px}}
  h1 .num{{font-variant-numeric:tabular-nums}}
  .lede{{font-size:16px;color:var(--ink-soft);max-width:62ch;margin:0 0 34px}}
  .lede b{{color:var(--ink)}}
  .panel{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:24px;margin:0 0 24px}}
  .panel h2{{font-family:var(--serif);font-size:19px;font-weight:600;margin:0 0 3px}}
  .panel .sub{{font-size:13px;color:var(--ink-soft);margin:0 0 16px}}
  svg{{display:block;width:100%;height:auto}}
  .gridln{{stroke:var(--grid);stroke-width:1}}
  .ceil{{stroke:var(--gold);stroke-width:1.5;stroke-dasharray:3 4;opacity:.7}}
  .ax{{fill:var(--ink-soft);font-size:12px;font-variant-numeric:tabular-nums}}
  table{{width:100%;border-collapse:collapse;font-size:13px}}
  th,td{{padding:7px 9px;text-align:center;border-bottom:1px solid var(--line)}}
  th{{color:var(--ink-soft);font-weight:600;font-size:12px}}
  tbody th{{text-align:left;font-weight:600;color:var(--ink)}}
  td.gap{{color:var(--ink-soft);opacity:.4}}
  td.sum{{font-weight:700;font-variant-numeric:tabular-nums}}
  td.s0{{color:var(--investor)}} td.s1{{color:var(--ink-soft)}}
  td.s2{{color:var(--user)}} td.s3{{color:var(--collab);font-weight:700}}
  .foot{{font-size:12.5px;color:var(--ink-soft);margin:20px 2px 0;max-width:64ch}}
</style>
<div class="wrap">
  <p class="eyebrow">황금새장을열다 · /reader 4 이해관계자 · {len(CHAPTERS)}장 커버리지</p>
  <h1>📐자로 잰 원고 품질,<br><span class="num">{latest['total']}</span> <span style="color:var(--ink-soft);font-weight:400">/ {MAXTOTAL}</span> <span style="font-size:.5em;color:var(--ink-soft)">({pct}%)</span></h1>
  <p class="lede">/reader 4 이해관계자(<b>🛠️기술자·🙋사용자·💰투자자·🤝협력자</b>)가 push마다 각 장을 0–3점으로 채점한다. 갱신: <b>{latest['date']}</b>. 과정 문법 = pivot-game의 📐자 5단계(수집→자→agent→상승→자 진화)를 소설에 이식.</p>

  <section class="panel">
    <h2>상승 추이 — push마다 한 점</h2>
    <p class="sub">누적 📐자 총점. 만점 {MAXTOTAL}(= {len(CHAPTERS)}장 × 4렌즈 × 3점).</p>
    <svg viewBox="0 0 800 400" role="img" aria-label="원고 품질 상승 추이">
      <line class="ceil" x1="70" y1="40" x2="760" y2="40"></line>
      <text class="ax" x="764" y="44">{MAXTOTAL} 만점</text>
      <line class="gridln" x1="70" y1="200" x2="760" y2="200"></line>
      <text class="ax" x="58" y="205" text-anchor="end">{MAXTOTAL//2}</text>
      <line class="gridln" x1="70" y1="360" x2="760" y2="360"></line>
      <text class="ax" x="58" y="365" text-anchor="end">0</text>
      <polyline points="{polyline}" fill="none" stroke="var(--collab)" stroke-width="3" stroke-linejoin="round"></polyline>
      {dots}
    </svg>
  </section>

  <section class="panel">
    <h2>장 × 렌즈 — 어디가 계산끝났나</h2>
    <p class="sub">0=부재·1=언급·2=응답·3=계산끝낸 응답. <b>·</b> = calibration gap(그 장에 그 렌즈 미실림).</p>
    <table>
      <thead><tr><th>장 \\ 렌즈</th>{lens_head}<th>합계</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </section>

  <p class="foot"><b>읽는 법:</b> 계단이 오르면 원고가 4 이해관계자를 더 계산끝내 만족시킨 것. 빈 칸(·)이 남으면 그 장은 그 렌즈에 아직 답하지 않았다 — 다음 개선 후보. 반대·이탈이 가장 값진 산출물이므로 낮은 점수 칸이 지도다. RUBRIC: <a href="../RUBRIC.md">RUBRIC.md</a>.</p>
</div>
"""


def main():
    client = anthropic.Anthropic()
    matrix = {}
    for ch_id, ch_name in CHAPTERS:
        print(f"채점 {ch_name}...")
        data = score_chapter(client, ch_id, ch_name)
        if data:
            matrix[ch_name] = {l: data[l] for l in LENSES}
            print(f"  {matrix[ch_name]}  · {data.get('note','')}")

    if not matrix:
        print("채점된 장 없음 — 종료")
        sys.exit(1)

    total = sum(sum(m.values()) for m in matrix.values())
    history = load_history()
    history.append({
        "date": date.today().isoformat(),
        "total": total,
        "matrix": matrix,
    })

    Path("docs").mkdir(exist_ok=True)
    Path("docs/reader_scores.json").write_text(
        json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    Path("docs/ascent.html").write_text(
        render_ascent_html(history, matrix), encoding="utf-8"
    )
    print(f"완료. 총점 {total}/{len(CHAPTERS)*len(LENSES)*3}. docs/ascent.html·reader_scores.json 갱신.")


if __name__ == "__main__":
    main()
