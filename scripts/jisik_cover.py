# ──────────────────────────────────────────────────────────────────────────
#  (의존 — 01 이 greedy·arches 를 부른다)   ·   ⛺️ 지식덮개 — 지식 8이 경험 19를 덮는다
#  원본  <저자 vault>/.claude/jisik_cover.py   —   손으로 고치지 마라 — .claude/publish_scripts.py 가 찍는다
# ──────────────────────────────────────────────────────────────────────────

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jisik_cover.py — ⛺️ 지식덮개의 자(尺) 하나. **여기 말고 어디에도 두지 않는다.**

덮개 문제는 한 줄이다 — **열(불)마다 X가 하나 이상, 고른 행(돌)의 수는 최소.**
그게 최소 집합덮개(minimum set cover)다. 정점덮개(vertex cover)는 *열마다 후보가
꼭 둘*인 특수꼴이고, 안정집합(stable set)은 부등호가 뒤집힌 **다른** 문제다
(열마다 ≤1 · 개수 최대). 지식덮개의 열은 후보가 둘이 아니므로 일반형에 앉는다.

    열마다 X ≥ 1 · 행 수 최소  →  덮개  (cover)    ← 지식덮개는 여기
    열마다 X ≤ 1 · 행 수 최대  →  쌓기  (packing)  ← stable set 은 여기

쓰는 곳 넷 — 전부 이 파일의 `greedy()` 하나를 부른다:

    ① baesun_mcmf.survivors()     불 = 자리 받은 일화 20  · 돌 = 🍇생각원소 → 9
    ② gen_graph_data PRUNE ×2     불 = 장 1~10            · 돌 = 📜신의전언 4 · 🪞상징 8
    ③ 손으로 지은 덮개 검산        불 = 원천               · 돌 = 지식원소  (`--json` · `--demo 161`)

③이 이 파일이 생긴 이유다. ①②는 코드가 돌리는데 ③은 손으로 지어 왔고,
그래서 중복이 안 걸렸다 — `--demo 161` 이 그 실측이다.

🌗 **덮개가 못 하는 것** — 덮개는 **노드만 센다.** 고른 돌끼리 생기는 모서리(아치)는
`arches()` 가 따로 세고, 둘은 같은 겹침에 **반대 부호**를 매긴다. 덮개는 겹침을
중복으로 깎고(이미 덮인 불은 점수 0), 아치는 겹침을 결론으로 센다. 어느 쪽이 맞는지는
알고리즘이 안 정한다 — **룰링이 정한다.** 그래서 `reverse_delete()` 는 기본으로
적용하지 않고 *보고만* 한다.

가르는 자 한 줄 — 두 돌이 **다른 말**로 같은 불을 받치면 아치, 같은 말을 되풀이하면 빚.

---
## 부록: 연료 (docx 제외)

**복기 — 2026-10-31 세 층 지도 대규모 다이어트 (노드 296 → 53 · 선 864 → 112)**

    0. 재료    네 층 파일 목록 + `[[ ]]` 링크 → 이분 입접관계
    1. 💣 배선  일화 65 → 자리 20.  **덮개 아님** — min cost max flow (baesun_mcmf.solve)
    2. ⛺️ 덮개① 불 = 그 20편.      돌 = 생각원소 145 → 9   (다이나모선이 입접)
    3. ⛺️ 덮개②③ 불 = 장 1~10.     돌 = 신의전언 → 4 · 상징 → 8  (frontmatter chapter)
    4. 🔗 선    양 끝이 **둘 다** 살아야 산다 = 유도부분그래프
    5. 🌗 음화  안 덮인 불은 **지우지 않고 찍는다**

4단이 이미 칼비노다 — 「돌이 없으면 아치도 없다」가 `s in keep and t in keep` 한 줄로
적혀 있다. 곧 **선을 고르는 규칙은 처음부터 아치 쪽이었고, 돌을 고르는 규칙만 덮개였다.**

