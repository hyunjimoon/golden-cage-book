#!/usr/bin/env python3
# 야성미 측정 코어 — 측정에 관한 모든 것이 여기 한 곳에 있다 (SSOT).
# 그리는 쪽(yaseong_map_10jang · yaseong_compass · yaseong_orbital)은 import만 하고
# 수식을 다시 만들지 않는다.
#
# ── 구조 ────────────────────────────────────────────────────────────
# 0 전처리   body() 본문 추출 · sentences() 문장 분할
# 1 원시량   네 층  x₁ 길이 · x₂ 어휘 희귀도 · x₃ 표기 전환 · x₄ 화행
# 2 표준화   z  = (x − 장평균)   / 장표준편차     ← 장 안의 리듬
#            zg = (x − 전체평균) / 전체표준편차   ← 장 사이의 온도
# 3 합성     W = max_k |z_k|  (L∞)  ·  터진 층 = argmax
# 4 파생     M_total · density · stats
#
# ── 표준화 둘을 함께 내는 이유 (2026-08-20 실측) ──────────────────────
# 장별 z는 각 장의 평균 0·표준편차 1을 강제하므로 장 사이의 온도차를 지운다.
# 실측: 밀도 변동계수 장별 4.9% → 전역 19.7%(4배). 원시 평균도 크게 벌어진다
#       (글자수 23.8~46.8 · 표기율 0.022~0.076 · 화행 0.03~0.18).
# 그래서 어느 하나만 쓰면 절반만 본다. 두 벌을 항상 같이 낸다.
#
# ── leave-one-out 코퍼스는 기각(2026-08-20) ─────────────────────────
# 자기참조 편향을 지우려 했으나 실측 결과 이동이 전 장 +0.69~+0.82로 거의 균일했다.
# z는 평행이동에 불변이라 장별 z에는 이득이 없고, 장마다 코퍼스가 달라져
# 전역 비교의 공통 척도를 깨뜨린다. 코퍼스는 대상 전체 하나로 유지한다.
import io, re, math
from collections import Counter
import statistics as st

LAYER = ["길이", "어휘", "표기", "화행"]
LCOL  = {"길이": "#2D5FA8", "어휘": "#B0821F", "표기": "#C8102E", "화행": "#1B1B1E"}
LOCAL, GLOBAL = "peak", "peak_g"          # 파생 지표에 넘기는 키

# 물밑(스캐폴딩) 절 — 이 헤더가 나오면 같거나 더 높은 레벨 헤더가 올 때까지 버린다
FUEL = re.compile(
    r"(Prior|채석장|제시\s*규칙|작업\s*노트|수식\s*물밑|인용\s*장부|재구성\s*매핑|"
    r"분위기|스캐폴딩\s*강등|수치검사|미해결|물밑|부록)")

# ── 0 전처리 ────────────────────────────────────────────────────────
def body(path):
    s = io.open(path, encoding="utf-8").read()
    s = re.sub(r"^---.*?\n---\n", "", s, flags=re.S)             # frontmatter
    m = re.search(r"^# ", s, flags=re.M)                         # 제목 앞 파일 포인터 줄
    if m: s = s[m.start():]

    keep, drop_at = [], None                                     # 절 단위로 물밑 층 제거
    for line in s.split("\n"):
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            lvl, title = len(m.group(1)), m.group(2)
            if drop_at is not None and lvl <= drop_at:
                drop_at = None
            if drop_at is None and FUEL.search(title):
                drop_at = lvl
            continue                                             # 헤더 자체는 본문 아님
        if drop_at is None:
            keep.append(line)
    s = "\n".join(keep)

    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)                   # 이미지
    s = re.sub(r"!?\[\[[^\]]*?\|([^\]]*?)\]\]", r"\1", s)        # 위키링크 → 표시텍스트
    s = re.sub(r"!?\[\[[^\]]*?\]\]", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)               # 일반 링크
    s = re.sub(r"^\s*\|.*$", "", s, flags=re.M)                  # 표
    s = re.sub(r"^\s*>.*$", "", s, flags=re.M)                   # 인용 블록
    s = re.sub(r"^\s*[-*_]{3,}\s*$", "", s, flags=re.M)          # 구분선
    s = re.sub(r"^\[(\d+)\]\s*", "", s, flags=re.M)              # 단락 번호는 지우고 내용 보존
    s = re.sub(r"\[\^[^\]]+\][^\n]*", "", s)                     # 각주
    s = re.sub(r"https?://\S+", "", s)
    s = s.replace("．", ". ").replace("，", ", ")
    s = re.sub(r"[*`_]", "", s)
    return s

def sentences(t):
    out = []
    for para in [p for p in t.split("\n") if p.strip()]:
        for s in re.split(r"(?<=[.?!])\s+", para.strip()):
            s = s.strip().lstrip("-–— ").strip()
            if 3 <= len(s) <= 300 and re.search(r"[가-힣]", s):
                out.append(s)
    return out

# ── 1 원시량 · 2 표준화 · 3 합성 ─────────────────────────────────────
def _syl_bigrams(s):
    syl = re.sub(r"[^가-힣]", "", s)
    return [syl[i:i+2] for i in range(len(syl)-1)]

