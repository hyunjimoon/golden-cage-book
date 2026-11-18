#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────────
#  10. 「당신 글이랑 이 책이랑 따로 노는데요」
#      두 무늬 겹치기 — 이 파일은 **자(尺)**다. 그림은 gen_converge_ladder.py 하나뿐
# ──────────────────────────────────────────────────────────────────────────
#  원본    tolzul/.claude/gen_style_converge.py — 이 사본은 공개 저장소에서 돌게 경로만 바꿨다
#  입력    원고 10장 + golden-cage-book 이슈 글(자장 계정) 월별 7묶음
#  출력    숫자만 (stdout). 그림은 .claude/gen_converge_ladder.py 가 그린다
#  실측    옛 눈금으로는 두 판이 겹쳤다(제품 30.4% · 과정 30.1%). 같은 눈금에 올리니 갈라졌다
#  돌리기  MAP_CACHE=1 python3 .claude/gen_style_converge.py   (숫자만 보고 싶을 때)
# ──────────────────────────────────────────────────────────────────────────
#  이 gist 는 사본이다. 고칠 일이 있으면 원본을 고친다 — 생성물이 아니라 생성기를.
# ──────────────────────────────────────────────────────────────────────────
"""겹침이 발견인지 눈금이 만든 것인지 가른다.

■ 고친 것 — 옛 과정지도(`gen_process_compass.py`)의 결함 넷

  ① 눈금이 각자 것이었다 (가장 큰 것)
     yaseong_core 는 자를 **두 벌** 낸다. `peak` = 그 글 안에서만 잰 z,
     `peak_g` = 코퍼스 전체를 하나로 놓고 잰 z. 두 판 모두 `peak` 만 썼다.
     글마다 제 평균·제 표준편차로 나누면 **봉우리 비율은 분포 모양만 같으면 저절로
     같아진다.** 한국어 산문 둘은 모양이 비슷하다 → 28~33%가 양쪽에서 나온다.
     겹침이 글에서 온 게 아니라 **나눗셈에서 왔다.**
     고침 — 원고와 이슈를 **한 묶음으로 load** 해 GM·GS 를 공유하고 `peak_g` 로 잰다.

  ② 이슈 글의 앞부분이 잘려 나갔다
     `body()` 는 첫 `# ` 헤더 앞을 버린다(원고 파일의 포인터 줄을 떼려고).
     이슈 코멘트는 본문 한참 뒤에 `#` 이 나오는 일이 흔해 **서두가 통째로 사라진다.**
     고침 — 월 묶음 맨 앞에 `# ` 제목 줄을 세워 자르는 칼이 거기서 멈추게 한다.

  ③ 코드블록·수식이 문장으로 세어졌다
     `body()` 는 표·인용·링크는 떼지만 ``` 펜스는 안 뗀다. 이슈에는 코드가 흔하고,
     네 층 중 「길이」와 「표기 전환」이 그 줄에 직격당한다. 원고에는 코드가 없다.
     고침 — 펜스·인라인코드·체크박스를 미리 떼고 넘긴다.

  ④ 다중 라벨이 상관을 부풀렸다
     10장 라벨이 달린 이슈 하나는 열 장에 전부 들어간다. 두 장이 같은 글을 나눠 가지면
     **닮는 게 당연하다.** 짝 상관을 쓰려면 공유분을 빼야 한다.
     고침 — 이 판은 짝 상관(ρ)을 아예 안 쓴다. ρ는 섞음 시험에서 이미 떨어졌다.

■ 새 자는 0개다. `peak_g` 는 2026-08 부터 yaseong_core 에 있던 둘째 자다.
  틀을 더하지 않고 **이미 있던 자를 바꿔 쥔다.**

■ 두 가지를 따로 묻는다 — 섞으면 또 넘어진다
  ·  겹침(무늬)  : 순서가 있어야 하는 물음. **전제 검사부터** 한다 — 1차 자기상관이
                   섞음 구간 밖인가. 밖이 아니면 맞출 무늬가 아예 없는 것이다.
  ·  수렴(문체)  : 순서가 없어도 되는 물음. 네 층 평균 z 네 칸을 한 점으로 보고
                   원고 점까지의 거리를 **달마다** 잰다. 줄면 과정이 제품을 닮아 간다.
  문체는 분포의 성질이라 순서 없이 재도 된다. 무늬는 아니다. 지난달 잘못은 이 둘을
  한 값으로 묶어 부른 것이었다.

■ 2026-10-30 그림을 뺐다 — 방사 팔 여덟이 이 파일의 가장 약한 칸이었다
  ·  방사 길이는 공통 밑동이 없다. Cleveland–McGill 3위 — 사다리의 「공통 눈금 위 위치」가 1위다.
  ·  5장·10장이 가운데 원 안의 **글씨**였다. 열 장 중 둘이 아무 눈금에도 안 서 있었다.
  ·  팔 끝 라벨이 범례와 세 곳에서 겹쳤다.
  그래서 왼쪽 그림만 버리고 **오른쪽 기둥(눈금 교체·둘 사이 거리·전제 검사·할 일 셋·다섯 줄)은
  사다리 판으로 옮겼다.** 이 파일에 남은 것은 자다. 자와 그림을 한 파일에 두면 둘이 갈린다.
  거울짝이 대척점에 서던 것 하나는 방사가 공짜로 가졌던 값인데, 사다리에서는
  행 차례 `1·2·3·4·5 │ 10·9·8·7·6` 과 활 다섯이 **지어서** 세운다.

■ 이 파일이 못 하는 것 — 이슈 글에 사람과 기계가 섞여 있고 계정으로는 못 가른다.
  자가 아니라 장부가 할 일이다. (못 하는 걸 안 적은 자는 자가 아니라 장식이다.)
"""
import collections, datetime as _dt, importlib.util, io, json, math, os, re
import random as _rd, statistics as st, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "hyunjimoon/golden-cage-book"
CACHE = "/tmp/issue_map_cache"
ME = "hyunjimoon"