⚠️ 2단과 3단이 **다른 불**을 쓰는 까닭 — 📜🪞는 일화가 부르지 않고 frontmatter 로 장에
붙는다. 「살아남은 노드가 부르는 것만」으로 재면 0 이 되는데, 0 은 발견이 아니라 자가
틀린 신호다 (#117).

**근사 성질 — 왜 교체가 1:1이 아닌가.** greedy 는 `ln n` 근사이고 그게 집합덮개의
한계다(Dinur–Steurer). 매 단계 *새로 덮는 불의 수*로 고르니 **인기**를 집는다 —
중요해서가 아니라 자주 불려서 1등이 된다. 하나를 내리면 남은 불의 구성이 바뀌어
다른 둘이 들어올 수 있다. `shuffle_sizes()` 로 **순서를 흔들어도 크기가 같은가**를
먼저 보라 — 같으면 뽑은 순서와 무관하게 쌓인 것이고(교환가능성), 흔들리면 그 수를
공표하면 안 된다.
"""
import json
import random
import sys

__all__ = ["greedy", "reverse_delete", "shuffle_sizes", "arches", "report",
           "DEMO_161", "DEMO_161B"]


def greedy(sets, fires, order=None):
    """선이 가장 많이 달린 덮개부터 집는다. 가중치 없음 — #117 note 4 (전부 1).

    sets  : {돌: {불, ...}}      고르는 쪽
    fires : {불, ...}            덮일 쪽
    order : 동점 깨기 순서. None = 이름 사전순 (재현성).

    반환 (chosen, uncovered).  **안 덮인 불은 버리지 않는다** — 음화로 돌려준다.
    ⚠️ baesun_mcmf._greedy_cover 와 한 글자도 다르게 굴지 않는다 (공표값 보존).
    """
    keys = sorted(sets) if order is None else order
    rem, chosen = set(fires), []
    while rem:
        best, bestn = None, 0
        for g in keys:
            n = len(sets[g] & rem)
            if n > bestn:
                bestn, best = n, g
        if best is None:
            break                      # 남은 불에 닿는 덮개가 없다
        chosen.append(best)
        rem -= sets[best]
    return chosen, rem


def reverse_delete(sets, chosen, fires):
    """greedy 뒤에 남은 **중복**을 거른다 — 집은 역순으로 하나씩 빼 본다.

    greedy 는 한 번 집은 돌을 다시 내려놓지 않으므로, 뒤에 집힌 돌이 앞의 것들을
    덮어 **앞의 돌이 필요 없어지는** 일이 생긴다. 표준 뒤처리이고 ①②③ 어디에도
    아직 안 붙어 있다.

    🚫 기본 적용하지 않는다 — 빼는 순간 그림이 바뀌므로 룰링이 먼저다. 보고만 한다.
    반환 (keep, dropped).
    """
    chosen = list(chosen)
    if not chosen:
        return [], []
    target = set(fires) & set().union(*(sets[g] for g in chosen))
    keep, dropped = list(chosen), []
    for g in reversed(chosen):
        rest = [h for h in keep if h != g]
        got = set().union(*(sets[h] for h in rest)) if rest else set()
        if target <= got:
            keep.remove(g)
            dropped.append(g)
    return keep, dropped


def shuffle_sizes(sets, fires, trials=400, seed=0):
    """순서를 흔들어 **크기만** 본다. 한 점이면 집는 순서와 무관하다 (교환가능성).

    「어느 게 선택되든 상관없다」를 재는 자가 이것뿐이다. ⚠️ 크기가 한 점이어도
    **집히는 돌은 달라진다** — 값이 불변인 것과 구성이 불변인 것은 다른 층이다.
    """
    rnd = random.Random(seed)
    keys, sizes = sorted(sets), set()
    for _ in range(trials):
        order = list(keys)
        rnd.shuffle(order)
        sizes.add(len(greedy(sets, fires, order)[0]))
    return sorted(sizes)


def arches(sets, chosen):
    """고른 돌끼리 **같은 불을 함께 받치는** 자리 = 모서리(아치).

    반환 (edges, loners).  edges = [(돌a, 돌b, {함께 받친 불})] · loners = 아치 0인 돌.
    덮개가 깎으려 드는 그 겹침이 여기서는 세어진다 — 같은 수, 반대 부호.
    """
    ks = list(chosen)
    edges = []
    for i, a in enumerate(ks):
        for b in ks[i + 1:]:
            shared = sets[a] & sets[b]
            if shared:
                edges.append((a, b, shared))
    linked = {x for a, b, _ in edges for x in (a, b)}
    return edges, [g for g in ks if g not in linked]


def report(sets, fires, chosen=None, uncovered=None, trials=400, label="지식덮개"):
    """덮개 하나를 집의 말투로 찍는다. 결정은 안 바꾼다 — 재고 보여 줄 뿐."""
    if chosen is None:
        chosen, uncovered = greedy(sets, fires)
    fires = set(fires)
    print("\n⛺️ %s — 돌 %d 중 %d 을 집어 불 %d 을 덮는다"
          % (label, len(sets), len(chosen), len(fires)))

    sizes = shuffle_sizes(sets, fires, trials)
    print("\n  동점 %d회 흔듦 — 덮개 크기 %s%s"
          % (trials, sizes, "  (크기 안정)" if len(sizes) == 1 else "  🚨 크기가 흔들린다"))

    print("\n  덮개 — 집은 순서대로 (몇 불을 새로 덮었나)")
    rem = set(fires)
    for k, g in enumerate(chosen, 1):
        got = sets[g] & rem
        rem -= got
        print("   %2d. %-34s %2d  %s" % (k, g, len(got), " ".join(sorted(got))))

    keep, dropped = reverse_delete(sets, chosen, fires)
    if dropped:
        print("\n  🚨 덮개로는 **중복** %d — 빼도 같은 불이 다 덮인다: %s"
              % (len(dropped), " ".join(dropped)))
        print("     → %d 이면 족하다. 그래도 남길지는 아래 아치가 정한다(룰링)." % len(keep))
    else:
        print("\n  ✅ 중복 없다 — 하나를 빼면 덮이지 않는 불이 생긴다 (극소 덮개)")

    edges, loners = arches(sets, chosen)
    print("\n  🔗 아치 %d — 두 돌이 같은 불을 함께 받치는 자리" % len(edges))
    for a, b, sh in edges:
        print("     %s  —  %s   (%s)" % (a, b, " ".join(sorted(sh))))
    if loners:
        print("  🪨 외돌 %d — 돌 하나, 아치 없음: %s" % (len(loners), " ".join(loners)))

    if uncovered:
        print("\n  🌗 안 덮인 불 %d — **버리지 않는다**: %s"
              % (len(uncovered), " ".join(sorted(uncovered))))
    return dict(chosen=chosen, uncovered=uncovered, sizes=sizes,
                keep=keep, dropped=dropped, arches=edges, loners=loners)


# ── 검산 재료 — #161 「최소복잡도 지식덮개 넷」 ────────────────────────────────
#  표의 **덮는 자리** 칸을 그대로 옮긴 것. 손으로 지은 덮개가 알고리즘을 통과하는지
#  보는 고정 재료다. pdf 는 열 하나(원천 일곱 = pdf 1 + 이슈 6).
#  ⚠️ 원소 2 의 #82·#78 배정은 자장이 「내가 읽은 것」이라 적어 둔 것이다.
DEMO_161 = {
    "1 순서에 안 변한다": {"#146", "#158", "#155"},
    "2 왕복 균형":        {"#82", "#78", "pdf"},
    "3 불변량":           {"#40"},
    "4 차원을 늘린다":    {"#146", "#155", "pdf"},
}
DEMO_161_FIRES = {"#146", "#158", "#155", "#82", "#78", "#40", "pdf"}

#  #161b 「캐는 법」 — 불 열. bridge_crossing.html 과 #155 코멘트(셋의 유사성)에서
#  실을 더 걷어 다시 짰다. 돌 「차원을 늘린다」는 **내려갔다** — 제 불이 전부 남의
#  불이어서 greedy 가 집지 않고, 넣으면 크기가 4~5로 흔들린다(공표 금지 신호).
#  그 말은 돌이 아니라 **캐는 동작**이라 §캐는 법 쪽으로 옮겼다.
DEMO_161B = {
    "A 순서에 안 변한다":      {"#146", "#158", "#155", "#155c"},
    "B 왕복 균형":             {"#82", "#78", "pdf", "#155c"},
    "C 불변량":                {"#40", "pdf"},
    "E 조건 걸수록 자유도 준다": {"bridge", "emotion", "pdf"},
}
DEMO_161B_FIRES = {"#146", "#158", "#155", "#155c", "#82", "#78",
                   "#40", "pdf", "bridge", "emotion"}


def main(argv):
    if "--demo" in argv:
        i = argv.index("--demo")
        which = argv[i + 1] if len(argv) > i + 1 else "161"
        if which == "161b":
            report(DEMO_161B, DEMO_161B_FIRES, label="지식덮개 #161b (캐는 법 · 불 열)")
        else:
            report(DEMO_161, DEMO_161_FIRES, label="지식덮개 #161 (손으로 지은 넷)")
        return 0
    if "--json" in argv:
        d = json.load(open(argv[argv.index("--json") + 1], encoding="utf-8"))
        sets = {k: set(v) for k, v in (d.get("sets") or d).items()}
        fires = set(d.get("fires") or set().union(*sets.values()))
        report(sets, fires, label=d.get("label", "지식덮개"))
        return 0
    print(__doc__.split("---")[0].strip())
    print("\n  python3 .claude/jisik_cover.py --demo [161|161b]")
    print('  python3 .claude/jisik_cover.py --json 입접.json'
          '      {"sets": {"돌": ["불", ...]}, "fires": [...], "label": "..."}')
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
