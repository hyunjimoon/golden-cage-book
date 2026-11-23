#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""11_fold_ranks.py — 「접은 것을 남이 펼 수 있나」 그림 둘 (#158 코멘트용).

재지 않는다. **설명하는 손**이다 — 10 과 같은 자리이고 09 와 다르다.
입력이 없다(모양을 코드가 짓는다). 밖에서 그대로 돌아간다.

그림 1  fold_test   — 내가 펴면 늘 펴진다 / 남이 펴야 등수가 생긴다
그림 2  rank_shapes — 등수 다섯 꼴과 그 뜻

꼴의 출처 = SBC 패키지 rank_visualizations 비녜트. 다섯 꼴의 통계 이름은
그 쪽 말을 그대로 쓰고(아래 SHAPES 의 stat 칸), 왼쪽 두 칸만 글쓰기 말로 옮겼다.

⚠️ SVG 안에 이모지 금지 · CSS 변수 금지(rsvg-convert 가 var() 를 못 읽는다) · 입체 금지.

    python3 scripts/11_fold_ranks.py        # → img/issue158/*.png (밝은판·어두운판)
"""
import os, math, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "img", "issue158")
FONT = "Apple SD Gothic Neo, AppleGothic, Noto Sans KR, sans-serif"

LIGHT = dict(bg="#fcfbf8", ink="#1c1c1c", mut="#8b8b85", line="#d8d5cd",
             bar="#c7d1de", barbad="#e0b4a6", acc="#0026fb", bad="#b4472e",
             panel="#f5f3ed", ok="#2f7d5d")
DARK  = dict(bg="#16181c", ink="#ecebe6", mut="#92959b", line="#353940",
             bar="#3b4450", barbad="#6b4336", acc="#8ba4ff", bad="#e08d74",
             panel="#1d2026", ok="#6cc3a0")

# ── 등수 다섯 꼴 ────────────────────────────────────────────────────────────
# bars = 상대 높이 12칸 · head = 꼴 이름 · mean = 글쓰기 뜻 · stat = 통계 이름
SHAPES = [
    dict(key="flat",  ok=True,
         bars=[1,1,1,1,1,1,1,1,1,1,1,1],
         head="고르다",
         mean=["줄여도 잃은 게 없다.", "남이 편 뜻 사이에 내 뜻이", "아무 데나 떨어진다."],
         stat="고른 등수 (통과)"),
    dict(key="u",     ok=False,
         bars=[9,5,2.2,1.3,.9,.7,.7,.9,1.3,2.2,5,9],
         head="양 끝이 높다",
         mean=["다들 **똑같이** 읽는데", "그게 내 뜻이 아니다.", "오해가 또렷하다."],
         stat="너무 확신 — 폭이 좁다"),
    dict(key="hump",  ok=False,
         bars=[.5,.9,1.6,2.6,3.6,4.2,4.2,3.6,2.6,1.6,.9,.5],
         head="가운데가 높다",
         mean=["**제각각** 읽는다.", "너무 많이 접어서", "아무 뜻이나 될 수 있다."],
         stat="너무 자신 없다 — 폭이 넓다"),
    dict(key="right", ok=False,
         bars=[.4,.5,.7,.9,1.1,1.4,1.8,2.4,3.2,4.2,5.4,7],
         head="오른쪽으로 쏠린다",
         mean=["늘 내 뜻보다 **약하게**", "읽는다. 한 번이면 운이고", "계속이면 버릇이다."],
         stat="낮게 잡았다"),
    dict(key="left",  ok=False,
         bars=[7,5.4,4.2,3.2,2.4,1.8,1.4,1.1,.9,.7,.5,.4],
         head="왼쪽으로 쏠린다",
         mean=["늘 내 뜻보다 **세게**", "읽는다. 쏠린 쪽이", "줄이는 방식을 가리킨다."],
         stat="높게 잡았다"),
]

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def txt(x, y, s, size=13, fill="ink", w="400", anchor="start", C=None, ls="0"):
    """**굵게** 한 쌍만 지원한다 — tspan 으로 끊는다."""
    parts, bold = s.split("**"), False
    body = ""
    for p in parts:
        if p: body += f'<tspan font-weight="{700 if bold else w}">{esc(p)}</tspan>'
        bold = not bold
    return (f'<text xml:space="preserve" x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'fill="{C[fill]}" font-weight="{w}" text-anchor="{anchor}" '
            f'letter-spacing="{ls}">{body}</text>')

# ── 그림 1 — 접어서 건넸을 때 ───────────────────────────────────────────────
def fig_fold(C):
    W, H = 920, 330
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
    s.append(txt(30, 36, "접어서 건넸다. 줄여도 됐는지 어떻게 아나", 19, "ink", "700", C=C))
    s.append(txt(30, 60, "내가 다시 펴 보는 것은 시험이 아니다 — 안 적은 자리에 무엇이 들었는지 내가 알고 있다.",
                 13, "mut", C=C))

    bx = [30, 335, 640]; bw = 250; by, bh = 84, 196
    for x in bx:
        s.append(f'<rect x="{x}" y="{by}" width="{bw}" height="{bh}" rx="10" '
                 f'fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="1"/>')
    for x in (bx[0]+bw, bx[1]+bw):
        s.append(f'<path d="M{x+14} {by+bh/2} l32 0 m-9 -6 l9 6 l-9 6" fill="none" '
                 f'stroke="{C["mut"]}" stroke-width="1.6" stroke-linecap="round"/>')

    # ① 접은 쪽지
    x = bx[0]
    s.append(txt(x+16, by+28, "1  접는다", 13, "mut", "700", C=C))
    s.append(f'<rect x="{x+78}" y="{by+54}" width="{94}" height="{66}" rx="4" fill="none" '
             f'stroke="{C["ink"]}" stroke-width="1.6"/>')
    for dy in (22, 44):
        s.append(f'<line x1="{x+78}" y1="{by+54+dy}" x2="{x+172}" y2="{by+54+dy}" '
                 f'stroke="{C["line"]}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    s.append(f'<circle cx="{x+125}" cy="{by+87}" r="5.5" fill="{C["acc"]}"/>')
    s.append(txt(x+125, by+150, "내 뜻은 접힌 안쪽에 있다", 12, "mut", anchor="middle", C=C))
    s.append(txt(x+125, by+172, "건넨 것은 글자뿐", 12, "mut", anchor="middle", C=C))

    # ② 내가 편다
    x = bx[1]
    s.append(txt(x+16, by+28, "2  내가 펴 본다", 13, "mut", "700", C=C))
    s.append(f'<line x1="{x+30}" y1="{by+92}" x2="{x+220}" y2="{by+92}" stroke="{C["line"]}" stroke-width="2"/>')
    s.append(f'<circle cx="{x+125}" cy="{by+92}" r="7" fill="{C["acc"]}"/>')
    s.append(f'<path d="M{x+111} {by+70} l10 10 l20 -20" fill="none" stroke="{C["ok"]}" '
             f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(txt(x+125, by+134, "늘 펴진다", 15, "ink", "700", anchor="middle", C=C))
    s.append(txt(x+125, by+156, "답을 알고 푸는 셈이다.", 12, "mut", anchor="middle", C=C))
    s.append(txt(x+125, by+176, "한 번도 틀릴 수가 없다.", 12, "mut", anchor="middle", C=C))

    # ③ 남 여럿이 편다
    x = bx[2]
    s.append(txt(x+16, by+28, "3  남 여럿이 편다", 13, "mut", "700", C=C))
    s.append(f'<line x1="{x+22}" y1="{by+92}" x2="{x+228}" y2="{by+92}" stroke="{C["line"]}" stroke-width="2"/>')
    for i, d in enumerate([-78,-55,-34,-14, 8, 30, 52, 76]):
        s.append(f'<circle cx="{x+125+d}" cy="{by+92}" r="5" fill="{C["bar"]}" '
                 f'stroke="{C["mut"]}" stroke-width="1"/>')
    s.append(f'<line x1="{x+125-24}" y1="{by+72}" x2="{x+125-24}" y2="{by+112}" '
             f'stroke="{C["acc"]}" stroke-width="2.4"/>')
    s.append(f'<circle cx="{x+125-24}" cy="{by+92}" r="7" fill="{C["acc"]}"/>')
    s.append(txt(x+125, by+134, "내 뜻은 그중 몇 등인가", 15, "ink", "700", anchor="middle", C=C))
    s.append(txt(x+125, by+156, "여기서 처음 등수가 생긴다.", 12, "mut", anchor="middle", C=C))
    s.append(txt(x+125, by+176, "등수를 만드는 답은 밖에서 온다.", 12, "mut", anchor="middle", C=C))

    s.append(txt(30, 312, "자리는 내가 가릴 수 있다. 눈은 못 빌린다.", 14, "ink", "700", C=C))
    s.append('</svg>')
    return "\n".join(s)

# ── 그림 2 — 등수 다섯 꼴 ──────────────────────────────────────────────────
def fig_shapes(C):
    W, H = 1120, 476
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{C["bg"]}"/>']
    s.append(txt(30, 36, "등수를 여러 번 모으면 꼴이 생긴다 — 꼴마다 뜻이 다르다", 19, "ink", "700", C=C))
    s.append(txt(30, 60, "가로 = 내 뜻이 몇 등이었나 (왼쪽 꼴찌 … 오른쪽 1등) · 세로 = 그 등수가 몇 번 나왔나",
                 13, "mut", C=C))

    cw, x0, top, ph = 212, 30, 92, 150
    for i, sh in enumerate(SHAPES):
        x = x0 + i*cw
        s.append(f'<rect x="{x}" y="{top}" width="{cw-16}" height="{ph+34}" rx="10" '
                 f'fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="1"/>')
        base, bw2 = top+ph, (cw-16-28)/12
        mx = max(sh["bars"])
        for j, b in enumerate(sh["bars"]):
            h = 14 + (b/mx)*98
            s.append(f'<rect x="{x+14+j*bw2+0.8}" y="{base-h}" width="{bw2-1.6}" height="{h}" '
                     f'fill="{C["bar"] if sh["ok"] else C["barbad"]}"/>')
        # 고른 높이 기준선
        avg = base - (14 + (sum(sh["bars"])/len(sh["bars"])/mx)*98)
        s.append(f'<line x1="{x+12}" y1="{avg:.1f}" x2="{x+cw-28}" y2="{avg:.1f}" '
                 f'stroke="{C["mut"]}" stroke-width="1.2" stroke-dasharray="5 4"/>')
        s.append(f'<line x1="{x+14}" y1="{base}" x2="{x+cw-30}" y2="{base}" stroke="{C["line"]}" stroke-width="1.5"/>')
        mark = "통과" if sh["ok"] else "탈락"
        s.append(txt(x+14, base+26, mark, 12, "ok" if sh["ok"] else "bad", "700", C=C))
        s.append(txt(x+cw-30, base+26, sh["head"], 14, "ink", "700", anchor="end", C=C))

        for k, line in enumerate(sh["mean"]):
            s.append(txt(x+14, top+ph+66+k*21, line, 13, "ink", C=C))
        s.append(txt(x+14, top+ph+66+3*21+14, sh["stat"], 12, "mut", "700", C=C))

    s.append(f'<line x1="30" y1="{H-54}" x2="{W-30}" y2="{H-54}" stroke="{C["line"]}" stroke-width="1"/>')
    s.append(txt(30, H-30, "한 번 어긋난 것은 운이고, 같은 쪽으로 계속 어긋나는 것은 버릇이다.", 14, "ink", "700", C=C))
    s.append(txt(W-30, H-30, "점선 = 고를 때의 높이", 12, "mut", anchor="end", C=C))
    s.append('</svg>')
    return "\n".join(s)

def write(name, svg):
    os.makedirs(OUT, exist_ok=True)
    sp = os.path.join(OUT, name + ".svg")
    open(sp, "w", encoding="utf-8").write(svg)
    png = os.path.join(OUT, name + ".png")
    subprocess.run(["rsvg-convert", "-z", "2", "-o", png, sp], check=True)
    os.remove(sp)
    print(f"  {png}  {os.path.getsize(png)//1024}KB")

if __name__ == "__main__":
    for tag, C in (("", LIGHT), ("_dark", DARK)):
        write("fold_test" + tag,  fig_fold(C))
        write("rank_shapes" + tag, fig_shapes(C))