def _z(v):
    m, sd = st.mean(v), st.pstdev(v) or 1e-9
    return [(x - m) / sd for x in v]

NOTATION = re.compile(r"[一-鿿A-Za-z0-9\"'“”‘’()（）—–]")

def load(base, chapters):
    """chapters = [(파일명, 표시이름, 부)] → (docs, measure).
       measure(파일명) → rows. 파일명으로 부르는 이유: 전역 표준화를 코어가 안다.
       어휘 코퍼스는 이 묶음 전체 하나(외부 코퍼스 금지·LOO 기각)."""
    docs, big = {}, Counter()
    for f, name, part in chapters:
        S = sentences(body(base + f))
        docs[f] = (name, part, S)
        for s in S:
            big.update(_syl_bigrams(s))
    NB = sum(big.values()) or 1

    def lex(s):
        # 음절 bigram 3개 미만(숫자·기호·한두 글자)은 희귀도를 못 잰다 → None,
        # 뒤에서 그 장의 평균으로 채워 z≈0. 안 그러면 "5초."가 −8σ 봉우리로 잡힌다.
        gs = _syl_bigrams(s)
        if len(gs) < 3: return None
        return sum(-math.log2((big[g] + 0.5) / (NB + 0.5)) for g in gs) / len(gs)

    def raw(f):
        S = docs[f][2]
        L1 = [len(s) for s in S]                                        # ① 길이
        r  = [lex(s) for s in S]                                        # ② 어휘 희귀도
        ok = [v for v in r if v is not None]
        mu = st.mean(ok) if ok else 0.0
        L2 = [mu if v is None else v for v in r]
        L3 = [len(NOTATION.findall(s)) / max(len(s), 1) for s in S]     # ③ 표기 전환
        L4 = [(2.0 if re.search(r"[?？]", s) else 0)                     # ④ 화행
              + (1.0 if re.search(r"[!！]", s) else 0)
              + (1.0 if re.search(r"(자|라|까|나)[.?!]$", s) else 0) for s in S]
        return [L1, L2, L3, L4]

    RAW = {f: raw(f) for f, _, _ in chapters}
    pool = [[], [], [], []]
    for f in RAW:
        for k in range(4): pool[k] += RAW[f][k]
    GM = [st.mean(pool[k]) for k in range(4)]
    GS = [st.pstdev(pool[k]) or 1e-9 for k in range(4)]

    def measure(f):
        X, S = RAW[f], docs[f][2]
        ZL = [_z(X[k]) for k in range(4)]                                # 장 안의 리듬
        ZG = [[(v - GM[k]) / GS[k] for v in X[k]] for k in range(4)]     # 장 사이의 온도
        rows = []
        for i, s in enumerate(S):
            zl = [ZL[k][i] for k in range(4)]
            zg = [ZG[k][i] for k in range(4)]
            kl = max(range(4), key=lambda j: abs(zl[j]))
            kg = max(range(4), key=lambda j: abs(zg[j]))
            rows.append({"s": s,
                         "x": [X[k][i] for k in range(4)],
                         "z": zl,  "peak": abs(zl[kl]), "layer": LAYER[kl],
                         "sign": 1 if zl[kl] > 0 else -1,
                         "zg": zg, "peak_g": abs(zg[kg]), "layer_g": LAYER[kg],
                         "sign_g": 1 if zg[kg] > 0 else -1})
        return rows

    return docs, measure

# ── 4 파생 지표 (여기가 유일한 정의. 그리는 쪽에서 다시 만들지 말 것) ──
def _lkey(key):
    return "layer_g" if key == GLOBAL else "layer"

def M_total(rows, key=LOCAL):
    """누적 놀람 ⟨M⟩ 대용 = Σ max(W − 1σ, 0). 1σ 아래는 눌러 평지를 버린다."""
    return sum(max(r[key] - 1.0, 0) for r in rows)

def density(rows, key=LOCAL):
    """문장 하나가 미는 힘 = ⟨M⟩ / n."""
    return M_total(rows, key) / max(len(rows), 1)

def peak_idx(rows, key=LOCAL, thr=1.5):
    return [i for i, r in enumerate(rows) if r[key] >= thr]

def rhythm(rows, key=LOCAL, thr=1.5):
    """봉우리가 고르게 서는가, 몰리는가 — 시계열 성질 (2026-08-22 추가).

    범례는 오래전부터 '리듬 / 과열 / 무기명'을 약속해 왔는데 정작 그것을 가르는 값을
    재지 않고 봉우리 '개수'만 셌다. 개수는 배치를 모른다. 배치를 재는 표준 두 값:

      CV = 간격의 표준편차 / 평균          (포아송이면 1)
      B  = (σ − μ) / (σ + μ)  ∈ [−1, 1]    Goh & Barabási 2008, Nature Physics 4, 118
           B < 0 규칙적(리듬) · B ≈ 0 무작위 · B > 0 몰림(버스트)
      ρ₁ = 야성지수 시계열의 1차 자기상관   (튄 다음 또 튀는가)

    B를 쓰는 이유: CV는 봉우리가 적을 때 불안정하고 상한이 없어 장끼리 비교가 어렵다.
    B는 [−1,1]로 유계라 길이가 다른 장을 나란히 놓을 수 있다."""
    idx = peak_idx(rows, key, thr)
    iv = [b - a for a, b in zip(idx, idx[1:])]
    out = {"npeak": len(idx), "CV": None, "B": None, "rho": None}
    if len(iv) >= 3:
        m, sd = st.mean(iv), st.pstdev(iv)
        out["CV"] = sd / m if m else None
        out["B"] = (sd - m) / (sd + m) if (sd + m) else None
    v = [r[key] for r in rows]
    if len(v) >= 3:
        mu = st.mean(v); d = [x - mu for x in v]
        den = sum(x * x for x in d) or 1e-9
        out["rho"] = sum(d[i] * d[i+1] for i in range(len(d)-1)) / den
    return out

