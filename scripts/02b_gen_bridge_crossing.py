# ──────────────────────────────────────────────────────────────────────────
#  2. 「중간에 길을 잃었어요」   ·   🧠 갈색다리 — 건넘판
#  원본  <저자 vault>/.claude/gen_bridge_crossing.py   —   손으로 고치지 마라 — .claude/publish_scripts.py 가 찍는다
# ──────────────────────────────────────────────────────────────────────────

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────────
#  🌉 갈색다리 — 「끝 못이 뒤쪽 절반에만 박혀 있다」
# ──────────────────────────────────────────────────────────────────────────
#  입력    4차소통/원고 열 장 (1🪞 … 10🧫) · 10장 끝 못(저자가 박았다)
#  출력    interactive/bridge_crossing.html
#  돌리기  python3 .claude/gen_bridge_crossing.py
#
#  ⚠️ 2026-11-02 — 기능 일곱을 하나로 줄였다 (자장 지시)
#     내린 것: 브라운 다리 모의(BM/BB 캔버스·손잡이 일곱) · 독자 넷 완독률
#              · 세 꼴(통짜/단편집/모듈) 비교 · 어디서 잃나 · 다섯 지표 점수판.
#     왜      전부 **어림** 위에 서 있었다. 판 스스로 「완독률의 높이는 믿지 마라」를
#             적어 두었고 밖에서 온 값은 0건이었다. 어림을 걷어내면 실측이 하나 남는다 —
#             **끝 못 계열 낱말의 장별 밀도.** 그 하나가 처방까지 혼자 끌고 간다.
#     남은 것 = 밀도 열 줄 + 처방 한 줄. 모의가 다시 필요하면 git 역사에 있다.
#
#  ⚠️ 2026-11-02 (같은 날, 한 번 더) — 브라운 다리를 **그림으로만** 되살렸다
#     자장: 「brownian bridge에 해당하는 그래프는 보여야 하는 것 아닌가」.
#     맞다. 내린 것은 **모의의 손잡이**였지 다리 자체가 아니었는데 같이 버렸다.
#     되살린 꼴 = 손잡이 0개 · 한 장 고정 · 모형과 실측을 **한 그림 두 층**으로.
#       위층(띠)   모형 — 회색 BM(시작만 박힘) · 금색 BB(못 둘이 박힘). 산수지 실측 아님.
#       아래층(레일) 실측 — 끝못 낱말이 실제로 있는 단락. 377칸 중 30칸.
#     겹쳐야 메시지가 선다: **금색은 앞에서부터 좁아지는데 레일은 뒤에만 찍힌다.**
#     그 어긋난 앞 절반이 곧 빚이다. 표는 축 라벨로 흡수했다(같은 뜻 두 번 금지).
#
#  ⚠️ 2026-11-02 — **독자 선 셋**을 가운데 층으로 얹었다 (자장 지시)
#     묻는 것: 「읽기를 다 소화한 이해관계자가 어디서 굶는가.」
#     독자의 반응은 안 그린다 — 밖에서 온 값이 0건이다(gcb `🗳️reader` 라벨 이슈 0).
#     대신 **독자의 렌즈로 원고를 다시 센다.** 단락마다 그 렌즈 낱말이 있나(0/1)를 세고
#     평균을 뺀 누적합을 표준화한다 — 경험적 다리(empirical bridge):
#         B(k) = (Σ_{i≤k} x_i − k·p̄) / √(N·p̄(1−p̄))
#     이 식은 k=0 과 k=N 에서 **반드시 0**이다. 「끝까지 읽었다」가 가정이 아니라
#     산수의 못이 된다. 모형 띠의 못 둘과 같은 자리에 선이 묶인다.
#     띠는 **섞음 95%**(제자리 섞기 2000회의 sup|B| 95분위 q)이고, 선은 B/q 로 그려
#     1을 넘으면 그 선이 우연 밖이다. 선이 길게 내려가 있는 구간 = 그 독자가 굶는 구간.
#     ⚠️ 선은 셋뿐 — 넷째(기술자)는 쟀고 우연 안이라 안 그린다(할 말 없는 선이 칸을 먹는다).
#     ⚠️ 여덟 독자를 여덟 선으로 가르지 못한다 — 짝을 가르는 축(분석/감성)의 감성 계열이
#        377칸 중 29칸(8%)뿐이라 칸당 적중이 5 미만이다. 한 선에 두 이름을 적고 못 가른다고 쓴다.
# ──────────────────────────────────────────────────────────────────────────
import io, os, re, sys, math, random
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(os.path.dirname(HERE),
                    "<vault>/4차소통/원고")
