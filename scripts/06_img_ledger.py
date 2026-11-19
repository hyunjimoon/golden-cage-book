#!/usr/bin/env python3
"""img/ 장부 — 그림마다 ⑴ 어디 쓰이나 ⑵ 밖에서 다시 그릴 수 있나.

scripts/README.md 가 선언한 규칙(「01_x.py 의 그림은 01_x.png 다 · 빈칸은 숨기지
않는다」)을 img/ 에 그대로 적용한다. 쓰는 법: python3 scripts/06_img_ledger.py
gh 로그인이 있으면 이슈 참조까지 세고, 없으면 그 칸만 「못 셈」으로 둔다.
"""
import json, os, re, subprocess, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG, OUT = os.path.join(ROOT, "img"), os.path.join(ROOT, "scripts/img_ledger.md")
SCAN = (".html", ".md", ".py", ".json", ".css", ".js")

def inrepo():
    hit = collections.defaultdict(set)
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__", "node_modules")]
        for f in fn:
            if not f.endswith(SCAN): continue
            p = os.path.join(dp, f)
            try: b = open(p, encoding="utf-8", errors="ignore").read()
            except OSError: continue
            for m in re.findall(r"img/([A-Za-z0-9_.\-가-힣]+)", b):
                hit[m].add(os.path.relpath(p, ROOT))
    return hit

def issues():
    Q = ('query($c:String){repository(owner:"hyunjimoon",name:"golden-cage-book"){'
         'issues(first:50,states:[OPEN,CLOSED],after:$c){pageInfo{hasNextPage endCursor}'
         'nodes{number body comments(first:100){nodes{body}}}}}}')
    sha, main, cur = collections.Counter(), collections.Counter(), None
    RS = re.compile(r"golden-cage-book/(?:raw/)?([0-9a-f]{7,40})/img/([^\s\"')]+)")
    RM = re.compile(r"golden-cage-book/(?:raw/|blob/|tree/)?(?:main|master)/img/([^\s\"')]+)")
    while True:
        a = ["gh","api","graphql","-f","query="+Q] + (["-f","c="+cur] if cur else [])
        r = subprocess.run(a, capture_output=True, text=True)
        try: d = json.loads(r.stdout)["data"]["repository"]["issues"]
        except Exception: return None, None
        for i in d["nodes"]:
            for b in [i["body"] or ""] + [c["body"] or "" for c in i["comments"]["nodes"]]:
                for _, f in RS.findall(b): sha[f] += 1
                for f in RM.findall(b):    main[f] += 1
        if not d["pageInfo"]["hasNextPage"]: break
        cur = d["pageInfo"]["endCursor"]
    return sha, main

# 생성기 — 이 저장소 안에서만 찾는다. 「밖에서 다시 그릴 수 있나」가 묻는 것이다.
def gens():
    g = collections.defaultdict(set)
    sd = os.path.join(ROOT, "scripts")
    for f in os.listdir(sd):
        if not f.endswith(".py"): continue
        b = open(os.path.join(sd, f), encoding="utf-8", errors="ignore").read()
        for m in re.findall(r"img/([A-Za-z0-9_.\-]+)|[\"']([A-Za-z0-9_.\-]+\.(?:png|svg|jpg))[\"']", b):
            n = m[0] or m[1]
            if n: g[n].add(f)
        stem = f[:-3]
        for e in (".png", ".svg"):
            if os.path.exists(os.path.join(sd, stem + e)): g[stem + e].add(f)
    return g

SCANLIKE = re.compile(r"^(ar2?_|scan_)")
def main_():
    rep, G = inrepo(), gens()
    sha, mn = issues()
    rows, n_ok = [], 0
    for f in sorted(os.listdir(IMG)):
        p = os.path.join(IMG, f)
        if os.path.isdir(p): continue
        kb = os.path.getsize(p) // 1024
        used = sorted(rep.get(f, []))
        s = "못 셈" if sha is None else str(sha[f])
        m = "못 셈" if mn  is None else str(mn[f])
        if f in G:            how, mark = "·".join(sorted(G[f])), "✅"
        elif SCANLIKE.match(f): how, mark = "손그림 — 원리상 없다", "🖐️"
        else:                 how, mark = "**없다**", "🚨"
        n_ok += mark == "✅"
        rows.append((mark, f, kb, used, s, m, how))
    L = ["# img/ 장부 — 어디 쓰이나 · 밖에서 다시 그릴 수 있나", "",
        f"> 생성기 `scripts/06_img_ledger.py` · {datetime.date.today()} · **손으로 고치지 않는다.**", "",
        f"**{len(rows)}장 중 이 저장소 안에 생성기가 있는 것 {n_ok}장.** 나머지는 밖의 한 사람이 다시 못 그린다.",
        "", "`✅` 생성기 있음 · `🖐️` 손그림이라 원리상 없음 · `🚨` 그릴 수 있는데 방법이 없음", "",
        "| | 그림 | KB | 저장소 안에서 쓰는 곳 | 이슈 해시핀 | 이슈 main | 다시 그리는 법 |",
        "|:-:|:--|--:|:--|--:|--:|:--|"]
    for mk, f, kb, used, s, m, how in rows:
        u = " · ".join(f"`{x}`" for x in used) if used else "**아무도 안 씀**"
        L.append(f"| {mk} | `{f}` | {kb} | {u} | {s} | {m} | {how} |")
    L += ["", "## 읽는 법", "",
        "- **이슈 해시핀**은 과거 커밋을 가리켜 **이름을 바꿔도 안 깨진다.** 대신 옛 그림을 영원히 보여 준다.",
        "- **이슈 main**은 커밋이 밀리면 **죽는다**(2026-11-15 에 17장이 그렇게 404 났다). 0이어야 한다.",
        "- **쓰는 곳도 0, 이슈도 0**인 줄은 이름을 고칠 게 아니라 **지울지 묻는 자리**다.",
        "- 🚨 줄이 이 저장소의 빚이다. `scripts/README.md` 가 선언한 「짝이 없으면 빈칸을 숨기지 않는다」를 img/ 에 적용한 것이다.", ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(L))
    print(f"{OUT}  — {len(rows)}장 · ✅{n_ok} · 🚨{sum(1 for r in rows if r[0]=='🚨')} · 🖐️{sum(1 for r in rows if r[0]=='🖐️')}")

main_()
