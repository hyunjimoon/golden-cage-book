#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""08_pull_essays.py — 조각 천을 원문에서 다시 뜬다.

**본문은 여기서 고치지 않는다.** 글의 원문은 공개 이슈 코멘트이고 docs/essays/ 는
그 사본이다. 고칠 것이 있으면 이슈에서 고치고 이것을 돌린다 — 그러면 사본에 손댈
자리가 없어진다. 2026-11-20 에 사본과 원문이 서로 다른 낱말을 쓰게 된 일이 있었고,
원인은 조심이 모자라서가 아니라 **사본이 고쳐질 수 있는 자리였기** 때문이다.

머리글 두 줄(제목 · 처음 쓴 자리 · 만나는 자리)만 이 파일이 짓는다. 그 아래는
이슈 본문 그대로다. 비공개 제목은 redact_private.py 가 따로 걷는다.

    python3 scripts/08_pull_essays.py            # 다시 뜬다
    python3 scripts/08_pull_essays.py --check    # 다른 데가 있나만 보고 안 고친다
"""
import json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DST  = ROOT / "docs" / "essays"

def gh(path):
    r = subprocess.run(["gh","api",path,"--jq",".body"],capture_output=True,text=True)
    return r.stdout.rstrip("\n") if r.returncode == 0 else None

def main():
    check = "--check" in sys.argv
    wrote = diff = miss = 0
    for f in sorted(DST.glob("*.md")):
        cur = f.read_text(encoding="utf-8")
        # 머리글 = 첫 「---」 줄 앞까지. 첫 빈 줄로 자르면 제목만 잡혀 주소를 놓친다.
        L = cur.split("\n")
        cut = next((i for i,x in enumerate(L) if x.strip() == "---"), None)
        if cut is None:
            print(f"   ⚠️ 구분선이 없다 — {f.name}"); miss += 1; continue
        head = "\n".join(L[:cut]).rstrip()
        # 원문은 둘 중 하나다 — 이슈 코멘트(#issuecomment-) 또는 이슈 본문(#issue-).
        mc = re.search(r"issues/\d+#issuecomment-(\d+)", head)
        mi = re.search(r"issues/(\d+)#issue-\d+", head)
        if mc:   src = gh(f"repos/hyunjimoon/golden-cage-book/issues/comments/{mc.group(1)}")
        elif mi: src = gh(f"repos/hyunjimoon/golden-cage-book/issues/{mi.group(1)}")
        else:
            print(f"   ⚠️ 머리글에 원문 주소가 없다 — {f.name}"); miss += 1; continue
        if src is None:
            print(f"   ⚠️ 원문을 못 읽었다 — {f.name}"); miss += 1; continue
        new = head + "\n\n---\n\n" + src + "\n"
        if new == cur: continue
        diff += 1
        if check:
            print(f"   ✎ 원문과 다르다 — {f.name}")
        else:
            f.write_text(new, encoding="utf-8"); wrote += 1
            print(f"   ✎ 다시 떴다 — {f.name}")
    n = len(list(DST.glob("*.md")))
    if check: print(f"🧵 조각 천 {n}편 · 원문과 다른 것 {diff} · 못 읽은 것 {miss}")
    else:     print(f"🧵 조각 천 {n}편 · 다시 뜬 것 {wrote} · 못 읽은 것 {miss}")

main()