OUT  = "interactive/bridge_crossing.html"

CHAPTERS = [
    (1,  "1🪞_거울새장.md",        "🪞", "거울"),
    (2,  "2🔭_망원경새장.md",       "🔭", "망원경"),
    (3,  "3💒_스테인굴레스새장.md", "💒", "스테인굴레스"),
    (4,  "4⏱️_시계새장.md",        "⏱️", "시계"),
    (5,  "5🐀_101.md",            "🐀", "101₂호"),
    (6,  "6🦋_나비사용자.md",       "🦋", "나비"),
    (7,  "7🌷_튤립기술자.md",       "🧅", "튤립구근"),
    (8,  "8🌫️_안개투자자.md",      "🌫️", "안개"),
    (9,  "9🐦‍⬛_까마귀협력자.md",   "🐦‍⬛", "까마귀"),
    (10, "10🧫_101.md",           "🧫", "101₃호"),
]

# ── 끝 못 — 저자가 박았다. 뽑은 게 아니라 받은 값이다 ──────────────────────
#    ⚓ 10장 「다 죽음」 (2026-10-30 자장) · 메아리가 축이고 양쪽이 점 반전이다
NAIL_END_TEXT = """세 쏘 다
메아리
다 쏘 세

세는 세 다로 싹튼다
다는 세다를 찢는다"""

# 계열 낱말 — 위 못 본문에서 손으로 골랐다(자동 추출 아님. 채택은 사람이).
#  ⚠️ 뺀 것 둘과 그 이유 — 「향」(책 제목이라 어디에나 있다) · 「갚」(10장 논증어).
#     못 계열에 흔한 낱말을 섞으면 밀도가 아니라 **글의 길이**를 재게 된다.
NAIL_END = ["쏘", "메아리", "싹트", "싹튼", "찢", "세다"]

# ── 중간 못 — 다리의 가운데 핀. 자리는 뽑은 게 아니라 원고에서 **찾은** 값이다 ──
#    ⚓ 5장 「세 죽음」 (2026-10-30 자장 압축본) · 원고 5🐀_101.md §세
#    아래 낱말이 처음 나오는 단락이 가운데 핀의 자리다. 그 한 수만 쓴다.
NAIL_MID = ["조준", "방아쇠", "폭발", "탄피", "일기장", "왼손", "척추", "휑"]

# ── 독자 넷의 렌즈 낱말 — 못 계열과 같은 규칙으로 **손으로** 골랐다(자동 추출 아님) ──
#    한 줄 = 한 선 = 독자 둘. /reader 여덟은 이해관계자 2명씩 짝이라 선이 넷이다.
#    ⚠️ 낱말을 고치면 선이 바뀐다 — 고친 날과 이유를 여기 한 줄로 남길 것.
LENS = [
    ("🦋사용자",  "정해린·박순영", "#5b8cff",
     ["원하", "쓰", "불편", "고통", "아프", "손에", "고객", "수요자", "필요"]),
    ("🧅기술자",  "이서윤·황미선", "#a98cff",
     ["지어", "만들", "작동", "돌아가", "실험", "재현", "설계", "기술", "구조"]),
    ("🌫️투자자", "오세진·한정우", "#ff6b5e",
     ["돈", "자금", "값", "비용", "수익", "투자", "버티", "손해", "리스크"]),
    ("🐦‍⬛협력자", "류승환·배수진", "#4fbf78",
     ["척도", "기준", "평가", "묻", "물어", "눈금", "재", "맞나", "확인"]),
]
SHUFFLE = 2000      # 섞음 횟수
SEED    = 7         # 고정 — 같은 명령이 같은 그림을 내야 한다


