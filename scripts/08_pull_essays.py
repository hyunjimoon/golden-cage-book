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
import hashlib, json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DST  = ROOT / "docs" / "essays"
LED  = ROOT / "docs" / "sources" / "원문대장.tsv"

# 📎 = 한 글자도 안 바꾼 원문. 블록 안은 편집 금지이고 익명화도 금지다 — 고치면 원문이 아니다.
# 표는 AI 가 아니라 원문에 단다(양성 표시): 빠뜨려도 거짓이 안 생긴다.
PIN = re.compile(r"<!-- 📎원문:(\S+) 시작[^>]*-->\n(.*?)\n<!-- 📎원문:\1 끝 -->", re.S)

def ledger():
    d = {}
    if LED.exists():
        for ln in LED.read_text(encoding="utf-8").splitlines():
            if ln.startswith("#") or not ln.strip(): continue
            c = ln.split("\t")
            if len(c) >= 5 and c[0] != "id": d[c[0]] = c[4]
    return d

def gh(path):
    r = subprocess.run(["gh","api",path,"--jq",".body"],capture_output=True,text=True)
    return r.stdout.rstrip("\n") if r.returncode == 0 else None

def main():
    check = "--check" in sys.argv
    wrote = diff = miss = 0
    LD = ledger(); pin_ok = pin_bad = 0
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
        for pid, body in PIN.findall(new):
            h = hashlib.sha256(body.encode("utf-8")).hexdigest()
            if pid not in LD:
                print(f"   ⚠️ 대장에 없는 원문 — {pid} ({f.name})"); pin_bad += 1
            elif LD[pid] != h:
                print(f"   🚨 원문이 바뀌었다 — {pid} ({f.name})"); pin_bad += 1
            else:
                pin_ok += 1
        if new == cur: continue
        diff += 1
        if check:
            print(f"   ✎ 원문과 다르다 — {f.name}")
        else:
            f.write_text(new, encoding="utf-8"); wrote += 1
            print(f"   ✎ 다시 떴다 — {f.name}")
    n = len(list(DST.glob("*.md")))
    pin = f" · 📎 원문 {pin_ok} 지킴" + (f" · 어긋난 것 {pin_bad}" if pin_bad else "")
    if check: print(f"🧵 조각 천 {n}편 · 원문과 다른 것 {diff} · 못 읽은 것 {miss}{pin}")
    else:     print(f"🧵 조각 천 {n}편 · 다시 뜬 것 {wrote} · 못 읽은 것 {miss}{pin}")

main()
