# ──────────────────────────────────────────────────────────────────────────
#  (의존 — 02 가 to_ym·coil_of 를 부른다)   ·   🤚 탈피 코일 — 자에서는 내렸다
#  원본  <저자 vault>/.claude/molt_map.py   —   손으로 고치지 마라 — .claude/publish_scripts.py 가 찍는다
# ──────────────────────────────────────────────────────────────────────────

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐍 살찌는뱀 지도 생성기 — 00_사슬지도.html 의 SSOT

  입력  시공간멜로디/On/me_문현지/생산자/기억/ep*.md 의 frontmatter
  출력  같은 폴더 00_사슬지도.html

축이 둘이다.
  가로 = 시간(탈피 코일)   세로 = 극(누가 나를 재는가)

발견 = 🌫️투자자 레인이 왼쪽에서 비고 오른쪽에서 찬다.
표로 쓰지 않는다. 비어 있음은 그려야 보인다(비평v1 #2).

⚠️ 00_사슬지도.html 은 생성물이다. 손으로 고치지 마라 — 이 파일을 고쳐라.
"""

import re, sys, html, datetime
from pathlib import Path
from collections import defaultdict

VAULT = Path(__file__).resolve().parent.parent
MEM = VAULT / "시공간멜로디/On/me_문현지/생산자/기억"
OUT = MEM / "00_사슬지도.html"

# ── 탈피 코일 ──────────────────────────────────────────────
# (키, 이름, 자를 쥔 자, 시작 yyyymm, 끝 yyyymm, 닫혔나)
COILS = [
    ("c0", "꼬리",   "뱀이 먹고 자란 것",          None,     202601, True),  # 202601 포함
    ("c1", "1 다리", "내가 잰다",                  202602,   202603, True),
    ("c2", "2 지도", "모형이 잰다",                202604,   202605, True),
    ("c3", "3 보고", "사람이 잰다",                202606,   202609, True),
    ("c4", "4 피벗", "미리 선언한 내가 잰다",      202610,   202701, False),
]
COIL_NOTE = {
    "c1": "두 세계 다리 놓기 · X.3 = 보폭이 너무 넓었나",
    "c2": "박사논문 지도제작 · X.3 = 언어가 달라 안 닿았다",
    "c3": "3일마다 25번 보고 · X.3 = 그 자를 버리고 최적무지로 점프",
    "c4": "planned pivot · X.3 아직 — 안 벗었으니 못 센다",
}

POLES = [  # 그리는 순서 = 위에서 아래
    ("🦋", "사용자",  "desirability",  "#0026FB"),
    ("🧅", "기술자",  "feasibility",   "#491786"),
    ("🌫️", "투자자",  "viability",     "#C8102E"),
    ("🐦‍⬛", "협력자", "metric",        "#006610"),
]
SEASON = {"봄": 3, "여름": 7, "가을": 10, "겨울": 1}


def read_front(p: Path) -> dict:
    """--- 사이 frontmatter 를 얕게 읽는다. 중첩은 쓰지 않으므로 얕게로 충분."""
    t = p.read_text(encoding="utf-8", errors="replace")
    if not t.startswith("---"):
        return {}
    end = t.find("\n---", 3)
    d = {}
    for line in t[3:end if end > 0 else 2000].splitlines():
        m = re.match(r"^([가-힣A-Za-z_]+):\s*(.*)$", line)
        if m:
            d[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return d


def to_ym(s: str):
    """날짜에서 (연월, 정밀도)를 뽑는다. 정밀도 = 'month' | 'year' | None.

    「없음」은 발견이 아니라 자를 의심할 신호다 — 계절·연도만 있는 꼴도 받되,
    **월을 지어내지 않는다.** 연도만 있으면 그 해 전체가 한 코일 안에 들 때만 배정한다.
    해를 걸쳐 누적된 것(2023 ~ 2026)은 한 점이 아니므로 배정하지 않는다.
    """
    if not s:
        return None, None
    m = re.match(r"\s*(20\d\d)[-./](\d{1,2})", s)
    if m:                            # 머리에 박힌 연-월이 이긴다 (ep56 채록일)
        return int(m.group(1)) * 100 + int(m.group(2)), "month"
    years = re.findall(r"20\d\d", s)
    if len(set(years)) > 1:          # 누적·범위 — 한 점이 아니다
        return None, None
    m = re.search(r"(20\d\d)[-./](\d{1,2})", s)
    if m:
        return int(m.group(1)) * 100 + int(m.group(2)), "month"
    if years:
        y = int(years[0])
        for k, mo in SEASON.items():
            if k in s:
                return y * 100 + mo, "month"
        return y * 100 + 6, "year"   # 연도만 — 월은 중앙값 자리표시, 코일 판정에만 쓴다
    return None, None


def coil_of(ym, prec):
    """연도 정밀도일 때는 그 해 1월과 12월이 같은 코일에 들어야만 배정한다."""
    if ym is None:
        return None

    def bucket(v):
        for key, _, _, a, b, _ in COILS:
            if a is None:
                if v <= b:
                    return key
            elif a <= v <= b:
                return key
        return "c4" if v > 202701 else None

    if prec == "year":
        y = ym // 100
        lo, hi = bucket(y * 100 + 1), bucket(y * 100 + 12)
        return lo if lo == hi else None
    return bucket(ym)


def load():
    eps = []
    for p in sorted(MEM.glob("ep*.md")):
        f = read_front(p)
        num = p.name.split("_")[0]
        title = p.stem.split("_", 1)[1].replace("_", " ") if "_" in p.stem else p.stem
        pole = next((e for e, n, _, _ in POLES if f.get("극", "").startswith(e)
                     or n in f.get("극", "")), None)
        ym, prec = to_ym(f.get("날짜", ""))
        eps.append(dict(
            num=num, title=title, file=p.name,
            date=f.get("날짜", ""), ym=ym, prec=prec, coil=coil_of(ym, prec),
            pole=pole, 마찰=f.get("마찰", ""),
            배선=int(f["배선"]) if f.get("배선", "").isdigit() else 0,
            투향장=f.get("투향장", "").strip() or "—",
        ))
    return eps


# ── 도면 좌표 ──────────────────────────────────────────────
PAD_L, LANE_H, TOP = 132, 86, 54
COIL_W = {"c0": 300, "c1": 120, "c2": 120, "c3": 230, "c4": 150}


def layout(eps):
    """코일 안에서 편들을 가로로 고르게 편다. 시간 비례가 아니라 코일 비례."""
    xs, cum = {}, PAD_L
    for key, *_ in COILS:
        xs[key] = (cum, cum + COIL_W[key])
        cum += COIL_W[key]
    width = cum + 40
    placed = []
    for key, *_ in COILS:
        a, b = xs[key]
        for li, (emo, *_r) in enumerate(POLES):
            grp = [e for e in eps if e["coil"] == key and e["pole"] == emo]
            grp.sort(key=lambda e: (e["ym"] or 0, e["num"]))
            n = len(grp)
            for i, e in enumerate(grp):
                e["x"] = a + (b - a) * (i + 1) / (n + 1)
                e["y"] = TOP + li * LANE_H + LANE_H / 2
                placed.append(e)
    return xs, width, placed


def esc(s):
    return html.escape(str(s), quote=True)


def build():
    eps = load()
    xs, W, placed = layout(eps)
    H = TOP + len(POLES) * LANE_H + 46
    orphan = [e for e in eps if e["coil"] is None or e["pole"] is None]

    # 코일 × 극 집계
    tally = defaultdict(lambda: defaultdict(int))
    for e in eps:
        if e["coil"] and e["pole"]:
            tally[e["coil"]][e["pole"]] += 1
    lit = {k: sum(1 for p, _, _, _ in POLES if tally[k][p] > 0) for k, *_ in COILS}

    # ── svg ──
    svg = [f'<svg viewBox="0 0 {W} {H}" width="100%" preserveAspectRatio="xMinYMin meet" '
           f'font-family="var(--sans)" role="img" aria-label="네 코일 × 네 극 탈피 도면">']
    # 코일 띠
    for key, name, who, *_r, closed in COILS:
        a, b = xs[key]
        fill = "#F5F0E4" if key in ("c0",) else ("#FFF" if closed else "#FBF3F3")
        svg.append(f'<rect x="{a}" y="{TOP}" width="{b-a}" height="{len(POLES)*LANE_H}" '
                   f'fill="{fill}" stroke="#D9CFBA"/>')
        if not closed:
            svg.append(f'<rect x="{a}" y="{TOP}" width="{b-a}" height="{len(POLES)*LANE_H}" '
                       f'fill="url(#open)" stroke="none"/>')
        cx = (a + b) / 2
        svg.append(f'<text x="{cx}" y="{TOP-30}" text-anchor="middle" font-size="13" '
                   f'font-weight="700" fill="#221F1B">{esc(name)}</text>')
        svg.append(f'<text x="{cx}" y="{TOP-14}" text-anchor="middle" font-size="10.5" '
                   f'fill="#655C50">{esc(who)}</text>')
        n = sum(tally[key].values())
        svg.append(f'<text x="{cx}" y="{TOP+len(POLES)*LANE_H+19}" text-anchor="middle" '
                   f'font-size="10.5" font-family="var(--mono)" fill="#A2967F">'
                   f'{n}편 · 선 극 {lit[key]}</text>')
    # 레인
    for li, (emo, nm, lens, col) in enumerate(POLES):
        y = TOP + li * LANE_H
        svg.append(f'<line x1="{PAD_L}" y1="{y}" x2="{W-40}" y2="{y}" stroke="#EAE3D4"/>')
        svg.append(f'<text x="{PAD_L-14}" y="{y+LANE_H/2-2}" text-anchor="end" font-size="13" '
                   f'fill="{col}" font-weight="700">{emo} {esc(nm)}</text>')
        svg.append(f'<text x="{PAD_L-14}" y="{y+LANE_H/2+14}" text-anchor="end" font-size="9.5" '
                   f'font-family="var(--mono)" fill="#A2967F">{lens}</text>')
    svg.append(f'<line x1="{PAD_L}" y1="{TOP+len(POLES)*LANE_H}" x2="{W-40}" '
               f'y2="{TOP+len(POLES)*LANE_H}" stroke="#EAE3D4"/>')
    # 청안기 표식 — 닫혔는데 0편인 코일
    for key, name, *_r, closed in COILS:
        if closed and sum(tally[key].values()) == 0:
            a, b = xs[key]
            svg.append(f'<text x="{(a+b)/2}" y="{TOP+len(POLES)*LANE_H/2}" '
                       f'text-anchor="middle" font-size="12" fill="#A2967F" '
                       f'font-style="italic">청안기</text>')
            svg.append(f'<text x="{(a+b)/2}" y="{TOP+len(POLES)*LANE_H/2+17}" '
                       f'text-anchor="middle" font-size="9.5" fill="#A2967F" '
                       f'font-family="var(--mono)">눈이 덮인다</text>')
    # 점
    for e in placed:
        col = next(c for emo, _, _, c in POLES if emo == e["pole"])
        r = 4.2 + min(e["배선"], 13) * 0.42
        tip = f'{e["num"]} {e["title"]}\n{e["date"]}\n마찰: {e["마찰"] or "—"}\n배선 {e["배선"]} · 투향장 {e["투향장"]}'
        svg.append(f'<g><title>{esc(tip)}</title>'
                   f'<circle cx="{e["x"]:.1f}" cy="{e["y"]:.1f}" r="{r:.1f}" fill="{col}" '
                   f'fill-opacity=".82" stroke="#fff" stroke-width="1.1"/>'
                   f'<text x="{e["x"]:.1f}" y="{e["y"]+r+10:.1f}" text-anchor="middle" '
                   f'font-size="8" font-family="var(--mono)" fill="#655C50">{e["num"][2:]}</text></g>')
    svg.append('<defs><pattern id="open" width="7" height="7" patternUnits="userSpaceOnUse" '
               'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" '
               'stroke="#C8102E" stroke-opacity=".17"/></pattern></defs>')
    svg.append("</svg>")

    # ── 집계 표 ──
    rows = []
    for key, name, who, *_r, closed in COILS:
        cells = "".join(
            f'<td class="{"z" if tally[key][p]==0 else ""}">{tally[key][p] or "·"}</td>'
            for p, _, _, _ in POLES)
        n = sum(tally[key].values())
        wires = sum(e["배선"] for e in eps if e["coil"] == key)
        rows.append(
            f'<tr><th>{esc(name)}<i>{esc(who)}</i></th>{cells}'
            f'<td class="n">{n}</td><td class="n lit">{lit[key]}</td>'
            f'<td class="n">{wires or "·"}</td>'
            f'<td class="note">{esc(COIL_NOTE.get(key,"—"))}</td></tr>')

    orow = "".join(
        f'<li><b>{esc(e["num"])}</b> {esc(e["title"])}'
        f'<span>{esc(e["date"] or "날짜 없음")}</span></li>' for e in orphan)

    inv0, inv3 = tally["c0"]["🌫️"], tally["c3"]["🌫️"]
    n0, n3 = sum(tally["c0"].values()), sum(tally["c3"].values())
    p0 = round(inv0 / n0 * 100) if n0 else 0
    p3 = round(inv3 / n3 * 100) if n3 else 0
    today = datetime.date.today().isoformat()

    doc = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>투향 — 바뀐 것은 어느 극이 말을 많이 하나다</title>
<style>
:root{{--paper:#FBF8F0;--ink:#221F1B;--ink2:#655C50;--faint:#A2967F;--rule:#D9CFBA;
--rule2:#EAE3D4;--jeok:#C8102E;
--serif:"AppleMyungjo","Nanum Myeongjo","Noto Serif KR",serif;
--sans:"Apple SD Gothic Neo","Noto Sans KR","Pretendard",-apple-system,sans-serif;
--mono:"SF Mono",ui-monospace,Menlo,monospace;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);
font-size:15px;line-height:1.72;-webkit-font-smoothing:antialiased}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 clamp(14px,3vw,38px) 96px}}
header{{padding:clamp(40px,8vh,84px) 0 28px}}
.eyebrow{{font-family:var(--mono);font-size:11px;letter-spacing:.3em;color:var(--faint);
margin:0 0 18px;text-transform:uppercase}}
h1{{font-family:var(--serif);font-weight:400;margin:0;font-size:clamp(30px,5vw,54px);
line-height:1.15;letter-spacing:-.015em;max-width:20ch}}
h1 em{{font-style:normal;color:var(--jeok)}}
.deck{{margin:22px 0 0;max-width:62ch;color:var(--ink2);font-size:16.5px}}
.deck b{{color:var(--ink);font-weight:600}}
.stat{{display:flex;gap:32px;flex-wrap:wrap;margin-top:28px;padding-top:20px;
border-top:1px solid var(--rule)}}
.stat div{{display:grid}} .stat b{{font-family:var(--mono);font-size:26px;line-height:1}}
.stat b.bad{{color:var(--jeok)}}
.stat span{{font-size:11.5px;color:var(--faint);letter-spacing:.05em;margin-top:5px}}
section{{padding-top:clamp(40px,6vh,68px)}}
h2{{font-family:var(--serif);font-weight:400;font-size:clamp(20px,2.6vw,27px);margin:0 0 6px}}
.sub{{margin:0 0 20px;color:var(--faint);font-size:13.5px;max-width:68ch}}
.plan{{border:1px solid var(--ink);background:#fff;overflow-x:auto}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:8px}}
th,td{{border-bottom:1px solid var(--rule2);padding:9px 10px;text-align:center}}
thead th{{font-size:11px;letter-spacing:.06em;color:var(--faint);font-weight:600;
border-bottom:1px solid var(--rule)}}
tbody th{{text-align:left;font-weight:600;display:grid;gap:1px}}
tbody th i{{font-style:normal;font-size:11px;color:var(--faint)}}
td.n{{font-family:var(--mono)}} td.z{{color:var(--jeok);font-weight:700}}
td.lit{{font-weight:700}}
td.note{{text-align:left;font-size:12px;color:var(--ink2)}}
ul.orph{{list-style:none;padding:0;margin:0;display:grid;
grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:2px 20px}}
ul.orph li{{font-size:13px;border-bottom:1px dotted var(--rule2);padding:5px 0;
display:flex;gap:8px;align-items:baseline}}
ul.orph b{{font-family:var(--mono);font-size:11.5px;color:var(--faint)}}
ul.orph span{{margin-left:auto;font-size:11px;color:var(--faint);font-family:var(--mono)}}
.warn{{border-left:3px solid var(--jeok);padding:12px 0 12px 16px;margin:22px 0;
background:#fff;max-width:72ch}}
.warn b{{color:var(--jeok)}}
footer{{margin-top:70px;padding-top:18px;border-top:1px solid var(--rule);
font-size:11.5px;color:var(--faint);font-family:var(--mono)}}
@media(max-width:700px){{.stat{{gap:20px}}}}
</style></head><body><div class="wrap">

<header>
<p class="eyebrow">살찌는뱀 · 네 코일 × 네 극</p>
<h1>네 극은 꼬리에도 다 있다. 바뀐 것은 <em>어느 극이 말을 많이 하나</em>다.</h1>
<p class="deck">살찌는 단위는 개월이 아니다 — <b>1.5·3·4·4</b>는 안 살찐다.
「동시에 선 극의 수」도 아니다 — <b>꼬리에 이미 넷이 다 섰다({lit['c0']}/4).</b>
남는 자는 <b>밀도</b>다. 🌫️투자자가 꼬리에서 <b>{p0}%</b>, 세 번째 탈피에서 <b>{p3}%</b>.
뱀은 벗기 전 눈꺼풀이 뿌예지고, 벗고 나면 <b>같은 넷을 다른 비율로</b> 본다.</p>
<div class="stat">
<div><b>{len(eps)}</b><span>일화원소</span></div>
<div><b>{inv0}/{n0} · {p0}%</b><span>🌫️ · 꼬리</span></div>
<div><b class="bad">{inv3}/{n3} · {p3}%</b><span>🌫️ · 3 보고</span></div>
<div><b>{p3/p0 if p0 else 0:.1f}×</b><span>밀도 비</span></div>
<div><b>{len(orphan)}</b><span>좌표 없는 편</span></div>
</div>
</header>

<section>
<h2>도면 — 비어 있음은 그려야 보인다</h2>
<p class="sub">가로 = 탈피 코일 · 세로 = 누가 나를 재는가. 점 크기 = 배선 수.
🌫️ 레인을 왼쪽부터 눈으로 훑으면 표를 읽지 않아도 보인다.</p>
<div class="plan">{''.join(svg)}</div>
</section>

<section>
<h2>셈</h2>
<table>
<thead><tr><th style="text-align:left">코일 · 자를 쥔 자</th>
{''.join(f'<th>{e}</th>' for e,_,_,_ in POLES)}
<th>편</th><th>선 극</th><th>배선</th><th style="text-align:left">X.3 — 흐려진 자리</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>

<div class="warn">
<p><b>⚠️ 배선 수를 해상도의 자로 쓰지 마라.</b> 배선은 사건이 일어난 때가 아니라
<b>글을 쓴 때</b>를 반영한다 — 최근 것을 더 촘촘히 썼을 뿐일 수 있다.
극 수는 62편이 같은 시기 한 눈으로 배정돼 코일 간 비교가 선다. 그래서 극을 자로 골랐다.</p>
<p><b>⚠️ 코일 1의 「선 극 {lit['c1']}」은 못 믿는다.</b> {sum(tally['c1'].values())}편짜리 표본이다.</p>
<p><b>⚠️ 코일 4의 0은 코일 2의 0과 다른 0이다.</b> 2는 청안기(벗고 나서 2.3이 도착했다),
4는 아직 안 벗었다. <b>탈피는 끝난 뒤에만 세어진다.</b></p>
</div>
</section>

<section>
<h2>좌표 없는 {len(orphan)}편 — 꼬리의 꼬리</h2>
<p class="sub">연도만 있거나 「상시」인 편. 월을 지어내지 않았다.
도면에서 빠진 것이지 장부에서 빠진 것이 아니다.</p>
<ul class="orph">{orow}</ul>
</section>

<footer>생성 {today} · .claude/molt_map.py · 손으로 고치지 마라, 생성기를 고쳐라<br>
입력 {MEM.relative_to(VAULT)}/ep*.md — frontmatter 날짜·극·배선·마찰</footer>
</div></body></html>"""
    return doc, eps, tally, lit, orphan


if __name__ == "__main__":
    doc, eps, tally, lit, orphan = build()
    OUT.write_text(doc, encoding="utf-8")
    print(f"✓ {OUT.relative_to(VAULT)}  ({len(doc)//1024}KB)")
    print(f"  일화원소 {len(eps)}편 · 좌표 없음 {len(orphan)}편")
    for key, name, *_ in COILS:
        n = sum(tally[key].values())
        mix = " ".join(f"{p}{tally[key][p]}" for p, _, _, _ in POLES if tally[key][p])
        print(f"  {name:<7} {n:>3}편  선극 {lit[key]}  {mix}")