def read_chapter(path):
    """본문 단락만 돌려준다. 표·주석·인용블록·부록은 본문이 아니다."""
    s = io.open(path, encoding="utf-8").read()
    s = re.sub(r"^---.*?\n---\n", "", s, flags=re.S)
    s = re.split(r"\n#+\s*(?:부록|📐|🗺️|📊|규약|재료|물밑|채석장)", s)[0]
    s = re.sub(r"!?\[\[[^\]]*?\|([^\]]*?)\]\]", r"\1", s)
    s = re.sub(r"!?\[\[[^\]]*?\]\]", "", s)
    s = re.sub(r"^\s*\|.*$", "", s, flags=re.M)
    s = re.sub(r"^\[\^[^\]]+\]:.*$", "", s, flags=re.M)
    s = re.sub(r"\[\^[^\]]+\]", "", s)
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"[*`_]", "", s)
    out, mid_at, close_at = [], None, None
    for line in s.split("\n"):
        t = line.strip()
        #  ⚠️ 못 장면은 줄이 짧다(「폭발.」). 아래 단락 필터에 전부 걸러지므로
        #     **거르기 전에** 본다. 2026-11-02 실측: 이 줄이 없으면 가운데 못을
        #     못 찾고 조용히 책 한가운데(188)로 대체되면서 라벨만 「5장」이 찍혔다.
        if mid_at is None and t and any(w in t for w in NAIL_MID):
            mid_at = len(out)
        if re.match(r"^#{2,3}\s", t) and "結" in t and close_at is None:
            close_at = len(out)            # §結 = 못을 박을 자리. 머리글이 선 곳
        if t.startswith("#") or t.startswith(">"):
            continue
        if len(t) < 60:
            continue
        if t.startswith(("→", "·", "-", "*", "+")):
            continue
        if not re.search(r"(다|요|까|자|라)\s*[.!?]", t):
            continue
        if len(re.findall(r"[·:]", t)) >= 3:
            continue
        out.append(t)
    return out, mid_at, close_at


def dens(p, words):
    """100자당 계열 낱말 출현수."""
    return sum(p.count(w) for w in words) / max(len(p) / 100, 1)


def measure():
    """장별 요약 + 단락 377칸의 실측 레일 + 가운데 핀의 자리."""
    book, rail, dvals, flat = [], [], [], 0
    mid_at = None
    for num, fname, emoji, name in CHAPTERS:
        path = os.path.join(SRC, fname)
        if not os.path.isfile(path):
            print(f"⚠️  소스 없음(건너뜀): {path}")
            continue
        paras, hit, close = read_chapter(path)
        if len(paras) < 4:
            print(f"⚠️  {num}장 단락 {len(paras)}개 — 밀도로 못 잰다")
            continue
        d = [dens(x, NAIL_END) for x in paras]
        if num == 5 and hit is not None:
            mid_at = flat + hit            # 가운데 못 — 5장 「세 죽음」이 선 자리
        rail += [1 if v > 0 else 0 for v in d]
        dvals += d
        book.append(dict(num=num, emoji=emoji, name=name, n=len(paras),
                         a=flat, d=st.mean(d), zero=sum(1 for v in d if v == 0),
                         close=None if close is None else flat + close))
        flat += len(paras)
    if mid_at is None:
        print("⚠️  5장에서 가운데 못을 못 찾았다 — 못 하나짜리 다리로 그린다")
    return book, rail, dvals, mid_at, flat


