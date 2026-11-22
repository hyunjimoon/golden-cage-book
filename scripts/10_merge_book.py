#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""10_merge_book.py — 흩어진 열다섯을 한 권으로 잇는다.

보내는 물건을 만드는 손이다. **자가 아니다** — 재지 않고 잇기만 한다.
입력은 공개면 `chapters/` 하나뿐이라 **밖에서 그대로 돌아간다.**

차례가 이 파일에 적혀 있는 까닭 — 파일명 순으로 정렬하면 ch10 이 ch2 앞에 서고,
앞머리 셋(머릿말·질문과 답·인물소개)은 애초에 알파벳 순이 아니다. 순서를 사람
기억에 두면 다음에 틀린다. 여기 한 곳에만 둔다.

    python3 scripts/10_merge_book.py > 투향_합본.md
    python3 scripts/10_merge_book.py --check          # 빠진 파일과 글자수만 본다
    pandoc 투향_합본.md -o 투향_합본.docx --toc --resource-path=interactive

⚠️ `--resource-path=interactive` 가 빠지면 그림 둘이 조용히 글자로 바뀐다.
   ch10_epilogue 의 그림 경로가 `diagrams/…` 인데, 그 기준이 `chapters/` 가 아니라
   **`interactive/`** 다. 웹에서는 맞고 책으로 뽑을 때만 어긋난다.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CH   = ROOT / "chapters"

# 「질문과 답」(앞) ↔ 「답과 질문」(뒤) 이 짝이라 앞뒤가 이렇게 선다.
ORDER = [
    "ch0_intro.md",          # 머릿말
    "ch0_prologue.md",       # 질문과 답
    "ch0_characters.md",     # 인물소개
    "ch1_mirror_cage.md", "ch2_telescope_cage.md", "ch3_glass_cage.md",
    "ch4_clock_cage.md",  "ch5_mirror_nest.md",    "ch6_butterfly_nest.md",
    "ch7_tulip_nest.md",  "ch8_mist_nest.md",      "ch9_raven_nest.md",
    "ch10_mirror_close.md",
    "ch10_epilogue.md",      # 답과 질문
]

# 본문이 가리키는 그림이 **책 기준으로** 닿나. 웹 기준으로 닿아도 책에선 안 닿을 수 있다.
# pandoc 은 못 닿는 그림을 경고 두 줄로 흘리고 **설명문으로 바꿔** 계속 간다 — 모르면 그대로 나간다.
IMG = re.compile(r'(?:src="|\]\()([^")]+\.(?:png|svg|jpg|jpeg|gif|webp))')

def images():
    out = []
    for f in sorted(CH.glob("*.md")):
        for path in IMG.findall(f.read_text(encoding="utf-8")):
            if path.startswith("http"): continue
            out.append((f.name, path, (CH / path).exists(), (ROOT / "interactive" / path).exists()))
    return out

def main():
    check = "--check" in sys.argv
    miss, total, heads = [], 0, []
    body = []
    for name in ORDER:
        f = CH / name
        if not f.exists():
            miss.append(name); continue
        t = f.read_text(encoding="utf-8").strip()
        total += len(t)
        heads.append(next((l[2:].strip() for l in t.split("\n") if l.startswith("# ")), name))
        body.append(t)

    if check:
        print(f"📕 한 권 — 조각 {len(ORDER)-len(miss)}/{len(ORDER)} · {total:,}자")
        for h in heads: print(f"   · {h}")
        if miss: print("⚠️ 없는 파일 — " + " ".join(miss))

        imgs = images()
        ok = sum(1 for *_, c, _ in imgs if c)
        print(f"🖼️ 본문 그림 {len(imgs)} — 책 기준 닿는 것 **{ok}**")
        for name, path, c, i in imgs:
            if not c:
                where = "interactive/ 기준으로는 닿는다" if i else "어디서도 못 찾았다"
                print(f"   ⚠️ {name} → {path} — {where}")
        if imgs and ok == 0:
            print("   🚨 책으로 뽑으면 그림이 한 장도 안 들어간다. 웹에서는 멀쩡해 보인다.")
        return

    if miss:   # 빈칸을 숨기고 내보내면 편집자가 차례에서 그걸 발견한다
        sys.exit("⚠️ 없는 파일이 있다 — " + " ".join(miss))
    bad = [p for _, p, c, _ in images() if not c]
    if bad:  # 조용히 나가면 받는 사람이 그림 자리에 설명문이 박힌 판을 본다
        print(f"⚠️ 책 기준으로 안 닿는 그림 {len(bad)} — pandoc 에 "
              "`--resource-path=interactive` 를 붙여라", file=sys.stderr)
    print("\n\n---\n\n".join(body))

main()