def verdict(B):
    """⚠️ 눈금이 안 맞는다 (2026-10-11 실측). 그대로 두되 새 글에서는 쓰지 마라.

    문턱 −0.05/+0.15 은 「B=0 이 무작위」를 가정한다. 아니다 — 봉우리가 촘촘하면
    간격이 짧아 σ<μ 가 되어 **섞은 순서도 B가 음수로 나온다.** 투향 10장에서
    문장을 300번씩 섞어 재니 섞은 B 평균이 **−0.08 ~ −0.12**였다. 즉 이 문턱은
    바탕값을 신호로 읽는다. 이 자로 「리듬 3장」이 나왔지만 영가설을 대면 0장이다.
    → 대신 `rhythm_null()` 을 쓴다. 지우지 않는 이유 = 옛 산출물의 숫자가
      어느 자로 나온 것인지 다음 사람이 알아야 한다."""
    if B is None: return "―"
    return "몰림" if B > 0.15 else ("리듬" if B < -0.05 else "무작위")

def rhythm_null(rows, key=LOCAL, thr=1.5, n=300, seed=7):
    """B를 **섞은 순서와 견주어** 판정한다 (2026-10-11 신설).

    왜: B의 바탕값이 0이 아니다(위 verdict 참조). 같은 문장들을 순서만 섞으면
    리듬은 사라지지만 봉우리 개수·크기는 그대로다 — 그래서 섞음 분포가
    「이 장의 봉우리 밀도에서 우연히 나올 B」의 올바른 영가설이다.

    반환: B · 섞음 평균 · 95% 구간 · 백분위 · 판정
      판정은 구간 **밖**일 때만 「리듬」(아래) 또는 「몰림」(위). 안이면 「우연」.
    """
    import random as _rd
    real = rhythm(rows, key, thr)["B"]
    if real is None:
        return {"B": None, "mu": None, "lo": None, "hi": None, "pct": None, "call": "―"}
    rd = _rd.Random(seed)
    sh = []
    for _ in range(n):
        q = list(rows); rd.shuffle(q)
        b = rhythm(q, key, thr)["B"]
        if b is not None: sh.append(b)
    if len(sh) < 20:
        return {"B": real, "mu": None, "lo": None, "hi": None, "pct": None, "call": "―"}
    sh.sort()
    lo, hi = sh[int(.025 * len(sh))], sh[int(.975 * len(sh))]
    pct = sum(1 for b in sh if b < real) / len(sh)
    call = "리듬" if real < lo else ("몰림" if real > hi else "우연")
    return {"B": real, "mu": st.mean(sh), "lo": lo, "hi": hi, "pct": pct, "call": call}

def stats(rows, key=LOCAL):
    pk = [r for r in rows if r[key] >= 1.5]
    return {"n": len(rows),
            "mean": st.mean(r[key] for r in rows) if rows else 0.0,
            "peaks": len(pk),
            "flat": sum(1 for r in rows if r[key] < 0.7) / max(len(rows), 1),
            "layers": Counter(r[_lkey(key)] for r in pk),
            "M": M_total(rows, key),
            "density": density(rows, key),
            **rhythm(rows, key)}

# ── 그리기 공통 ──────────────────────────────────────────────────────
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def heat(v):           # 야성지수 → 색 농도 (크림 → 진홍)
    a = max(0.0, min(1.0, v / 2.5))
    return f"rgba(200,16,46,{0.08 + 0.82*a:.2f})"

def heat_on(v, hexcol, lo=0.10, hi=0.92):
    """짝색 **위에** 농도로 야성을 얹는다 — 색상(hue)=짝 · 농도(value)=야성.

    heat() 는 색이 빨강으로 고정이라 판 전체가 한 색이 된다. 그러면 「색 = 짝」이라는
    규약(🧲CLAUDE.md §1 짝색 5)을 그림이 못 지키고, 더 나쁘게는 고정 빨강이
    짝색 빨강(3↔8 설득·손익)과 같은 색이 되어 한 색이 두 뜻을 진다.
    heat_on 은 한 자국이 두 값을 지되 색 체계는 하나로 유지한다."""
    a = max(0.0, min(1.0, v / 2.5))
    h = hexcol.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{lo + (hi-lo)*a:.2f})"