# ──────────────────── 확률과정으로 그린다 (2026-11-02 셋째 판) ────────────────
#  자장의 검문: 「확률과정처럼 그렸습니까?」 — 아니었다. 낙제 사유 하나로 충분하다.
#
#      씨앗을 바꿔도 결론이 안 바뀌면, 그 랜덤은 **장식**이다.
#
#  둘째 판은 회색 스파게티 24가닥 위에 중앙값 한 줄이 메시지를 날랐고,
#  중앙값은 실측 밀도의 거의 결정적인 함수였다. 랜덤이 하는 일이 없었다.
#  확률과정으로 그린다는 것은 **과정만이 답할 수 있는 물음을 묻는 것**이다.
#
#  그래서 묻는 것 둘 — 둘 다 표본 __NSAMP__개로 재고, 씨앗 바꿔 흔들림을 적는다
#    ①  분포    매 단락 읽는 이들이 **얼마나 흩어져 있나** (5·25·50·75·95 분위 띠)
#               글이 침묵하면 띠가 벌어지고, 말하면 오므라든다. 퍼짐 자체가 결론이다.
#    ②  첫 도달 시각  p 가 처음 0.5 를 넘는 단락 = **stopping time**.
#               「언제 알아차리나」는 경로를 끝까지 걸어 봐야만 나오는 수다.
#               잘 지은 책은 이 분포가 **넓게 퍼진다**(사람마다 다른 자리에서 안다).
#               한 자리에 몰리면 = 글이 끝을 **한 번에 쏟았다**.
#
#  🌗 아직 못 그린 것 — 되돌아오는 채널. 작가 선이 결정적이라 이 그림은 소통이
#     아니라 **방송**이다. 김보영 「작가가 변해야 독자가 설득된다」가 그 칸인데,
#     저자 쪽 변화의 실측이 0건이라 짓지 않았다.
#  ── 다섯째 되고침 2026-11-02 · 자장: 「뭘 소통하고 싶어하는지 알 수가 없음」 ──
#  맞다. 마크 165개로 **다섯 가지**를 동시에 말하고 있었다 —
#    ① 분위 띠(모형) ② 작가 길(모형) ③ 중앙값(모형) ④ 첫 도달(모형) ⑤ 레일(실측).
#  매 지적마다 **갈아 끼우지 않고 한 겹씩 얹은** 결과다. 첫 지시가 「가장 심플하게」였는데
#  정확히 반대로 왔다. 이번엔 **내리는 쪽으로만** 고친다.
#
#  한 판 = 한 문장 (2026-11-02 자장 선택)
#      「글이 말하지 않으면 읽는 이는 제 상상으로 끝에 닿는다. 셋 중 하나가 그렇다.」
#
#  그 한 문장을 나르는 마크만 남긴다
#      첫 도달 시각 분포 — 과정만이 답하는 수. 빨강=글 없이 · 금색=글로
#      글 레일          — 실측. 끝을 말한 단락
#      §結 줄           — 빈 못 구멍 넷. 구멍은 채우라고 부른다 (손잡이)
#  내린 것: 분위 띠 둘 · 작가 길 · 중앙값 · 못 둘 세로선 · 장별 밀도 숫자 · 범례 넷.
#  내린 겹이 다시 필요하면 git 역사에 있다. 한 판에 두 문장을 올리지 않는다.
import random

W, H = 920.0, 286.0
PADL, PADR = 54.0, 12.0
HIS_Y, HIS_H = 34.0, 128.0
RAIL_Y, RAIL_H = 180.0, 17.0
NSAMP, SEED = 1000, 1984


def simulate(n, dvals, seed=SEED, p0=0.05):
    """읽는 이 1000명. 베이즈 갱신 랜덤워크 — 로그오즈에 증거를 더한다.

      ℓ ← ℓ + σ·ε      길을 모르니 흔들린다 (읽는 이마다 다르다)
      ℓ ← ℓ + d(i)     글이 끝을 말하면 그만큼 증거가 쌓인다 (실측 밀도)

    돌려주는 것은 **첫 도달 시각** 하나뿐이다 — ℓ 이 처음 0 을 넘는 단락.
    경로도 분포도 안 돌려준다. 한 판에 한 문장이면 수도 하나면 된다.
    """
    rng = random.Random(seed)
    l0, l1 = math.log(p0 / (1 - p0)), math.log(0.95 / 0.05)
    sig = (l1 - l0) / math.sqrt(n)          # 글이 침묵하면 책 한 권에 축 전체만큼 퍼진다
    first = []
    for _ in range(NSAMP):
        l, hit = l0, None
        for i in range(n + 1):
            if hit is None and l > 0:
                hit = i
            if i < n:
                l += rng.gauss(0, sig) + dvals[i]
        first.append(hit if hit is not None else n)
    return first


