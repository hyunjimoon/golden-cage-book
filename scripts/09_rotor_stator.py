#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""로터와 스테이터 — 감정 낱말로 센 열 장 (gcb #9).

2026-05-02 가 정의하고 한 번도 자동화하지 않은 10 cluster 를 구현한다.
새 자가 아니라 있는 자에 손잡이를 단 것이다(#9 ⭐ 「환산표가 없다」).

누가 말하나 — 다섯으로 가른다
  말머리 「다:」 「세:」 「세다:」 가 셋. 머리글이 발화 묶음을 끊는다.
  황·뒤마·일연 등 다른 입과, 임자가 안 적힌 줄(5·10장의 1인칭 문장)은
  빼 둔다 — 투향의 인물이 아니라 파서의 통이라 판에 올리지 않는다.

디자인 (2026-11-19 30 비판 중 상위 아홉 반영)
  · 인물 셋만 선으로 — 속말·해설은 아래 얇은 띠로 강등(종류가 다르다)
  · y 눈금을 세운다 · 0 은 선으로 안 잇는다
  · 라벨은 각 인물의 꼭대기에만 — 「고요」가 모든 점에 붙어 변별력이 0 이었다
  · 셋째 표 높이를 자동 계산 — 넘쳐서 바닥글과 겹쳤다
  · 범례를 선 끝에 직접 붙인다 · 0 인 칸 셋은 한 줄로 접는다

⚠️ 씨앗은 손으로 지었다. 바닥에 전부 적어 두니 누구든 다시 연다.
⚠️ SVG 에 이모지 금지(rsvg 에서 검은 네모).

이 사본은 **공개면 `chapters/` 를 읽는다.** 저자 vault 를 안 보므로 밖에서 그대로 돌아간다
(`05_style_converge.py` 와 같은 꼴). 말머리 서식이 동기화로 안 변해서 값은 저자 판과 같다 —
실측 2026-11-21: 1장 다 16·세 15, 7장 다 2·세다 16 으로 양쪽이 일치했다.

  python3 scripts/09_rotor_stator.py
"""
import os, re, glob, subprocess, unicodedata

N = lambda s: unicodedata.normalize("NFC", s)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "chapters")
OUT_SVG = os.path.join(HERE, "09_rotor_stator.svg")
PUB_PNG = os.path.join(HERE, "09_rotor_stator.png")
DREW = os.environ.get("DREW") or __import__("datetime").date.today().isoformat()

BG, INK, GRID, HI = "#0B0B0C", "#EDE7DC", "#242422", "#E8BC5C"
DA, SE, SEDA = "#F08A3C", "#C9B99A", "#E07AC8"      # 인물 셋
NO = "#F0605A"

CLUSTERS = [
 ("두려움·압도", ["무서","두려","서늘","뜨끔","체한","숨이 막","떨렸","떨린","떨려","공포","불안","오싹","아찔","조마","겁이","겁나"], ""),
 ("평온",       ["평온","고요","안도","숨이 트","편안","잔잔","후련"], ""),
 ("연민·고마움", ["고마","감사","미안","안타까","연민","뭉클","애틋","짠했"], "05-02 둘 다 가졌다"),
 ("경계·의심",   ["의심","경계","포획","수상","미심","떠보","간 보"], "05-02 세 전유"),
 ("절망·수치",   ["참담","부끄","수치","절망","자책","한심","후회","창피","민망","비참","낯 뜨","울었","눈물","울음"], ""),
 ("분노",       ["분노","화가 나","화가 치","화를 냈","화를 내","짜증","분했","억울","역겨","혐오","미워","원망"], ""),
 ("장난",       ["웃었","웃음","장난","농담","유쾌","재밌","익살","깔깔"], ""),
 ("해방",       ["해방","숨통"], ""),
 ("소진·물러남", ["지쳤","지친","무기력","허탈","체념","시들","식었","식은","텅 비","소진","넋"], "05-02 세의 가장 센 칸"),
 ("환희",       ["기뻤","기쁨","환희","벅찼","벅찬","신났","설렜","들떴","짜릿"], ""),
 ("자긍",       ["자랑","뿌듯","자긍","당당","우쭐"], ""),
]
CHS = [("1","1 거울"),("2","2 망원경"),("3","3 스테인굴레스"),("4","4 시계"),("5","5 101"),
       ("6","6 나비"),("7","7 튤립"),("8","8 안개"),("9","9 까마귀"),("10","10 투향")]
CAST = [("다", DA), ("세", SE), ("세다", SEDA)]
TAG = re.compile(r"^\*\*([^*:]{1,14}):\*\*")
TAIL = re.compile(r"[가-힣]{0,4}")
FIRST = ("나는", "내가", "나를", "나도", "나에게", "나한테", "내 ", "우리는")
W, LX = 1480, 64


def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")


def t(x, y, s, sz, col, bold=False, anc="start", op=1.0):
    w = ' font-weight="700"' if bold else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{sz}" fill="{col}" '
            f'fill-opacity="{op}" text-anchor="{anc}"{w}>{esc(s)}</text>')


def measure():
    def pick(ch):
        c = sorted(glob.glob(os.path.join(SRC, f"ch{ch}_*.md")))
        if ch == "10": c = [p for p in c if "epilogue" not in p]
        assert len(c) == 1, f"ch{ch} 가 하나로 안 잡힌다: {c}"
        return c[0]
    per, prof, ev = {}, {}, {}
    for ch, _ in CHS:
        cur, buf = None, {}
        for ln in N(open(pick(ch), encoding="utf-8").read()).splitlines():
            if ln.startswith("#"):
                cur = None
            m = TAG.match(ln)
            if m: cur = m.group(1)
            if cur in ("다", "세", "세다"):
                key = cur
            elif cur is not None:
                key = "다른 입"
            else:
                key = "속말" if any(w in ln for w in FIRST) else "해설"
            buf.setdefault(key, []).append(ln)
        for who, _c in CAST:
            txt = "\n".join(buf.get(who, []))
            tot, words = 0, {}
            for name, seeds, _n in CLUSTERS:
                n = sum(txt.count(s) for s in seeds)
                tot += n
                if n: prof[(who, name)] = prof.get((who, name), 0) + n
                for sd in seeds:
                    for m in re.finditer(re.escape(sd), txt):
                        w = (sd + TAIL.match(txt[m.end():]).group(0)).strip()
                        words[w] = words.get(w, 0) + 1
            per[(ch, who)] = tot
            if words:
                ev[(ch, who)] = sorted(words.items(), key=lambda kv: (-kv[1], kv[0]))
    return per, prof, ev


def build(per, prof, ev):
    # ── 셋째 표의 줄 수를 먼저 세어 캔버스 높이를 정한다 (넘침 방지)
    blocks = []
    for ch, name in CHS:
        rs = [(w, c) for w, c in CAST if ev.get((ch, w))]
        blocks.append((name, ch, rs))
    nrow = sum(1 + len(rs) for _n, _c, rs in blocks)
    colrows = (nrow + 1) // 2

    o = []   # 높이는 끝에서 정해 머리에 끼운다

    o.append(t(LX, 54, "로터와 스테이터 — 감정 낱말로 센 열 장", 27, INK, bold=True))
    o.append(t(LX, 86, "로터(다)는 몸으로 느끼고 스테이터(세)는 거리 둬 본다. 둘은 손잡이의 양 끝이 아니라 "
                       "동시에 있어야 도는 두 부품이다.", 15, INK, op=.78))
    o.append(t(LX, 110, "말수가 아니라 감정 낱말을 세었다 — 적은 말로 더 세게 당길 수 있다. "
                        "5·10장엔 대사가 없다. 그 장의 감정은 임자가 안 적힌 1인칭 문장에 있고, 여기 셋에는 안 센다.",
               13.5, INK, op=.5))

    d14 = sum(per[(c, "다")] for c in "1234")
    d69 = sum(per[(c, "다")] for c in "6789")
    s69 = sum(per[(c, "세다")] for c in "6789")
    o.append(f'<rect x="{LX}" y="130" width="{W-2*LX}" height="58" rx="5" '
             f'fill="{NO}" fill-opacity=".10" stroke="{NO}" stroke-opacity=".40"/>')
    o.append(t(LX + 16, 152, f"로터가 식었다 — 둥지 넷에서 다 {d69} 대 세다 {s69}. "
                             f"1~4장의 다는 {d14} 이었다.", 16, NO, bold=True))
    o.append(t(LX + 16, 176, "그 1~4장도 깎여 있었고 오늘 되돌렸다 — 05-02 가 적어 둔 다의 몸 어휘 중 여섯이 0 이었다"
                             "(한심·서늘·뜨끔·숨이 막·참담·울었다). 넷을 1~3장에 다시 넣었다. 4장은 안 깎여 안 건드렸다.",
               13, NO, op=.85))

    # ══ 판 하나 — 인물 셋
    TOP, BOT = 248, 452
    px0, px1 = LX + 54, W - LX - 232
    mx = max(per[(c, w)] for c, _ in CHS for w, _ in CAST)
    step = 4 if mx <= 12 else 5
    xs = {c: px0 + (px1 - px0) * i / (len(CHS) - 1) for i, (c, _) in enumerate(CHS)}
    yo = lambda v: BOT - (BOT - TOP) * v / (mx + 1)

    for g in range(0, mx + 2, step):
        y = yo(g)
        o.append(f'<line x1="{px0-16}" y1="{y:.1f}" x2="{px1+16}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        o.append(t(px0 - 24, y + 4, str(g), 11.5, INK, anc="end", op=.45))
    for c in ("5", "10"):
        o.append(f'<rect x="{xs[c]-24:.1f}" y="{TOP-20}" width="48" height="{BOT-TOP+20}" '
                 f'fill="{HI}" fill-opacity=".11"/>')
        o.append(t(xs[c], TOP - 28, "셋 다 입을 닫는다", 12, HI, anc="middle", bold=True))

    for who, col in CAST:
        seg, pts = [], []
        for c, _ in CHS:
            v = per[(c, who)]
            if v:
                pts.append(f"{xs[c]:.1f},{yo(v):.1f}")
            else:
                if len(pts) > 1: seg.append(pts)
                pts = []
        if len(pts) > 1: seg.append(pts)
        for sp in seg:
            o.append(f'<polyline points="{" ".join(sp)}" fill="none" stroke="{col}" '
                     f'stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round"/>')
        for c, _ in CHS:
            v = per[(c, who)]
            if v:
                o.append(f'<circle cx="{xs[c]:.1f}" cy="{yo(v):.1f}" r="4.6" fill="{col}"/>')
        # 선 끝에 직접 이름을 붙인다 (범례를 없앤다)
        last = [c for c, _ in CHS if per[(c, who)]][-1]
        tot = sum(per[(c, who)] for c, _ in CHS)
        nudge = {"다": 16, "세": 5, "세다": -10}[who]
        o.append(t(xs[last] + 15, yo(per[(last, who)]) + nudge,
                   f"{who}  {tot}", 15, col, bold=True))
    o.append(t(px0 - 24, TOP - 30, "감정", 12, INK, anc="end", op=.5))
    o.append(t(px0 - 24, TOP - 16, "낱말 수", 12, INK, anc="end", op=.5))

    # 꼭대기에만 낱말을 단다
    for who, col in CAST:
        peak = max((c for c, _ in CHS), key=lambda c: per[(c, who)])
        lst = ev.get((peak, who))
        if not lst: continue
        lab = " · ".join(w for w, _n in lst[:3])
        o.append(t(xs[peak], yo(per[(peak, who)]) - 16, lab, 11.5, col, anc="middle", op=.95))
    v8 = per[("8", "다")]
    if v8:
        o.append(f'<circle cx="{xs["8"]:.1f}" cy="{yo(v8):.1f}" r="10" fill="none" '
                 f'stroke="{DA}" stroke-width="1.6" stroke-opacity=".85"/>')
        o.append(t(xs["8"], yo(v8) + 30, "오늘 몸을 돌려준 자리", 11, DA, anc="middle", op=.9))
    # 감정.html(12축)은 열 장 전부에 Prior·Posterior·Gap 이 있다. 갈리는 것은
    # 있다/없다가 아니라 Prior 를 언제 걸었나다 — 5~9장은 원고를 읽은 뒤에 걸었다.
    x5, x9 = xs["5"], xs["9"]
    o.append(f'<path d="M {x5:.1f} {BOT+44} L {x5:.1f} {BOT+52} L {x9:.1f} {BOT+52} '
             f'L {x9:.1f} {BOT+44}" fill="none" stroke="{NO}" stroke-width="1" stroke-opacity=".45"/>')
    o.append(t((x5 + x9) / 2, BOT + 70,
               "Prior 를 원고 읽은 뒤에 건 다섯 — 빚이 작게 나와도 정합의 증거가 아니다",
               11.5, NO, anc="middle", op=.8))
    o.append(t((x5 + x9) / 2, BOT + 88,
               "1·2·3·4·10 장은 원고보다 먼저 걸었다(반증 가능). "
               "자 = 감정.html 12축 2026-08-22 · /sbc 6축은 3·4장 둘만 돌았다",
               11, INK, anc="middle", op=.42))

    for c, name in CHS:
        o.append(t(xs[c], BOT + 26, name, 13, INK, anc="middle", op=.72))

    # ══ 판 둘 — 열 칸
    CY = BOT + 124
    o.append(t(LX, CY, "열 칸에 누가 사나 — 세의 전유가 세다로 옮겨 갔다", 18, INK, bold=True))
    live = [(n, note) for n, _s, note in CLUSTERS
            if any(prof.get((w, n), 0) for w, _ in CAST)]
    dead = [n for n, _s, _x in CLUSTERS
            if not any(prof.get((w, n), 0) for w, _ in CAST)]
    cw = (W - 2 * LX - 300) / max(len(live), 1)
    base = CY + 150
    cmx = max([prof.get((w, n), 0) for n, _x in live for w, _ in CAST] + [1])
    for g in (0, 5, 10):
        if g > cmx: continue
        y = base - (base - CY - 44) * g / cmx
        o.append(f'<line x1="{LX}" y1="{y:.1f}" x2="{LX+cw*len(live):.1f}" y2="{y:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
        o.append(t(LX - 8, y + 4, str(g), 11, INK, anc="end", op=.45))
    for i, (name, note) in enumerate(live):
        cx = LX + cw * (i + .5)
        for j, (who, col) in enumerate(CAST):
            v = prof.get((who, name), 0)
            bw, bx = cw * .22, cx + (j - 1) * cw * .25
            h = (base - CY - 44) * v / cmx
            if v:
                o.append(f'<rect x="{bx-bw/2:.1f}" y="{base-h:.1f}" width="{bw:.1f}" '
                         f'height="{max(h,2.5):.1f}" fill="{col}" rx="2"/>')
                o.append(t(bx, base - max(h, 2.5) - 6, str(v), 11.5, col, anc="middle", bold=True))
        o.append(t(cx, base + 20, name, 12, INK, anc="middle", op=.78))
        if note:
            o.append(t(cx, base + 38, note, 10.5, NO, anc="middle", op=.9))
    o.append(f'<line x1="{LX}" y1="{base}" x2="{LX+cw*len(live):.1f}" y2="{base}" '
             f'stroke="{GRID}" stroke-width="1.5"/>')
    rx2 = LX + cw * len(live) + 36
    for k, (txt, col) in enumerate([
        ("소진·물러남 — 05-02 에 세의 가장 센 칸. 지금 0.", NO),
        ("경계·의심 · 연민·고마움 — 세의 것이 세다로 갔다.", NO),
        ("장난 — 05-02 에 둘 다 0 이었는데 세에게 생겼다.", DA),
        ("0 인 칸 " + str(len(dead)) + " — " + " · ".join(dead), INK),
        ("05-02 도 0 이라 구멍이 아니라 경계다.", INK)]):
        o.append(t(rx2, CY + 46 + k * 30, txt, 12.5, col, op=.9 if col != INK else .5))

    # ══ 판 셋 — 낱말
    EY = base + 76
    o.append(t(LX, EY, "무슨 낱말이 이 수를 만들었나 — 원고에서 그대로 뽑았다", 18, INK, bold=True))
    o.append(t(LX, EY + 22, "× 는 같은 장에서 거듭 나온 횟수. 아래 낱말 말고 센 것은 없다.", 12.5, INK, op=.5))
    colw = (W - 2 * LX) / 2
    rows = []
    for name, ch, rs in blocks:
        rows.append(("H", name, bool(rs), None, None))
        for who, col in rs:
            lst = ev[(ch, who)]
            txt = " · ".join(f"{w}{chr(215)+str(c) if c > 1 else ''}" for w, c in lst[:9])
            rows.append(("R", who, col, txt, per[(ch, who)]))
    for i, r in enumerate(rows):
        cc, k = (0, i) if i < colrows else (1, i - colrows)
        x, y = LX + cc * colw, EY + 58 + k * 22
        if r[0] == "H":
            o.append(t(x, y, r[1], 13.5, HI, bold=True))
            if not r[2]:
                o.append(t(x + 72, y, "대사 없음 — 이 장의 감정은 임자가 안 적힌 1인칭 문장에 있다",
                           12, INK, op=.42))
        else:
            o.append(t(x + 20, y, r[1], 12.5, r[2], bold=True))
            o.append(t(x + 72, y, r[3], 12.5, INK, op=.82))
            o.append(t(x + colw - 30, y, str(r[4]), 12.5, r[2], anc="end", bold=True))

    H = EY + 58 + colrows * 22 + 86
    seeds = " · ".join(n for n, _s, _x in CLUSTERS)
    o.append(t(LX, H - 52, "씨앗은 손으로 지었다 — " + seeds +
               "   |   오탐 교정: 「화가 」 「화를 」 적중 14건이 전부 대화·최적화·실화·변화였다. 씨앗을 좁혔다.",
               11, INK, op=.42))
    o.append(t(LX, H - 26, "로터와 스테이터는 한 손잡이의 두 눈금이 아니다. 둘 다 있어야 돈다.",
               15, HI, op=.9))
    o.append(t(W - LX, H - 26,
               f"자 = chapters/ 전수 · 10 cluster(gcb #9 2026-05-02) · "
               f"생성기 scripts/09_rotor_stator.py · {DREW}", 11, INK, anc="end", op=.38))
    o.append("</svg>")
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="Apple SD Gothic Neo, Noto Sans CJK KR, Noto Sans KR, '
            f'Helvetica Neue, Helvetica, Arial, sans-serif">',
            f'<rect width="{W}" height="{H}" fill="{BG}"/>']
    return "\n".join(head + o)


if __name__ == "__main__":
    per, prof, ev = measure()
    open(OUT_SVG, "w", encoding="utf-8").write(build(per, prof, ev))
    subprocess.run(["rsvg-convert", "-w", str(W), OUT_SVG, "-o", PUB_PNG], check=True)
    print(f"PNG {PUB_PNG} ({os.path.getsize(PUB_PNG)/1024:.0f} kB)")
    print("장   " + "".join(f"{w:>6s}" for w, _ in CAST))
    for ch, name in CHS:
        print(f"{ch:3s} " + "".join(f"{per[(ch,w)]:6d}" for w, _ in CAST))