spec = importlib.util.spec_from_file_location("yc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "yaseong_core.py"))
yc = importlib.util.module_from_spec(spec); sys.modules["yc"] = yc
spec.loader.exec_module(yc)
LAYER, LCOL, esc = yc.LAYER, yc.LCOL, yc.esc

E = os.path.join(ROOT, "chapters/")
CH = [("ch1_mirror_cage.md", 1), ("ch2_telescope_cage.md", 2), ("ch3_glass_cage.md", 3),
      ("ch4_clock_cage.md", 4), ("ch5_mirror_nest.md", 5), ("ch6_butterfly_nest.md", 6),
      ("ch7_tulip_nest.md", 7), ("ch8_mist_nest.md", 8),
      ("ch9_raven_nest.md", 9), ("ch10_mirror_close.md", 10)]
CHNAME = {1: "1 거울새장", 2: "2 망원경", 3: "3 스테인굴레스", 4: "4 시계", 5: "5 101₂호",
          6: "6 나비", 7: "7 튤립", 8: "8 안개", 9: "9 까마귀", 10: "10 투향"}
PAIRCOL = {1: "#0026FB", 6: "#0026FB", 2: "#491786", 7: "#491786",
           3: "#DF1F16", 8: "#DF1F16", 4: "#006610", 9: "#006610",
           5: "#C9A227", 10: "#C9A227"}
INK, SUB, FAINT, CREAM = "#1B1B1E", "#5E584E", "#8C867C", "#FBF8F0"
FONT = "Apple SD Gothic Neo, Helvetica Neue, Helvetica, Arial, sans-serif"
PK, FLAT = 1.5, 0.5


# ── 0 이슈 글 ───────────────────────────────────────────────────────────────
def fetch(name, args):
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, name)
    if os.environ.get("MAP_CACHE") and os.path.exists(p):
        return io.open(p, encoding="utf-8").read()
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        sys.exit("gh 실패: " + r.stderr[:300])
    io.open(p, "w", encoding="utf-8").write(r.stdout)
    return r.stdout