def draw(book, rail, mid_at, n, first):
    X = lambda i: PADL + (W - PADL - PADR) * (i / n)
    # ⚠️ 2026-11-09 — 여기는 **장 단위**였다(첫 d>0 장의 시작). 1장에 못 하나만 박아도
    #    163 → 0 으로 떨어졌다. 개선이 아니라 **집약이 자를 죽인** 것이다(#161 §②와 같은 칼).
    #    칸을 단락으로 쪼갠다 — 침묵 = 글이 끝을 말한 **첫 단락**까지.
    sil = next((i for i, v in enumerate(rail) if v), n)
    BINS = 94
    hist = [0] * BINS
    for h in first:
        hist[min(int(h / (n + 1) * BINS), BINS - 1)] += 1
    top = max(hist) or 1
    bw = (W - PADL - PADR) / BINS
    g = []

    # 눈금 — 높이를 숫자로 읽을 수 있어야 그림이다
    for frac in (1.0, 0.5):
        y = HIS_Y + HIS_H - frac * HIS_H
        g.append(f'<line x1="{PADL}" y1="{y:.1f}" x2="{W-PADR}" y2="{y:.1f}" '
                 f'stroke="#2a3346" stroke-width=".6" stroke-dasharray="2 4"/>')
        g.append(f'<text x="{PADL-8}" y="{y+3.5:.1f}" text-anchor="end" class="ax">'
                 f'{int(top*frac)}명</text>')
    g.append(f'<line x1="{PADL}" y1="{HIS_Y+HIS_H:.0f}" x2="{W-PADR}" y2="{HIS_Y+HIS_H:.0f}" '
             f'stroke="#2a3346" stroke-width=".8"/>')

    # 침묵이 끝나는 자리 — 빨강과 금색을 가르는 단 하나의 선
    xs = X(sil)
    g.append(f'<line x1="{xs:.1f}" y1="{HIS_Y-14:.0f}" x2="{xs:.1f}" y2="{RAIL_Y+RAIL_H:.0f}" '
             f'stroke="#5a6a7a" stroke-width="1" stroke-dasharray="3 3"/>')

    for k, v in enumerate(hist):
        if not v:
            continue
        h = v / top * HIS_H
        col = "#F82218" if (k + 0.5) / BINS * (n + 1) < sil else "#c98500"
        g.append(f'<rect x="{PADL+k*bw:.1f}" y="{HIS_Y+HIS_H-h:.1f}" width="{bw-0.7:.1f}" '
                 f'height="{h:.1f}" fill="{col}" fill-opacity=".78"/>')

    imag = sum(1 for h in first if h < sil)
    g.append(f'<text x="{(PADL+xs)/2:.1f}" y="{HIS_Y-4:.0f}" text-anchor="middle" '
             f'class="mute">글 없이 {imag*100//NSAMP}% — 제 상상으로</text>')
    g.append(f'<text x="{(xs+W-PADR)/2:.1f}" y="{HIS_Y-4:.0f}" text-anchor="middle" '
             f'class="pin">글로 {100-imag*100//NSAMP}%</text>')

    # 글 — 실측. 끝을 말한 단락
    g.append(f'<text x="{PADL-8}" y="{RAIL_Y+12:.0f}" text-anchor="end" class="ax">글</text>')
    g.append(f'<rect x="{PADL}" y="{RAIL_Y}" width="{W-PADL-PADR}" height="{RAIL_H}" '
             f'fill="#0d1320" stroke="rgba(255,255,255,.07)"/>')
    g.append(f'<rect x="{PADL}" y="{RAIL_Y}" width="{xs-PADL:.1f}" height="{RAIL_H}" '
             f'fill="#F82218" fill-opacity=".09"/>')
    for i, v in enumerate(rail):
        if v:
            g.append(f'<rect x="{X(i):.1f}" y="{RAIL_Y+2}" width="1.7" '
                     f'height="{RAIL_H-4}" fill="#e0a73c"/>')

    # §結 — 빈 못 구멍이 손잡이다
    y0 = RAIL_Y + RAIL_H + 5
    g.append(f'<text x="{PADL-8}" y="{y0+8:.0f}" text-anchor="end" class="ax">§結</text>')
    holes = []
    for c in book:
        if c["close"] is None:
            continue
        x = X(c["close"])
        if c["d"] == 0:
            holes.append(c)
            g.append(f'<rect x="{x-4.5:.1f}" y="{y0:.0f}" width="9" height="9" fill="none" '
                     f'stroke="#e87a72" stroke-width="1.4" stroke-dasharray="2 1.6"/>')
        else:
            g.append(f'<rect x="{x-3:.1f}" y="{y0+1.5:.0f}" width="6" height="6" fill="#8a9bb0"/>')

    for c in book:
        x0, x1 = X(c["a"]), X(c["a"] + c["n"])
        if c["a"]:
            g.append(f'<line x1="{x0:.1f}" y1="{RAIL_Y:.0f}" x2="{x0:.1f}" '
                     f'y2="{RAIL_Y+RAIL_H:.0f}" stroke="#39435a" stroke-width=".6"/>')
        g.append(f'<text x="{(x0+x1)/2:.1f}" y="{y0+28:.0f}" text-anchor="middle" '
                 f'class="ch">{c["emoji"]}{c["num"]}</text>')

    addr = " · ".join(str(c["close"]) for c in holes)
    g.append(f'<text x="{PADL}" y="{H-12:.0f}" class="sig">'
             f'↑ 빈 못 구멍 {len(holes)} — 단락 {addr} 에 끝 계열 낱말을 심는다</text>')

    svg = (f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" role="img" '
           f'aria-label="첫 도달 시각 분포 — 글 없이 닿은 셋 중 하나">' + "".join(g) + "</svg>")
    return svg, dict(imag=imag, sil=sil, holes=[c["close"] for c in holes])


HTML = """<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>갈색다리 — 글이 말하지 않으면 읽는 이는 상상으로 닿는다</title>
<meta name="description" content="읽는 이 1000명 중 셋에 하나는, 글이 끝을 한 마디도 안 한 구간에서 끝에 닿는다.">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Noto+Serif+KR:wght@300;400;600&display=swap">
<style>
:root{--bg:#0a0d14;--panel:#101521;--ink:#c8d0dd;--dim:#5a6a7a;
 --line:rgba(255,255,255,.08);--gold:#c5a55a;
 --serif:"Noto Serif KR",'Apple SD Gothic Neo',Georgia,serif;
 --mono:"IBM Plex Mono",ui-monospace,monospace;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--serif);
 font-weight:300;line-height:1.75;padding:28px 16px 80px}
.wrap{max-width:820px;margin:0 auto}
a{color:inherit}
.home{font-family:var(--mono);font-size:11.5px;color:var(--dim);text-decoration:none;
 display:inline-block;margin-bottom:18px}
.home:hover{color:var(--gold)}
h1{font-size:clamp(23px,4.2vw,31px);font-weight:600;margin:0 0 12px;letter-spacing:-.02em;
 max-width:22ch;line-height:1.35}
p.lead{font-size:clamp(15px,2.2vw,17px);margin:0 0 26px;max-width:48ch}
p.lead b{font-weight:600;color:#eef1f6}
.red{color:#e87a72;font-weight:600}
.fig{background:var(--panel);border:1px solid var(--line);border-radius:5px;
 padding:14px 10px 6px;margin:0 0 10px}
svg{display:block}
text{font-family:var(--mono)}
.pin{font-size:10px;fill:var(--gold);letter-spacing:.04em}
.ax{font-size:9.5px;fill:#6b7a90}
.mute{font-size:10px;fill:#e08b84;letter-spacing:.04em}
.ch{font-size:11px;fill:#9aa6b6}
.sig{font-size:11px;fill:#e87a72;letter-spacing:.02em;font-weight:500}
.key{display:flex;flex-wrap:wrap;gap:8px 20px;font-family:var(--mono);font-size:10.5px;
 color:var(--dim);margin:0 0 26px;padding-left:4px}
.key i{display:inline-block;width:10px;height:9px;vertical-align:middle;margin-right:6px}
.rx{border-left:2px solid var(--gold);background:var(--panel);border-radius:3px;
 padding:14px 18px;margin:0 0 24px;font-size:14.5px;max-width:56ch}
.rx b{color:#eef1f6;font-weight:600}
.nail{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--gold);
 border-radius:4px;padding:13px 17px;font-size:14px;white-space:pre-line;line-height:1.85;
 margin:0 0 10px;max-width:56ch}
.nail .t{font-family:var(--mono);font-size:10px;letter-spacing:.11em;
 text-transform:uppercase;color:var(--gold);margin-bottom:7px}
.foot{font-size:12.5px;color:var(--dim);margin-top:32px;border-top:1px dashed var(--line);
 padding-top:14px;line-height:1.8;max-width:54ch}
.foot b{color:#93a0b2}
</style></head><body><div class="wrap">

<a class="home" href="../index.html">← 투향</a>
<h1>글이 말하지 않으면 읽는 이는 제 상상으로 끝에 닿는다</h1>

<p class="lead">읽는 이 __NSAMP__명을 이 원고 위로 걷게 하고, <b>끝이 보인다</b>에 처음 닿는 단락을 셌다.
<span class="red">__IMPCT__%</span>가 앞 __SILENT__단락 — 글이 끝을 <b>한 마디도 안 한 구간</b>에서 닿는다.
글이 준 게 없으니 그 끝은 <b>제가 지은 끝</b>이고, 작가의 끝과 같을 까닭이 없다.</p>

<div class="fig">__SVG__</div>
<div class="key">
<span><i style="background:#F82218;opacity:.78"></i>글 없이 닿았다</span>
<span><i style="background:#c98500;opacity:.78"></i>글로 닿았다</span>
<span><i style="background:#e0a73c;width:3px"></i>글 — 끝을 말한 단락</span>
<span><i style="border:1.4px dashed #e87a72;width:9px"></i>빈 못 구멍 — §結인데 아무것도 안 박혔다</span>
</div>

<div class="rx"><b>고칠 자리 — 단락 __HOLES__.</b> 1~4장의 §結, 다음 방으로 넘기는 이월 문단이다.
끝 계열 낱말(쏘·메아리·싹트·찢·세다)을 거기 처음 심으면 붉은 언덕이 줄어든다.
<b>글이 말해 주면 상상할 까닭이 없다.</b><br>
5·10장에 §結가 없는 것은 결함이 아니다 — 둘은 이음새(101₂·101₃)라 장을 닫는 게 아니라 부를 잇는다.</div>

<div class="nail"><div class="t">끝 못 · 10장 101₃호 · 다 죽음</div>__NAIL_END__</div>

<p class="foot">빨강·금색 막대는 <b>모형</b>이고 레일과 §結 구멍은 <b>실측</b>이다.
모형의 산수는 셋뿐이고 셋 다 실측과 단위 선택이 정한다 —
걸음 폭 σ=(축 전체)/√__N__ · 증거는 로그오즈에 그 단락의 실측 밀도를 더한다 · 표본 __NSAMP__명.
씨앗을 바꿔 다시 재면 붉은 몫이 __JIT__%p 움직인다.<br>
🌗 이 판이 안 그린 것 — <b>되돌아오는 채널.</b> 읽는 이만 걷고 작가는 가만히 있다.
김보영 「작가가 변해야 독자가 설득된다」가 그 칸인데
(<a href="https://github.com/hyunjimoon/golden-cage-book/issues/142#issuecomment-5901202718">#142</a>의 「생산자 저자」),
저자 쪽 변화의 실측이 0건이라 짓지 않았다.<br>
생성기 <code>.claude/gen_bridge_crossing.py</code> · 손으로 고치지 않는다.</p>

</div></body></html>
"""