def strip_md(t):
    """③ 고침 — body() 가 안 떼는 것들을 먼저 뗀다."""
    t = re.sub(r"```.*?```", " ", t, flags=re.S)        # 펜스 코드
    t = re.sub(r"~~~.*?~~~", " ", t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", " ", t)                    # 인라인 코드
    t = re.sub(r"<[^>]+>", " ", t)                      # 날 HTML
    t = re.sub(r"^\s*[-*]\s*\[[ xX]\]\s*", "", t, flags=re.M)   # 체크박스
    t = re.sub(r"\$\$?[^$\n]{0,200}\$\$?", " ", t)      # 수식
    return t


def load_process():
    iss = json.loads(fetch("iss.json", [
        "gh", "issue", "list", "--repo", REPO, "--state", "all", "--limit", "400",
        "--json", "number,title,body,labels,state,createdAt,author"]))
    craw = fetch("cm.json", ["gh", "api", f"repos/{REPO}/issues/comments?per_page=100", "--paginate"])
    dec, i, cm = json.JSONDecoder(), 0, []
    while i < len(craw):
        while i < len(craw) and craw[i] in " \n\r\t":
            i += 1
        if i >= len(craw):
            break
        o, j = dec.raw_decode(craw, i); cm += o; i = j
    CHP = re.compile(r"(\d{1,2})장")
    meta, glue = {}, []
    for x in iss:
        lb = [l["name"] for l in x["labels"]]
        meta[x["number"]] = sorted({int(m) for nm in lb for m in CHP.findall(nm) if 1 <= int(m) <= 10})
        if (x.get("author") or {}).get("login") == ME:
            glue.append((x["number"], x["createdAt"], x.get("body") or ""))
    for c in cm:
        if c["user"]["login"] != ME:
            continue
        n = int(re.search(r"/issues/(\d+)", c["issue_url"]).group(1))
        if n in meta:
            glue.append((n, c["created_at"], c.get("body") or ""))
    glue.sort(key=lambda t: t[1])
    return meta, glue


def bundle(tmp, items):
    """items = [(키, 본문문자열)]. ② 고침 — 맨 앞에 '# 제목' 을 세워 body() 의 칼을 멈춘다."""
    chapters = []
    for k, text in items:
        f = "d_%s.md" % re.sub(r"[^0-9A-Za-z가-힣]", "_", str(k))
        io.open(os.path.join(tmp, f), "w", encoding="utf-8").write("# %s\n\n%s" % (k, text))
        chapters.append((f, str(k), "x"))
    return chapters


def ruler(items):
    """① 고침 — 원고와 이슈를 한 묶음으로 넘긴다. GM·GS 와 어휘 코퍼스를 공유한다."""
    tmp = tempfile.mkdtemp()
    chapters = bundle(tmp, items)
    _, measure = yc.load(tmp + "/", chapters)
    return {k: measure(c[0]) for (k, _t), c in zip(items, chapters)}


def pct(rows, key, op):
    n = max(len(rows), 1)
    return 100.0 * sum(1 for r in rows if op(r[key])) / n


def profile(rows):
    """네 층 평균 z 네 칸 = 그 글의 문체 한 점 (공통 눈금)."""
    if not rows:
        return [0.0] * 4
    return [st.mean(r["zg"][k] for r in rows) for k in range(4)]


def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def lag1(v):
    if len(v) < 3:
        return 0.0
    a, b = v[:-1], v[1:]
    ma, mb = st.mean(a), st.mean(b)
    da = math.sqrt(sum((x - ma) ** 2 for x in a)); db = math.sqrt(sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (da * db) if da and db else 0.0


def slope(xs, ys):
    mx, my = st.mean(xs), st.mean(ys)
    d = sum((x - mx) ** 2 for x in xs)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / d if d else 0.0


# ── 제품도 수열이다 — 월말 원고를 git 에서 꺼낸다 (#139 👤🤚 → 👥) ──────────
def _sh(args):
    import subprocess
    r = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    return r.stdout if not r.returncode else ""


def product_months(months):
    """달마다 그때의 원고. 그달 말 커밋에서 가장 높은 N차소통 아래 장 파일을 읽는다."""
    out = {}
    for m in months:
        sha = _sh(["git", "-c", "log.showSignature=false", "log",
                   "--until=%s-28" % m, "--format=%H", "-1"]).strip()
        if not sha:
            continue
        files = [f for f in _sh(["git", "ls-tree", "-r", "--name-only", sha]).split("\n")
                 if re.search(r"^chapters/ch\d{1,2}_[^/]*\.md$", f)]
        if not files:
            continue
        txt = []
        for f in sorted(files):
            raw = _sh(["git", "show", "%s:%s" % (sha, f)])
            if raw.strip():
                txt.append(strip_md(raw))
        if txt:
            out[m] = "\n\n".join(txt)
    return out

# ── 1 재기 — 이 파일은 이제 자(尺)만 낸다. 그림은 gen_converge_ladder.py 하나다 ──
def measure():
    """한 번 돌려 두 판이 쓸 값을 전부 낸다.

    예전에는 이 파일과 사다리 판이 `ruler()` 를 **각자 한 번씩** 돌렸다. 같은 묶음을
    두 번 재면서 시간만 두 배 쓴 것이고, 두 그림의 숫자가 갈릴 틈도 있었다. 이제 한 번이다.
    """
    meta, glue = load_process()
    prod_txt = {c: yc.body(E + f) for f, c in CH}

    # 묶음 A — 장별. 원고 10 + 과정 10(+전반).
    gch = {c: [] for c in range(1, 11)}
    gch[0] = []
    for n, t, b in glue:
        for c in (meta[n] or [0]):
            gch[c].append(strip_md(b))
    A_items = [("원고%d" % c, prod_txt[c]) for c in range(1, 11)] + \
              [("과정%d" % c, "\n\n".join(gch[c])) for c in range(1, 11)]
    A = ruler(A_items)

    # 묶음 B — 두 수열. 제품도 달마다 움직인다(#139 코시) → 👤🤚 가 아니라 👥.
    gmo = collections.OrderedDict()
    for n, t, b in glue:
        gmo.setdefault(t[:7], []).append(strip_md(b))
    MOS = list(gmo.keys())
    PM = product_months(MOS)
    PMOS = [m for m in MOS if m in PM]
    B_items = [("과정%s" % m, "\n\n".join(gmo[m])) for m in MOS] + \
              [("제품%s" % m, PM[m]) for m in PMOS]
    B = ruler(B_items)

    rowP = {c: A["원고%d" % c] for c in range(1, 11)}
    rowQ = {c: A["과정%d" % c] for c in range(1, 11)}

    # 옛 눈금(peak, 글 안 z)과 새 눈금(peak_g, 공통 z) 둘 다 적는다
    old = {"제품": st.mean([pct(rowP[c], "peak", lambda v: v >= PK) for c in range(1, 11)]),
           "과정": st.mean([pct(rowQ[c], "peak", lambda v: v >= PK) for c in range(1, 11)])}
    new = {"제품": st.mean([pct(rowP[c], "peak_g", lambda v: v >= PK) for c in range(1, 11)]),
           "과정": st.mean([pct(rowQ[c], "peak_g", lambda v: v >= PK) for c in range(1, 11)])}

    # 전제 검사 — 무늬가 있기는 한가. 1차 자기상관 대 섞음 95% 구간
    def pre(rows):
        v = [r["peak_g"] for r in rows]
        rd = _rd.Random(7); sh = []
        for _ in range(200):
            q = list(v); rd.shuffle(q); sh.append(lag1(q))
        sh.sort()
        return lag1(v), sh[5], sh[194]
    allP = [r for c in range(1, 11) for r in rowP[c]]
    allQ = [r for c in range(1, 11) for r in rowQ[c]]
    PRE = {"제품": pre(allP), "과정": pre(allQ)}

    # 수렴 — 둘 사이 거리(👥). 별은 안 쓴다. 코시 걸음도 함께 잰다.
    QP = {m: profile(B["과정%s" % m]) for m in MOS}
    PP = {m: profile(B["제품%s" % m]) for m in PMOS}
    D = [(m, dist(PP[m], QP[m]), len(B["과정%s" % m])) for m in PMOS]
    xs = list(range(len(D))); ys = [d for _, d, _ in D]
    sl = slope(xs, ys)
    STEPQ = [(MOS[i + 1], dist(QP[MOS[i]], QP[MOS[i + 1]])) for i in range(len(MOS) - 1)]
    STEPP = [(PMOS[i + 1], dist(PP[PMOS[i]], PP[PMOS[i + 1]])) for i in range(len(PMOS) - 1)]
    # 섞음 — 그달 과정 문장을 뒤섞어 달 꼬리표를 지운다. 거리 줄기가 우연인가.
    pool = [r for m in MOS for r in B["과정%s" % m]]
    sizes = [len(B["과정%s" % m]) for m in MOS]
    rd = _rd.Random(11); shs = []
    for _ in range(200):
        q = list(pool); rd.shuffle(q); i = 0; cut = {}
        for m, sz in zip(MOS, sizes):
            cut[m] = profile(q[i:i + sz]); i += sz
        shs.append(slope(xs, [dist(PP[m], cut[m]) for m in PMOS]))
    shs.sort()

    # 장별 파생 — 사다리 판이 그대로 쓴다. 한 자리에서 내야 두 그림이 안 갈린다.
    P = {c: pct(rowP[c], "peak_g", lambda v: v >= PK) for c in range(1, 11)}
    Q = {c: pct(rowQ[c], "peak_g", lambda v: v >= PK) for c in range(1, 11)}
    NP = {c: len(rowP[c]) for c in range(1, 11)}
    NQ = {c: len(rowQ[c]) for c in range(1, 11)}
    GAP = {c: Q[c] - P[c] for c in range(1, 11)}
    # ⚠️ 이 ± 는 문장이 서로 독립이라고 보고 낸 이항 표준오차다. 전제 검사(PRE)가
    #    1차 자기상관을 섞음 구간 **밖**으로 내놓으므로 독립이 아니다. 분산팽창
    #    (1+r)/(1-r) 로 부풀려 적는다 — 어림이 아니라 같은 실측에서 나온 보정이다.
    rP = PRE["제품"][0]; rQ = PRE["과정"][0]
    vifP = math.sqrt(max(1.0, (1 + rP) / (1 - rP))) if abs(rP) < 1 else 1.0
    vifQ = math.sqrt(max(1.0, (1 + rQ) / (1 - rQ))) if abs(rQ) < 1 else 1.0
    SE = {c: math.hypot(math.sqrt(P[c] / 100 * (1 - P[c] / 100) / NP[c]) * 100 * vifP,
                        math.sqrt(Q[c] / 100 * (1 - Q[c] / 100) / NQ[c]) * 100 * vifQ)
          for c in range(1, 11)}

    return dict(rowP=rowP, rowQ=rowQ, old=old, new=new, PRE=PRE, D=D,
                sl=sl, SLO=shs[5], SHI=shs[194], nglue=len(glue),
                STEPQ=STEPQ, STEPP=STEPP, MOS=MOS,
                P=P, Q=Q, NP=NP, NQ=NQ, GAP=GAP, SE=SE, VIF=(vifP, vifQ))


def main():
    m = measure()
    old, new, PRE = m["old"], m["new"], m["PRE"]
    print("옛 눈금 봉우리%%  제품 %.1f · 과정 %.1f  (차 %.1f)" % (old["제품"], old["과정"], abs(old["제품"] - old["과정"])))
    print("새 눈금 봉우리%%  제품 %.1f · 과정 %.1f  (차 %.1f)" % (new["제품"], new["과정"], abs(new["제품"] - new["과정"])))
    for k, (v, lo, hi) in PRE.items():
        print("1차 자기상관 %s  %+.3f   섞음 95%% [%+.3f, %+.3f]  %s"
              % (k, v, lo, hi, "밖" if not (lo <= v <= hi) else "안"))
    print("분산팽창 보정  제품 ×%.2f · 과정 ×%.2f  (독립 아님 → ± 를 부풀려 적는다)" % m["VIF"])
    for mo, d, n in m["D"]:
        print("  %s  둘 사이 거리 %.3f  (과정 문장 %d)" % (mo, d, n))
    print("  걸음 과정 " + " ".join("%s %.3f" % t for t in m["STEPQ"]))
    print("  걸음 제품 " + " ".join("%s %.3f" % t for t in m["STEPP"]))
    print("기울기 %+.4f   섞음 95%% [%+.4f, %+.4f]  %s"
          % (m["sl"], m["SLO"], m["SHI"], "밖" if not (m["SLO"] <= m["sl"] <= m["SHI"]) else "안"))
    print("\n그림은 .claude/gen_converge_ladder.py 가 그린다 — 이 파일은 자(尺)다.")


if __name__ == "__main__":
    main()