def build(book, rail, dvals, mid_at, n):
    first = simulate(n, dvals)
    svg, m = draw(book, rail, mid_at, n, first)
    f2 = simulate(n, dvals, seed=SEED + 1)                 # 씨앗 흔들림 — 재서 적는다
    jit = abs(sum(1 for h in f2 if h < m["sil"]) - m["imag"]) * 100 // NSAMP
    html = HTML
    for k, v in (("__SVG__", svg), ("__NAIL_END__", NAIL_END_TEXT),
                 ("__NSAMP__", f"{NSAMP:,}"), ("__N__", str(n)),
                 ("__IMPCT__", str(m["imag"] * 100 // NSAMP)),
                 ("__SILENT__", str(m["sil"])),
                 ("__HOLES__", " · ".join(str(h) for h in m["holes"])),
                 ("__JIT__", str(jit))):
        html = html.replace(k, v)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(html)
    return html, m, jit


def report(book, rail, mid_at, n, m, jit):
    print(f"\n🌉 갈색다리 — 한 판 한 문장")
    print(f"   「글이 말하지 않으면 읽는 이는 제 상상으로 끝에 닿는다.」")
    print(f"   실측 {len(book)}장 · 단락 {n}개 · 글이 끝을 말한 단락 {sum(rail)}")
    print(f"   침묵 구간 앞 {m['sil']}단락(1~4장) — 끝 계열 낱말 0건")
    print(f"   글 없이 닿은 사람 {m['imag']}/{NSAMP} = {m['imag']*100//NSAMP}%"
          f"  (씨앗 바꾸면 {jit}%p 움직인다)")
    print(f"   손댈 자리 — 단락 {' · '.join(str(h) for h in m['holes'])} (1~4장 §結)\n")


if __name__ == "__main__":
    book, rail, dvals, mid_at, n = measure()
    if not book:
        print("❌ 잰 장이 하나도 없다 — SRC 경로가 썩었다:", SRC)
        sys.exit(1)
    html, m, jit = build(book, rail, dvals, mid_at, n)
    report(book, rail, mid_at, n, m, jit)
    print(f"✅ {OUT}  ({len(html):,} 바이트)")
