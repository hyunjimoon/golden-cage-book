# ──────────────────────────────────────────────────────────────────────────
#  5. 「자꾸 앞으로 되돌아가야 해요」   ·   🧠 배선 — 경험 19를 열 장에 앉힌다
#  원본  <저자 vault>/.claude/baesun_mcmf.py   —   손으로 고치지 마라 — .claude/publish_scripts.py 가 찍는다
# ──────────────────────────────────────────────────────────────────────────

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""배선 최적화 — 기억원소를 「투향」 열 장에 min cost max flow로 배정한다.

원리 문서 = 시공간멜로디/On/me_문현지/생산자/3설득_8손익/저미다_찢기다.md §결대로 찢기
산출 = ep*.md frontmatter의 투향장 · 투향비용  (+ 🧨화약가루_투향.base가 그 값을 읽는다)
⚠️ md·base는 생성물이다. 눈금을 바꾸려면 이 파일을 고친다.

    python3 .claude/baesun_mcmf.py            # 계산만 하고 보고
    python3 .claude/baesun_mcmf.py --write    # frontmatter에 써 넣는다
    python3 .claude/baesun_mcmf.py --recount  # 배선·거울을 본문에서 다시 세어 써 넣는다
    python3 .claude/baesun_mcmf.py --layers   # 세 층 선 수만 센다 (솔버 안 돌린다)
    python3 .claude/baesun_mcmf.py --html     # 자리 경합 한 장 → 기억/00_자리경합.html
"""
import os, re, sys, unicodedata
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jisik_cover as _jc          # ⛺️ 덮개의 자 — SSOT

EP_DIR = "시공간멜로디/On/me_문현지/생산자/기억"
# 세 층 배선을 세려면 이웃 두 층의 이름표가 있어야 한다 (gen_graph_data.py 와 같은 주소).
_NOVEL  = "시공간멜로디/On/me_문현지/제품/소설"
ELEM_DIR = f"{_NOVEL}/_채석장/2차소통/원고/diagrams/생각원소"   # L2 🍇생각원소
GOD_DIR  = f"{_NOVEL}/3차소통/_연료/🗣️현재_신의전언"            # L3 📜신의전언 (읽은 것)
# 공표값 — 이슈 #117 이 든 숫자. 지금 값과 어긋나면 이슈가 낡은 것이다.
# 2026-11-11 다시 못 박음. 옛 값 dict(god=0, 거울=115, 다이나모=167) 은 2026-09-21 실측이고,
# 두 달 사이에 god 이 0→10 으로 섰다 — 「읽은 것은 서로 안 엮인다」를 0 으로 단정할 수 없다.
공표 = dict(god=10, 거울=184, 다이나모=294)
공표_2026_09_21 = 공표          # 옛 이름 — 부르는 자리가 남아 있어 당분간 함께 둔다

# ── 입력 ③ 장(章) — 극과 자리 수 ────────────────────────────────────────────
# ⚓ 룰링 2026-11-09 — **열 장 전부 2자리.** 균등분배(장마다 경험 둘)가 자장의 결정이다.
#   옛 값 「둥지 3 · 이음새 2 · 새장 1」은 새장 넷을 한 편에 가뒀다(1~4장 1 vs 6~9장 3).
#   셋으로 올려 재 봤다 → 자리 30 중 **5가 빈다**(3장 2 · 4·5·10장 각 1). 재료가 셋을 못 받친다.
#   둘이면 20 중 1만 빈다(3장 둘째) — **둘이 재어 나온 균등값이다.**
#   값: 강한 넷(ep61·ep57·ep52·ep60)이 지면에서 내려가고 약한 셋(ep62·ep24·ep30)이 올라온다.
#   되돌리려면 PIN 에 그 장·그 원소를 적는다 — 룰링은 솔버를 이긴다.
CHAPTERS = {
    1: dict(극="🦋", 이름="🪞거울",     자리=2),
    2: dict(극="🧅", 이름="🔭망원경",   자리=2),
    3: dict(극="🌫️", 이름="💒스테인굴레스", 자리=2),
    4: dict(극="🐦‍⬛", 이름="⏱️시계",     자리=2),
    5: dict(극="*",  이름="🐀101₂호",   자리=2),
    6: dict(극="🦋", 이름="🦋나비",     자리=2),
    7: dict(극="🧅", 이름="🧅튤립구근", 자리=2),
    8: dict(극="🌫️", 이름="🌫️안개",     자리=2),
    9: dict(극="🐦‍⬛", 이름="🐦‍⬛까마귀",   자리=2),
   10: dict(극="*",  이름="🧫101₃호",   자리=2),
}
NEST = {6, 7, 8, 9}          # 둥지 = 그 극의 본자리
CAGE = {1: 6, 2: 7, 3: 8, 4: 9}   # 거울짝 (점 반전) — 본자리의 짝
SEAM = {5, 10}               # 이음새 = 모든 극을 조금씩 받는다

# ── 입력 ④ 문턱(gate)과 비용 눈금 ───────────────────────────────────────────
# 문턱 = 없으면 비싸지는 게 아니라 **변 자체가 없다**. 후보에서 뺀다.
#   마찰 — 독자가 왜 아픈지 못 읽는다 (실측 2026-09-30: 16/61 미달)
#   연료 — 고통→연료 전환이 안 적혔으면 아직 쓸 수 없다 (17/61)
#   증거 — 지금 61/61 통과라 비용항으로 두면 상수다. 문턱으로만 남긴다
# 비용 항은 셋뿐 — fit · 배선 · 방출.
# 근거(단순성 기준, `--audit`): 마찰·증거·연료를 비용항으로 두든 빼든 배정 변화 0/20.
# 자리를 실제로 가르는 것은 배선(8/20)과 방출(14/20)이다. 나머지를 항으로 두면 훈장이다.
GATES = ("마찰", "증거", "연료")

# ── 입력 ⑤ 룰링 — 솔버가 되돌려 준 자리를 자장이 이유 한 줄로 못 박는다 ──────
# 여유 ≤ 0 으로 되돌아온 자리만 여기 적는다. **적힌 자리는 솔버를 이긴다**
# (후보 변을 그 장 하나로 줄이고 PIN 만큼 깎아, 자리 경합에서 밀리지 않게 한다).
# 보고의 비용·총비용은 PIN 을 되돌려 적는다 — 룰링이 숫자를 예쁘게 만들면 안 된다.
RULINGS = {
    21: (5, "핵심 주장이 「이익을 본 뒤」가 아니라 「보기 전에 묶는다」 = 5장 ★멈춤. "
            "먹이는 생각원소도 g5_02_멈춤_NC 가 첫 줄. 10장은 빚을 갚는 장이고 ep21 은 "
            "의가 8개월 늦게 왔다고 적은, 아직 쓰는 중인 빚이다. 5장·10장 둘 다 이음새라 총비용 변화 0."),
    # 9장 세 자리 (2026-10-11) — 자가 아예 0이라 손으로 가른 자리다.
    # 9장에 앉을 수 있는 협력자 7편 중 여섯이 g=-11·비용 -9 로 완전 동점이고,
    # 일곱 중 **누구도** g9_ 도 거울짝 g4_ 도 지목하지 않는다(조준 = 0). 모형이 눈을 감는 칸.
    # 9장의 자 = 「잰 값이 아니라 자(尺)를 감사한다」 + 둥지 동사 **매혹(재명명)** + 「삼키면 어둠, 던지면 해·달·별」.
    42: (9, "마찰 줄 자체가 「평가자가 준 척도 ↔ 그 척도 자체가 옳은가」이고 연료에 "
            "「자를 감사한다 — 협력자 극의 본령」이 적혀 있다. 다이나모선 첫 줄이 "
            "g5_13_evaluate_재는_손 「잰 값이 아니라 자를 감사한다」. 반박 근거를 "
            "**다른 스승의 논문**(Fine 1986)에서 가져온 것 = 자를 바꿔 끼운 동작."),
    59: (9, "9장 둥지 동사는 매혹 = 재명명인데 다이나모선에 g5_11_재명명_rename "
            "「*못 알아듣겠다*를 *디버깅*으로 다시 이름 붙이기」가 그대로 있다. "
            "그리고 g5_13 주석이 「형식은 버렸으나 자는 그대로 내 손에 있었다」 — "
            "잰 값을 버리고 자를 지킨 자리."),
    60: (9, "「삼키면 어둠, 던지면 해·달·별」 — 중심식(dG/dF)을 뒤집는 코딩을 "
            "남이 찾기 전에 내가 먼저 말한다(g5_06_장부를_펴다 · g5_04_음화로_완성). "
            "연료 줄이 「무엇을 성공으로 셀지가 부호를 정한다」 = 자가 답을 만든다."),
    # 3장 대표 (⚓ 룰링 2026-10-14) — R5 가 ep51 을 빼면서 빈 자리다.
    31: (3, "3장 자 = 「검증보다 빠른 확신이 남의 자원을 담보로 잡았다」이고 ep31 의 마찰 줄이 "
            "「병렬 탐색의 속도 ↔ 남의 이름이 걸린 평판」 — 자와 글자 그대로 맞는다. "
            "스스로 3장을 댄 ep51 은 원본형태가 「하얀거짓말(엄마)」 당일 채록이라 "
            "R5(새장 1~4장 자전적 가족 소재 금지)에 걸려 연료층으로 내렸다. "
            "ep03·ep11 보다 ep31 인 이유 = 담보로 잡힌 것이 남의 **평판**이라 3장 자의 목적어가 같다."),
    # 밀린 둘 — 왜 9장이 아닌가
    #   ep48 : 자기 거울 줄이 ep42 를 「쌍둥이 원소」라 부른다(3주 차이). 세 자리를 쌍둥이 둘에 쓰지
    #          않는다. 그리고 ep48 의 가장 센 조준은 6장 4번 — 「그의 연장(NSP)을 들고 그에게 갔다」
    #          = 둥지 **모방**이지 자를 바꿔 끼운 게 아니다.
    #   ep26 : 조준이 5·6·2 로 가고 9·4 에는 한 줄도 없다. 핵심은 어휘를 바꿔 건넨 것 =
    #          **전이 축**(넘김)이라 9장 자에 안 걸린다.
}
PIN = 1000

# ── 입력 ⑤′ 주제장 — 61편 전수 「장 주제」 분류 (⚓ 룰링 2026-10-14) ──────────
# **이것이 적합(fit)을 재는 자다.** 옛 자는 극(누가 나오나)이었고, 극은 거울짝을
# 원리상 못 갈랐다 — 1장 *모르고* 입기 ↔ 6장 *알고* 입기가 **같은 극**이다.
# 근거는 각 편의 자기 말(`마찰:`·`연료:`)에서만 뽑았다. 표 = 00_일화원소_대장 §🧭.
# ⚠️ 이 dict 가 후보를 정한다 — **적힌 장 말고는 변이 없다.** 그래서 극 문턱은 걷었다.
#    걷은 근거(실측) — 9장 자(「잰 값이 아니라 자를 감사한다」)에 걸린
#    ep02·04·08·32·36 다섯이 전부 🧅기술자 극이다. 극으로 재면 이 다섯이 통째로 빠진다.
#    「누구로 세면 가장 얇은 극(🐦‍⬛ 8/61)이, 무엇으로 세면 가장 두껍다(10/61).」
# ⚠️ None = **자리에 앉히지 않는다**(하단 연료층으로만 남긴다). 지금 하나뿐.
# 🙋‍♀️ 투향장 frontmatter 는 이제 이 dict 의 **생성물**이다 — 손으로 고치지 마라.
주제장 = {
    # 1 🪞 거울 — 내 것인 줄 알았는데 남의 것이었다 (모름)
    12: 1, 19: 1, 27: 1, 29: 1, 62: 1,
    # 2 🔭 망원경 — 정확히 봤는데 안 움직였다 (진단이 알리바이)
    24: 2, 28: 2, 33: 2, 38: 2, 46: 2,
    # 3 💒 스테인굴레스 — 검증보다 빠른 확신이 남의 자원을 담보로 잡았다
    3: 3, 11: 3, 31: 3,
    51: None,   # 🚨 R5 — 원본형태가 「하얀거짓말(엄마)」 당일 채록이다. 자기 연료 줄이
                #    3장을 직접 대지만(🗣️), 새장은 **남의 이야기로 진단하는 층**이라
                #    저자 가족이 들어오면 진단이 고백으로 바뀐다. 연료층으로만 남긴다.
    # 4 ⏱️ 시계 — 내가 지은 질서가 잘 돌수록 나를 가둔다
    5: 4, 30: 4, 55: 4,
    # 5 🐀 101₂호 — 재는 자가 녹는다 · 보기 전에 묶는다
    7: 5, 13: 5, 18: 5, 21: 5, 22: 5, 39: 5,
    # 6 🦋 나비 — 알고 입는다 · 내 원함이 남의 원함을 덮어썼나
    9: 6, 23: 6, 25: 6, 44: 6, 47: 6, 58: 6, 61: 6,
    63: 6,     # 🎞️ep63 Aether — 연료 줄이 「모르고 입는다(1장) → 알고 입는다(6장)」를
                #    직접 댄다. 빌린 이름이 출처가 꺼진 뒤에도 남는 자리.
    # 7 🧅 튤립구근 — 상상한 것이 지어지나 · 손이 흙에 닿았나
    15: 7, 16: 7, 34: 7, 41: 7, 56: 7,
    57: 7,      # ⚠️ 이동 3→7 (⚓ 2026-10-14). 자기 연료 줄이 「7장 — τ*의 V와 i가
                #    한 밥상에서 갈린다」로 **7장을 직접 댄다**. 옛 투향장 3 은 극(🌫️)이 낸 값.
    # 8 🌫️ 안개 — 되물음은 모욕이 아니라 보호다 · 삼켰나 되물었나
    1: 8, 17: 8, 43: 8, 49: 8, 50: 8, 52: 8, 53: 8, 54: 8,
    # 9 🐦‍⬛ 까마귀 — 잰 값이 아니라 자(尺)를 감사한다 · 삼키지 않고 던진다
    2: 9, 4: 9, 8: 9, 26: 9, 32: 9, 36: 9, 42: 9, 48: 9, 59: 9, 60: 9,
    # 10 🧫 101₃호 — 뜨겁게 빚을 갚는다 · 줄탁동시
    6: 10, 10: 10, 20: 10, 37: 10, 40: 10, 45: 10,
    35: 10,     # ⚠️ 이동 5→10 (⚓ 2026-10-14). 연료 줄이 「10장 공명 구조의 실물 배선」.
                #    가족 소재지만 10장은 R5 예외다(§6 「첫 고객은 부모였다」 기존 확정분).
}

# 🙋‍♀️ 기억.py 가 올린 자리 — 컴퓨터를 모르는 사람이 코드를 고치지 않아도 되게,
#    `.claude/주제장_추가.json` 에 적힌 것을 여기서 합친다. 위 표가 늘 이긴다.
import json as _json
_추가 = f"{os.path.dirname(os.path.abspath(__file__))}/주제장_추가.json"
if os.path.exists(_추가):
    for _k, _v in _json.load(open(_추가, encoding="utf-8")).items():
        주제장.setdefault(int(_k), _v)

# 자가 둘이 되는 순간 터지게 둔다 — RULINGS 와 주제장이 어긋나면 import 자체가 실패한다.
for _n, (_ch, _why) in RULINGS.items():
    assert 주제장.get(_n) == _ch, f"🚨 자가 갈렸다: RULINGS[{_n}]={_ch} ↔ 주제장[{_n}]={주제장.get(_n)}"

# ── 입력 ⑥ 자리값(유보가격) ─────────────────────────────────────────────────
# 예전 `c = 10 - 2*fit` 의 10. 상수로 숨어 있던 것을 이름으로 꺼냈다.
# 뜻 = 「빈 자리 하나의 값」. 원소의 감동이 이 값을 못 넘으면 **자리를 비워 둔다.**
# 그래서 이 파일은 더 이상 min cost MAX flow 가 아니라 min cost flow 를 푼다 —
# 20자리를 채우는 것이 목적이 아니라, 채울 값이 있는 자리만 채우는 것이 목적이다.
# 🙋‍♀️ 10 은 아무도 정한 적 없는 숫자다. 자장 룰링 대상.
자리값 = 10

# ── 입력 ⑦ 조준 — 원소가 스스로 가리키는 장 (유일한 「원소×장」 항) ──────────
# 지금까지 감동은 f(장)+g(원소) 로 **완전히 쪼개졌다**(실측 2026-10-11: 교환 4,126가지
# 전부 합 동일). 그래서 짝짓기를 감동이 전혀 못 가리고, 배정표의 짝은 SPFA 큐 순서였다.
# 짝짓기 정보는 이미 데이터에 있다 — 🔗다이나모선이 가리킨 생각원소의 `chapter:`.
# ⚠️ 2026-11-11 고침 — 그 전에는 파일명 `g{n}_` 의 n 을 장으로 셌다. n 은 **족번호**다
#    (1 방정식·2 프레임워크·3 이론·4 메타포·5 연산·6 어휘). 족이 여섯에서 끝나기 때문에
#    「7~10장은 조준이 영원히 0」으로 읽혔지만, 실은 족 분포를 장으로 읽고 있었다.
#    장 주소는 원소 frontmatter 의 `chapter:` 하나다 — 88/148 원소(59%)가 숫자 장을 적었고
#    장별로 1:7 · 2:6 · 3:11 · 4:6 · 5:19 · 6:7 · 7:17 · 8:12 · 9:17 · 10:4 이다.
# 자리 셈 — **직접 지목 2점 · 거울짝 지목 1점.** 직접은 원소가 댄 증거,
# 거울은 추론이다. 그래서 거울을 반값으로 둔다(정수로 유지하려 2:1 로 적는다).
# ⑵ 거울짝 지목도 센다 — 7↔2 · 8↔3 · 9↔4 · 10↔5 (CLAUDE §1 거울짝 다섯, 점 반전).
#    장을 안 적은 원소 60편이 있어 짝 쪽 증거까지 긁어모은다.
#    ⚠️ 거울을 **같은 값**으로 주면 짝 안쪽(1↔6, 5↔10)이 다시 동점이 된다. 반값이 그 이유다.
# 🙋‍♀️ 남은 룰링 하나 — 조준값. 1 이면 직접 지목 1건이 방출 2 만큼 센다.
조준값 = 1
MIRROR = {1: 6, 6: 1, 2: 7, 7: 2, 3: 8, 8: 3, 4: 9, 9: 4, 5: 10, 10: 5}

# ── 입력 ⑧ 2단 분리 — 선발과 배정을 다른 저울에 올린다 ──────────────────────
# 한 저울에 두면 「잘 맞지만 약한 원소」가 「안 맞지만 센 원소」를 밀어낸다
# (실측 2026-10-11: 조준을 켜자 선발이 3건 바뀌었다 — ep18·ep20·ep33 나가고
#  ep28·ep29·ep59 들어옴). 적합은 **자리를 가르는 자**이지 **뽑는 자**가 아니다.
#   ① 선발 — 조준을 끄고 화력(배선·방출)으로만 20명을 고른다
#   ② 배정 — 뽑힌 20명 **안에서만** 조준으로 자리를 가른다
분리 = True
COHORT = None   # ② 단계에서 ①을 통과한 원소 번호. None = 전원 후보

def cost(ep, ch):
    """낮을수록 좋다. 변이 없으면 None."""
    if any(not ep[g] for g in GATES):
        return None                # 문턱 미달 = 아직 후보가 아니다
    if COHORT is not None and ep["번호"] not in COHORT:
        return None                # 2단 배정 — ① 선발을 통과한 원소만 후보
    ruled = RULINGS.get(ep["번호"])
    if ruled and ruled[0] != ch:
        return None                # 룰링된 원소는 그 장 말고 갈 데가 없다
    주제 = 주제장.get(ep["번호"])
    if 주제 is None or 주제 != ch:
        return None                # 주제장이 후보를 정한다 (옛 극 문턱을 대신한다)
    # 자리종류 — 주제가 이미 맞았으므로 「어느 층의 자리인가」만 남는다
    fit = 4 if ch in NEST else (2 if ch in CAGE else 1)
    c = 자리값 - 2 * fit
    # 다이나모선 — 🎞️일화원소.base의 「꿰맴」 3단 눈금을 그대로 쓴다 (자를 둘로 두지 않는다)
    c -= 3 if ep["배선"] >= 5 else (1 if ep["배선"] > 0 else 0)   # ✅감김 / ⚠️얇음 / 🕳️없음
    c -= ep["투향방출"]            # 투향 화력
    조준 = 2 * ep["조준"].get(ch, 0) + ep["조준"].get(MIRROR[ch], 0)
    c -= 조준값 * 조준                  # 유일한 원소×장 항 (조준값 0이면 축퇴 그대로)
    if ruled:
        c -= PIN                   # 룰링은 자리 경합에서 지지 않는다 (보고에서 되돌린다)
    return c                       # ⚠️ 음수 허용 — 0에서 끊으면 화력 차이가 통째로 뭉개진다

# ── min cost flow (successive shortest path · SPFA) ───────────────────────
# ⚠️ Dijkstra 로 바꾸지 마라 — 간선 비용이 **음수**다(투향방출을 빼기 때문).
#    초기 그래프가 S→원소→장→T 비순환이라 음수 순환이 없고, 매번 최단경로로만
#    증대하므로 잔여 그래프에도 음수 순환이 안 생긴다 = SSP 정당성 조건.
#    Dijkstra 는 음수 간선에서 틀린 답을 조용히 낸다(Johnson 전위 없이는).
#    q.pop(0) 는 O(n) 이지만 n=71 이라 둔다. 1e4 자리에서는 deque 로 바꿀 것.
class MCMF:
    def __init__(s, n):
        s.n = n; s.g = [[] for _ in range(n)]
    def add(s, u, v, cap, cst):
        s.g[u].append([v, cap, cst, len(s.g[v])])
        s.g[v].append([u, 0, -cst, len(s.g[u]) - 1])
    def run(s, src, snk):
        flow = total = 0
        while True:
            dist = [None] * s.n; dist[src] = 0
            inq = [False] * s.n; prev = [None] * s.n
            q = [src]; inq[src] = True
            while q:
                u = q.pop(0); inq[u] = False
                for i, e in enumerate(s.g[u]):
                    v, cap, cst, _ = e
                    if cap > 0 and (dist[v] is None or dist[u] + cst < dist[v]):
                        dist[v] = dist[u] + cst; prev[v] = (u, i)
                        if not inq[v]:
                            q.append(v); inq[v] = True
            # 길이 없거나, 더 흘려도 비용이 안 줄면 멈춘다.
            # ⚠️ `is None` 만 보고 멈추면 min cost MAX flow 가 되어, 비용 양수인
            #    자리까지 억지로 채운다. 자리값을 유보가격으로 쓰는 뜻이 사라진다.
            if dist[snk] is None or dist[snk] >= 0:
                return flow, total
            # 병목 찾기
            d = float("inf"); v = snk
            while v != src:
                u, i = prev[v]; d = min(d, s.g[u][i][1]); v = u
            v = snk
            while v != src:
                u, i = prev[v]
                s.g[u][i][1] -= d
                s.g[v][s.g[u][i][3]][1] += d
                v = u
            flow += d; total += d * dist[snk]

# ── 원소 읽기 ───────────────────────────────────────────────────────────────
_CHAP = None


def chap_of_elements():
    """생각원소 이름 → 그 원소가 적어 둔 장 번호들. 장 주소는 `chapter:` 하나다.
    「부2」·「Lex」·「전」 같은 값은 장이 아니므로 버린다 (「6·9」 는 둘 다 센다)."""
    global _CHAP
    if _CHAP is None:
        _CHAP = {}
        for fn in os.listdir(ELEM_DIR) if os.path.isdir(ELEM_DIR) else []:
            nfc = unicodedata.normalize("NFC", fn)
            if not nfc.endswith(".md"):
                continue
            s = open(os.path.join(ELEM_DIR, fn), encoding="utf-8").read()
            m = re.search(r"^chapter:\s*\"?([^\"\n]+)", s, re.M)
            toks = re.split(r"[·,/\s]+", m.group(1).strip()) if m else []
            _CHAP[nfc[:-3]] = [int(t) for t in toks if t.isdigit() and 1 <= int(t) <= 10]
    return _CHAP


def aim(body):
    """🔗다이나모선이 가리킨 생각원소들의 `chapter:` 를 장별로 센다. 원소가 스스로 댄 주소.
    ⚠️ 링크는 **전체경로**여야 한다 — 짧은 꼴은 여기서 조용히 0이 된다."""
    m = re.search(r"##\s*🔗 다이나모선(.*?)(?=\n##\s|\Z)", body, re.S)
    out = defaultdict(int)
    cmap = chap_of_elements()
    for nm in re.findall(r"/(g\d_[^\]|/\n]+)", m.group(1) if m else ""):
        for ch in cmap.get(unicodedata.normalize("NFC", nm.strip()), []):
            out[ch] += 1
    return dict(out)


def read_eps():
    eps = []
    for fn in sorted(os.listdir(EP_DIR)):
        nfc = unicodedata.normalize("NFC", fn)
        if not (nfc.startswith("ep") and nfc.endswith(".md")):
            continue
        s = open(os.path.join(EP_DIR, fn), encoding="utf-8").read()
        if not s.startswith("---\n"):
            continue
        fm = s[4:s.index("\n---\n", 3)]
        def g(k, d=""):
            m = re.search(rf"^{k}:\s*(.*)$", fm, re.M)
            return m.group(1).strip().strip('"') if m else d
        eps.append(dict(
            file=fn, 이름=nfc[:-3],
            번호=int(g("번호", "0") or 0),
            극=g("극"), 마찰=bool(g("마찰")), 증거=bool(g("증거")),
            배선=int(g("배선", "0") or 0), gen=int(g("gen", "1") or 1),
            연료=bool(g("연료")) and "🟡" not in g("연료"),   # 🟡 = 미확보 (base 「연료상태」와 같은 자)
            방출=int(g("방출", "0") or 0),
            투향방출=int(g("투향방출", "0") or 0),
            조준=aim(s),
        ))
    return eps

def _basenames(d, keep):
    if not os.path.isdir(d):
        return set()
    out = set()
    for f in os.listdir(d):
        nfc = unicodedata.normalize("NFC", f)
        if nfc.endswith(".md") and keep(nfc):
            out.add(nfc[:-3])
    return out


def _links(body, title=None):
    """[[대상]] 을 파일이름(basename)으로. title 을 주면 그 `## 절` 안만 본다."""
    if title is not None:
        m = re.search(rf"##\s*{title}[^\n]*\n(.*?)(?=\n##\s|\Z)", body, re.S)
        body = m.group(1) if m else ""
    return [unicodedata.normalize("NFC", t.split("|")[0].split("#")[0].split("/")[-1].strip())
            for t in re.findall(r"\[\[([^\]]+)\]\]", body)]


def _read(d, name):
    return open(os.path.join(d, name), encoding="utf-8").read()


def _greedy_cover(covers, fires, order=None):
    """⛺️ 덮개 — **자는 .claude/jisik_cover.py 하나뿐이다.** 여기는 빌려 쓰는 자리.
       gen_graph_data.py 가 이 이름으로 부르므로 이름·인자·반환을 그대로 둔다.
       (2026-11-02 이관 — 같은 알고리즘이 세 곳에서 돌고 있었다.)"""
    return _jc.greedy(covers, fires, order)


def survivors():
    """살아남는 집합 하나. **자는 여기 하나뿐이다** — gen_graph_data.py 도 이걸 불러 쓴다.

    ① 💣 배선(min cost max flow)이 일화 65 → 자리 20 을 가른다.
    ② ⛺️ 덮개가 **그 20편만** 덮는 최소 생각원소를 집는다.
    ⚠️ 상대경로를 쓰므로 vault 루트에서 돌려야 한다 (EP_DIR 이 상대다).
    """
    global 조준값, COHORT
    eps = read_eps()
    if 분리:
        keep, 조준값 = 조준값, 0
        sel, _, _, _ = solve(eps)
        조준값, COHORT = keep, {eps[i]["번호"] for i in sel}
    assign, _, _, _ = solve(eps)
    seat_of = {eps[i]["이름"]: ch for i, (ch, _) in assign.items()}

    gs = _basenames(ELEM_DIR, lambda f: re.match(r"g[1-6]_", f) is not None)
    covers, ep_links = defaultdict(set), {}
    for f in sorted(os.listdir(EP_DIR)):
        nfc = unicodedata.normalize("NFC", f)
        if not (nfc.startswith("ep") and nfc.endswith(".md")):
            continue
        me, body = nfc[:-3], _read(EP_DIR, f)
        ep_links[me] = set(_links(body))
        for t in _links(body, "🔗 다이나모선"):
            if t in gs:
                covers[t].add(me)

    seated = set(seat_of)
    chosen, uncovered = _greedy_cover(covers, seated)
    return dict(eps=eps, seat_of=seat_of, seated=seated, gs=gs,
                covers=covers, ep_links=ep_links, chosen=chosen, uncovered=uncovered)


def cover():
    """⛺️ 지식덮개 — **자리를 받은 일화만** 덮는 최소 생각원소 집합.

    #117 코멘트 두 개가 이 함수의 정본이다.
      6517189091  ⛺️ 덮개 찾기 일곱 줄 · 안 덮인 불은 버리지 말 것 · 음화 셋
      5881204926  🔥a 뿌린다 → ⛺️ 덮는다 → 💣b 잇는다 → 🌀c 댄다

    ⚠️ 순서가 자다 — 결과를 보고 바꾸지 마라.
      ① 💣 배선(min cost max flow)이 먼저 일화 65 → 자리 20 을 가른다.
         자리는 책의 실제 수용량이다(열 장 전부 2, ⚓ 룰링 2026-11-09).
      ② ⛺️ 덮개는 **그 20편만** 덮는다. 65 전체를 덮으면 지면에 안 올 일화를
         받치는 생각원소가 살아남아, 「딱 필요한 것」이 아니라 「많이 불린 것」이 남는다.

    ⚠️ 셈을 이기는 규칙 하나 (#117) — 「남에게 안 일어나는 건가, 남이 안 적는 건가?」
      「지른 나, 막는 나」는 사례 장부 0건이다. 셈에 맡기면 5장·10장이 통째로 지워진다.
      그래서 이음새 두 장의 자리 4개는 솔버가 아니라 룰링이 지킨다 — 아래 검문이 그것을 센다.

    🌗 이 자가 못 하는 것 (#117 음화 그대로)
      · 덮개는 **인기**를 고른다. 중요해서가 아니라 자주 불려서 1등이 된다.
      · 탐욕은 최적이 아니다 — 최악의 경우 최적의 ln(n)배.
      · 덮는다 = 나머지 선을 버린다. 그 나머지가 「이 겪음이 어느 생각을 받치나」다.
        그래서 노드 수만 적지 않고 **엣지 수를 같이** 적는다.
    """
    import random
    S = survivors()
    eps, seat_of, seated = S["eps"], S["seat_of"], S["seated"]
    gs, covers, ep_links = S["gs"], S["covers"], S["ep_links"]
    chosen, uncovered = S["chosen"], S["uncovered"]
    # 동점 안정성 — 순서를 400번 흔들어 크기만 본다 (#117 note 2)
    sizes = set()
    for _ in range(400):
        order = sorted(covers); random.shuffle(order)
        sizes.add(len(_greedy_cover(covers, seated, order)[0]))

    # ── 📜 신의전언 — 살아남은 노드가 부르는 것만 ─────────────────────────
    gods = _basenames(GOD_DIR, lambda f: True)
    called = set()
    for e in seated:
        called |= ep_links.get(e, set()) & gods
    for g in chosen:
        try:
            called |= set(_links(_read(ELEM_DIR, g + ".md"))) & gods
        except Exception:
            pass

    # ── 엣지 — 노드만 세면 거짓말이 된다 (#117 음화) ──────────────────────
    mirror_all = mirror_cut = 0
    for f in sorted(os.listdir(EP_DIR)):
        nfc = unicodedata.normalize("NFC", f)
        if not (nfc.startswith("ep") and nfc.endswith(".md")):
            continue
        me = nfc[:-3]
        for t in _links(_read(EP_DIR, f), "🪞 거울"):
            if t in ep_links and t != me:
                mirror_all += 1
                if me in seated and t in seated:
                    mirror_cut += 1
    dyn_all = sum(len(v) for v in covers.values())
    dyn_cut = sum(1 for g in chosen for e in covers[g] if e in seated)
    e_all, e_cut = mirror_all // 2 + dyn_all, mirror_cut // 2 + dyn_cut

    # ── 보고 ───────────────────────────────────────────────────────────────
    W = lambda a, b: "%d → %d  (%+.0f%%)" % (a, b, -100 * (a - b) / a) if a else "0"
    print("\n⛺️ 가지치기 — ① 배선으로 자리를 가르고 ② 그 자리만 덮는다\n")
    print("  🎞️ 일화원소   " + W(len(eps), len(seated)) + "   ← 💣 자리 20 (룰링한 수용량)")
    print("  🍇 생각원소   " + W(len(gs), len(chosen)) + "   ← ⛺️ 덮개")
    print("  📜 신의전언   " + W(len(gods), len(called)) + "   ← 살아남은 노드가 부르는 것만")
    print("  🔗 엣지       " + W(e_all, e_cut) + "   ← 거울 %d + 다이나모 %d" % (mirror_cut // 2, dyn_cut))
    print("\n  동점 400회 흔듦 — 덮개 크기 %s%s"
          % (sorted(sizes), "  (크기 안정)" if len(sizes) == 1 else "  🚨 크기가 흔들린다"))

    print("\n  덮개 — 집은 순서대로 (몇 편을 새로 덮었나)")
    rem = set(seated)
    for k, g in enumerate(chosen, 1):
        got = covers[g] & rem
        rem -= got
        print("   %2d. %-44s %2d편  %s" % (k, g, len(got),
              " ".join(sorted(x.split("_")[0] for x in got))))

    # ── 덮개 뒤처리 — 재기만 한다. 결정은 안 바꾼다 (2026-11-02) ────────────
    #  중복: greedy 는 집은 돌을 다시 내려놓지 않아 앞의 돌이 남을 수 있다.
    #  아치: 고른 돌끼리 같은 불을 함께 받치는 자리. 덮개가 깎으려 드는 그 겹침이다.
    #  🚫 중복을 빼지 않는다 — 빼면 그림이 바뀌고, 아치가 먼저 0 이 된다. 룰링 자리.
    _keep, _drop = _jc.reverse_delete(covers, chosen, seated)
    if _drop:
        print("  🚨 덮개 중복 %d — 빼도 같은 불이 다 덮인다: %s  → %d 로 족하다"
              % (len(_drop), " ".join(_drop), len(_keep)))
    _arch, _lone = _jc.arches(covers, chosen)
    print("  🔗 아치 %d — 두 생각원소가 같은 일화를 함께 받치는 자리%s"
          % (len(_arch), ("  · 🪨 외돌 " + str(len(_lone))) if _lone else ""))
    if uncovered:
        print("\n  🚨 안 덮인 불 %d — **버리지 않는다.** 어떤 생각도 안 닿는다 (#117)" % len(uncovered))
        for e in sorted(uncovered):
            print("      %-44s %d장" % (e, seat_of[e]))
    else:
        print("\n  안 덮인 불 0 — 「0건은 발견이 아니라 자를 의심할 신호」(#117). 자를 바꿔 한 번 더 셀 자리다.")

    # ── 검문 — 셈이 책을 지웠나 ────────────────────────────────────────────
    print("\n  📐 검문 — 열 장이 다 남았나 (셈이 5·10장을 지우는 것을 막는 자리)")
    hole = []
    for ch in sorted(CHAPTERS):
        mine = sorted(e for e in seated if seat_of[e] == ch)
        gcov = [g for g in chosen if covers[g] & set(mine)]
        if not mine or not gcov:
            hole.append(ch)
        print("    %2d장 %-10s 일화 %d · 덮개 %d %s"
              % (ch, CHAPTERS[ch]["이름"], len(mine), len(gcov), "🚨" if (not mine or not gcov) else ""))
    print("    " + ("✅ 열 장 전부 일화와 덮개를 쥐었다" if not hole
                    else "🚨 %s장이 비었다 — 자를 의심하라, 지우지 마라" % hole))


def layers():
    """세 층 사이의 선을 센다 — 📜god↔god · 🎞️ep↔ep(거울) · 🎞️ep→🍇g(다이나모).

    ⚠️ 두 가지 수를 **같이** 찍는다. 언급(mention)은 적힌 [[ ]] 개수고,
       선(edge)은 중복을 접은 뒤다. 거울은 양쪽이 서로를 적으므로 쌍으로 접고
       (방향을 버리는 것이 여기선 의도다), 다이나모는 방향이 뜻이라 (ep,g) 로 접는다.
    """
    eps  = _basenames(EP_DIR, lambda f: f.startswith("ep"))
    gs   = _basenames(ELEM_DIR, lambda f: re.match(r"g[1-6]_", f) is not None)
    gods = _basenames(GOD_DIR, lambda f: True)

    거울, 다이나모, 밖 = set(), set(), 0
    거울_언급 = 다이나모_언급 = 0
    for f in sorted(os.listdir(EP_DIR)):
        nfc = unicodedata.normalize("NFC", f)
        if not (nfc.startswith("ep") and nfc.endswith(".md")):
            continue
        me, body = nfc[:-3], _read(EP_DIR, f)
        for t in _links(body, "🪞 거울"):
            거울_언급 += 1
            if t in eps and t != me:
                거울.add(frozenset((me, t)))
        for t in _links(body, "🔗 다이나모선"):
            다이나모_언급 += 1
            if t in gs:
                다이나모.add((me, t))
            else:
                밖 += 1

    신 = set()
    for f in sorted(os.listdir(GOD_DIR)) if os.path.isdir(GOD_DIR) else []:
        nfc = unicodedata.normalize("NFC", f)
        if not nfc.endswith(".md"):
            continue
        me = nfc[:-3]
        for t in _links(_read(GOD_DIR, f)):
            if t in gods and t != me:
                신.add(frozenset((me, t)))

    물린_g = {t for _, t in 다이나모}
    print("\n── 세 층 배선 (이슈 #117 코멘트의 숫자) ───────────────────────")
    # 📜 끼리의 선은 「같은 저자 안」과 「저자를 넘어」를 갈라야 뜻이 있다.
    # 2026-09-21 의 「읽은 것은 나란히 놓인다」는 **저자를 넘는 선이 드물다**는 말이지
    # 선이 하나도 없다는 말이 아니다 (당시 0선이었을 뿐).
    _author = lambda n: n.lstrip("📜").split("_")[0]
    안 = sum(1 for pr in 신 if len({_author(x) for x in pr}) == 1)
    print(f"  📜 god↔god   {len(신):>4}선   (신의전언 {len(gods)}편 · "
          f"같은 저자 안 {안} · 저자 넘는 선 {len(신) - 안})")
    print(f"  🎞️ ep↔ep     {len(거울):>4}선   (일화원소 {len(eps)}편 · 거울 언급 {거울_언급} → 쌍으로 접음)")
    print(f"  🎞️→🍇 다이나모 {len(다이나모):>4}선   (언급 {다이나모_언급} → (ep,g)로 접음"
          + (f" · 생각원소 밖 가리킴 {밖}" if 밖 else "") + ")")
    print(f"     물린 생각원소 {len(물린_g)}/{len(gs)}"
          f" — 안 물린 {len(gs) - len(물린_g)}편은 아직 겪은 것이 안 받친다")
    공 = 공표_2026_09_21
    now = dict(god=len(신), 거울=len(거울), 다이나모=len(다이나모))
    차 = {k: now[k] - 공[k] for k in 공}
    if any(차.values()):
        print(f"  🚨 공표값과 어긋난다 — god {공['god']}→{now['god']} · "
              f"거울 {공['거울']}→{now['거울']} · 다이나모 {공['다이나모']}→{now['다이나모']}")
        print("     이슈 #117 본문과 _채석장/4차소통/설계도/117_세층_촉매와말단기.md 를 이 수로 갈고 "
              "`공표` 를 오늘 값으로 다시 못 박아라.")
    else:
        print("  ✅ 공표값(2026-11-11)과 같다")


def recount():
    """🔗다이나모선(L3→L2)과 🪞거울(L3↔L3) 링크를 본문에서 세어 frontmatter에 박는다.
    손으로 센 값은 어긋난다 — 실측 2026-09-30: ep45(0 vs 3) · ep49(8 vs 13)."""
    changed = 0
    for fn in sorted(os.listdir(EP_DIR)):
        nfc = unicodedata.normalize("NFC", fn)
        if not (nfc.startswith("ep") and nfc.endswith(".md")):
            continue
        path = os.path.join(EP_DIR, fn)
        s = open(path, encoding="utf-8").read()
        end = s.index("\n---\n", 3) + 1
        fm, body = s[:end], s[end:]
        def count(title):
            m = re.search(rf"##\s*{title}[^\n]*\n(.*?)(?=\n##\s|\Z)", body, re.S)
            return len(re.findall(r"\[\[", m.group(1))) if m else 0
        wire, mirror = count("🔗 다이나모선"), count("🪞 거울")
        old = re.search(r"^배선:\s*(\d+)", fm, re.M)
        if not old or int(old.group(1)) != wire or f"거울: {mirror}" not in fm:
            changed += 1
            if old:
                print(f"  {nfc[:-3][:34]:<36} 배선 {old.group(1)}→{wire} · 거울 {mirror}")
        fm = re.sub(r"^배선:.*\n", f"배선: {wire}\n", fm, flags=re.M)
        fm = re.sub(r"^거울:.*\n", "", fm, flags=re.M)
        fm = fm[:-4] + f"거울: {mirror}\n---\n" if fm.endswith("---\n") else fm + f"거울: {mirror}\n"
        open(path, "w", encoding="utf-8").write(fm + body)
    print(f"✅ 재계수 완료 — 바뀐 원소 {changed}")


# ── 공표 규칙 (예측가능성 기준) ─────────────────────────────────────────────
# 협력자가 솔버 없이 손으로 재현하는 배정. 장 순서 = 둥지 → 이음새 → 새장,
# 각 장은 자기 극 후보 중 (방출 ↓ · 배선 ↓ · 번호 ↑) 상위.
# MCMF와 갈리는 자리가 곧 「이유 한 줄을 달아야 하는 배선」이다.
GREEDY_ORDER = [6, 7, 8, 9, 5, 10, 1, 2, 3, 4]

def greedy(eps):
    used, out = set(), {}
    for ch in GREEDY_ORDER:
        pole = CHAPTERS[ch]["극"]
        cand = [i for i, e in enumerate(eps)
                if i not in used and cost(e, ch) is not None
                and (pole == "*" or e["극"].startswith(pole))]
        cand.sort(key=lambda i: (-eps[i]["투향방출"], -eps[i]["배선"], eps[i]["번호"]))
        for i in cand[:CHAPTERS[ch]["자리"]]:
            out[i] = ch; used.add(i)
    return out


def solve(eps, costfn=cost):
    """min cost max flow 한 판. → (assign{i:(장,비용)}, edges{(i,장):비용}, flow, total)"""
    n = len(eps)
    S, T = 0, 1 + n + len(CHAPTERS)
    ch_idx = {ch: 1 + n + k for k, ch in enumerate(sorted(CHAPTERS))}
    mc = MCMF(T + 1)
    edges, eid = {}, {}
    for i, ep in enumerate(eps):
        mc.add(S, 1 + i, 1, 0)
        for ch in CHAPTERS:
            c = costfn(ep, ch)
            if c is not None:
                edges[(i, ch)] = c
                eid[(i, ch)] = len(mc.g[1 + i])
                mc.add(1 + i, ch_idx[ch], 1, c)
    for ch, meta in CHAPTERS.items():
        mc.add(ch_idx[ch], T, meta["자리"], 0)
    flow, total = mc.run(S, T)
    assign = {i: (ch, edges[(i, ch)]) for (i, ch), k in eid.items()
              if mc.g[1 + i][k][1] == 0}      # 용량 1이 다 쓰였다 = 이 변으로 흘렀다
    return assign, edges, flow, total


def margins(assign, edges):
    """🪦 은퇴 2026-10-11 — 쓰지 마라. move_loss() 를 쓴다.

    옛 여유 = (다른 장 중 최저비용) − (앉은 장 비용). **그 장이 꽉 찼는지 안 봤다.**
    꽉 찬 자리를 공짜인 척 비교해 억울함을 부풀렸고, 20자리 중 10을 🔴로 불렀다.
    정확히 재면(move_loss) 억울함은 10이 아니라 19다 — 짝짓기 자체가 동점이기 때문."""
    out = {}
    for i, (ch, c) in assign.items():
        alt = [cc for (j, c2), cc in edges.items() if j == i and c2 != ch]
        out[i] = (min(alt) - c) if alt else 99
    return out


def move_loss(eps, assign, total, flow):
    """이동손해 = (그 원소를 다른 장으로 **강제**했을 때 최저 총비용) − (지금 총비용).

    항상 ≥ 0 (지금이 최적이므로). **0 = 공짜로 옮길 수 있다 = 진짜 룰링 대상.**
    클수록 솔버 판단에 근거가 있다 = 자장이 손댈 자리가 아니다.

    ⚠️ 옛 「여유」는 *(다른 장 단독 최저비용) − (앉은 비용)* 이었다. 그 장에 **빈 자리가
       있는지 안 봤다.** 꽉 찬 자리를 공짜인 척 비교해 억울함을 부풀렸다 — 자가 틀렸다.
       (실측 2026-10-11: 옛 자는 20자리 중 10을 🔴로 불렀다. 새 자로는 아래 숫자.)"""
    out = {}
    n_ruled = sum(1 for i in assign if eps[i]["번호"] in RULINGS)
    for i, (ch, _) in assign.items():
        if eps[i]["번호"] in RULINGS:
            out[i] = None                      # 룰링된 자리는 재는 대상이 아니다
            continue
        num, best = eps[i]["번호"], None
        for ch2 in CHAPTERS:
            if ch2 == ch or cost(eps[i], ch2) is None:
                continue
            def forced(ep, c, _n=num, _c2=ch2):
                if ep["번호"] == _n:
                    return cost(ep, c) - PIN if c == _c2 else None
                return cost(ep, c)
            _, _, fl, t = solve(eps, forced)
            # 할인은 강제한 1개 + 이미 룰링된 자리들에 모두 얹혀 있다. 전부 되돌린다.
            d = (t + PIN * (n_ruled + 1)) - total
            best = d if best is None else min(best, d)
        out[i] = best
    return out


def audit(eps, assign, edges, total, flow):
    """세 기준으로 배선을 감사한다 (PDF §2 — robustness · simplicity · predictability)."""
    import random
    base = {i: ch for i, (ch, _) in assign.items()}

    # ① 견고성 — 투향방출 ±1 교란
    random.seed(0)
    flip = defaultdict(int)
    for _ in range(20):
        pert = [dict(e, 투향방출=max(0, e["투향방출"] + random.choice([-1, 0, 1]))) for e in eps]
        a, _, _, _ = solve(pert)
        a = {i: ch for i, (ch, _) in a.items()}
        for i in base:
            if a.get(i) != base[i]:
                flip[i] += 1
    stable = sum(1 for i in base if not flip[i])

    # ② 단순성 — 문턱 셋을 비용항으로 되돌리면 배정이 바뀌나
    def old(ep, ch):
        c = cost(ep, ch)
        if c is None:
            return None
        return c + (0 if ep["마찰"] else 3) + (0 if ep["증거"] else 1) + (0 if ep["연료"] else 1)
    a2, _, _, t2 = solve(eps, old)
    t2 += PIN * sum(1 for i in base if eps[i]["번호"] in RULINGS)   # 룰링 할인 되돌림
    moved = sum(1 for i in base if {j: ch for j, (ch, _) in a2.items()}.get(i) != base[i])

    # ③ 예측가능성 — 공표 규칙과 대조
    g = greedy(eps)
    agree = sum(1 for i in base if g.get(i) == base[i])

    # ⚠️ 옛 「여유」는 꽉 찬 자리를 공짜인 척 비교한 자다 — 이동손해로 갈았다.
    #    두 자를 같이 두면 다음 세션이 죽은 자로 산 결론을 끌어낸다.
    mg = move_loss(eps, assign, total, flow)
    tight = {i for i in base if mg[i] is not None and mg[i] <= 0}
    shaky = set(sorted(flip, key=lambda i: -flip[i])[:len(tight)]) if tight else set()
    mismatch = {i for i in base if g.get(i) != base[i]}
    union = (tight | shaky | mismatch) - {i for i in base if eps[i]["번호"] in RULINGS}

    # ④ 축퇴 — 감동이 짝짓기를 가릴 수 있나. c(a,X)+c(b,Y) == c(a,Y)+c(b,X) 이면 못 가린다.
    # ⚠️ 장 짝은 **한 번만** 센다. 검사식 c(a,X)+c(b,Y) == c(a,Y)+c(b,X) 는 X·Y 를
    #    바꿔도 같은 식이라, permutations 로 세면 전수가 정확히 두 겹이 된다
    #    (실측 2026-10-11: 4126 으로 보고했는데 구별되는 경우는 2063 이었다).
    # 구조식 = 같은극쌍×C(4,2) + 다른극쌍×C(2,2)  — 같은 극은 둥지1+새장1+이음새2 를
    #    공유하고, 다른 극은 이음새 2개만 공유한다. 룰링된 원소는 후보 장이 1개라 빠진다.
    import itertools
    same = diff = 0
    for i, j in itertools.combinations(range(len(eps)), 2):
        for X, Y in itertools.combinations(sorted(CHAPTERS), 2):
            q = (cost(eps[i], X), cost(eps[j], Y), cost(eps[i], Y), cost(eps[j], X))
            if None in q:
                continue
            same, diff = (same + 1, diff) if q[0] + q[1] == q[2] + q[3] else (same, diff + 1)

    print("\n── 배선 감사 (기준 넷) ───────────────────────────────────────")
    print(f"  ① 견고성   방출 ±1 교란 ×20 → 20회 내내 제자리 {stable}/{flow}")
    print(f"  ② 단순성   문턱 셋을 비용항으로 되돌림 → 배정 변화 {moved}/{flow} (총비용 {t2})")
    print(f"  ③ 예측성   공표 규칙(greedy) 일치 {agree}/{flow}")
    print(f"  ④ 축퇴     원소·장 맞교환 {same+diff}가지 중 총비용이 **바뀌는** 경우 {diff}"
          f"  (룰링 {len(RULINGS)}건은 후보가 1장이라 제외됨 — 이 수는 룰링이 쌓이면 줄어든다)")
    if diff == 0:
        print("     🚨 감동이 짝짓기를 하나도 못 가린다 = f(장)+g(원소) 로 쪼개진다.")
        print("        최소비용은 장식이고, 실제로 푸는 문제는 「61→20 선발」뿐이다.")
        print("        → 필요한 것은 max flow(극별 자리에 20개가 앉나) + 정렬(g 작은 순).")
        print(f"        → 짝짓기 {flow - len(RULINGS)}자리는 **전부** 자장 룰링 대상이다 (9가 아니다).")
    print(f"\n  📌 룰링된 자리 {len(RULINGS)} — 솔버가 아니라 자장이 정했다")
    for num, (ch, why) in sorted(RULINGS.items()):
        print(f"     ep{num:<3} →{ch:>2}장   {why}")
    print(f"\n  🔴 세 자가 가리키는 자리 {len(union)} (여유≤0 {len(tight)} · 흔들림 {len(shaky)} · 규칙불일치 {len(mismatch)})")
    for i in sorted(union, key=lambda i: eps[i]["번호"]):
        tag = "".join(t for t, st in (("견", tight), ("흔", shaky), ("예", mismatch)) if i in st)
        print(f"     [{tag:<6}] {eps[i]['이름'][:30]:<32} →{base[i]:>2}장 "
              f"이동손해 {mg[i]:>3} · 규칙 {g.get(i, '—')}")
    if union:
        print("  ↑ 이 자리들은 솔버가 정한 게 아니라 **자장이 이유 한 줄로 정해야 한다**")


# ── 한 장 그림 — 00_자리경합.html ────────────────────────────────────────────
# 글로 된 보고는 「누가 어디 앉았나」는 말해 주지만 **몇이 못 앉았나**를 못 보여 준다.
# 비어 있음은 그려야 보인다(00_사슬지도_비평v1 #2). 그래서 자리와 대기열을 같은 자 위에 둔다.
# ⚠️ 00_자리경합.html 은 생성물이다. 손으로 고치지 마라 — 이 파일을 고쳐라.
짝색 = {1: "#0026FB", 6: "#0026FB", 2: "#491786", 7: "#491786",
        3: "#F82218", 8: "#F82218", 4: "#006610", 9: "#006610",
        5: "#FFD53A", 10: "#FFD53A"}
노랑장 = {5, 10}          # 노랑은 면으로만 — 글자는 검정으로 얹는다(CLAUDE.md §1 짝색)


def html_out(eps, assign, gated, ml):
    import datetime, html as H
    OUT = os.path.join(EP_DIR, "00_자리경합.html")
    앉음 = {eps[i]["번호"]: (ch, c) for i, (ch, c) in assign.items()}
    문턱 = {eps[i]["번호"] for i in gated}
    이름 = {e["번호"]: e["이름"].split("_", 1)[1].replace("_", " ") for e in eps}
    번호들 = sorted(e["번호"] for e in eps)
    주제밖 = [n for n in 번호들 if n not in 주제장]
    대기 = {ch: [n for n in 번호들
                 if 주제장.get(n) == ch and n not in 앉음] for ch in CHAPTERS}
    칸수 = max(CHAPTERS[ch]["자리"] + len(대기[ch]) for ch in CHAPTERS)

    def 알(n, 참=True):
        """원소 하나를 한 칸으로. 참=앉은 자리 / 거짓=대기."""
        cls = "al seated" if 참 else ("al gated" if n in 문턱 else "al wait")
        return (f'<span class="{cls}" title="ep{n:02d} {H.escape(이름[n])}">'
                f'{n:02d}</span>')

    줄 = []
    for ch in sorted(CHAPTERS):
        자리 = CHAPTERS[ch]["자리"]
        앉은 = [n for n in 번호들 if 앉음.get(n, (None,))[0] == ch]
        빈자리 = 자리 - len(앉은)
        칸 = "".join(알(n) for n in 앉은) \
             + '<span class="al empty" title="빈 자리">·</span>' * 빈자리 \
             + '<span class="gap"></span>' \
             + "".join(알(n, False) for n in 대기[ch])
        c = 짝색[ch]
        줄.append(
            f'<tr style="--c:{c}">'
            f'<th><b>{ch}</b> {H.escape(CHAPTERS[ch]["이름"])}</th>'
            f'<td class="seats">{자리}</td>'
            f'<td class="cells{" ink" if ch in 노랑장 else ""}">{칸}</td>'
            f'<td class="q">{len(대기[ch]) or ""}</td></tr>')

    # 어느 장 줄에도 안 서는 편 — 보이게 두지 않으면 깔때기 숫자가 안 맞는다
    밖 = [n for n in 번호들 if n not in 앉음 and 주제장.get(n) is None]
    if 밖:
        칸 = '<span class="gap"></span>' + "".join(알(n, False) for n in 밖)
        줄.append(f'<tr style="--c:var(--dim)" class="out">'
                  f'<th>— 줄에도 없음</th><td class="seats">0</td>'
                  f'<td class="cells">{칸}</td><td class="q">{len(밖)}</td></tr>')

    총, 통과, 앉은수 = len(eps), len(eps) - len(문턱), len(앉음)
    밀림 = 통과 - 앉은수
    바 = lambda n: f"{n / 총 * 100:.1f}%"

    # 장부(frontmatter)에 적힌 값과 지금 솔버 값이 어긋난 편
    어긋 = []
    for n in 번호들:
        p = os.path.join(EP_DIR, next(e["file"] for e in eps if e["번호"] == n))
        mm = re.search(r"^투향장:\s*(.*)$", open(p, encoding="utf-8").read(), re.M)
        v = (mm.group(1).split("#")[0].strip() if mm else "")
        장부 = None if v in ("—", "", "·") else v
        솔버 = str(앉음[n][0]) if n in 앉음 else None
        if 장부 != 솔버:
            어긋.append((n, 장부 or "—", 솔버 or "—",
                         "주제장 밖" if n in 주제밖 else str(주제장.get(n) or "앉히지 않음")))

    gen1 = sorted(e["번호"] for e in eps if e["gen"] == 1)
    오늘 = datetime.date.today().isoformat()
    rows_어긋 = "".join(
        f"<tr><td>ep{n:02d}</td><td>{H.escape(이름[n])}</td>"
        f'<td class="n">{a}</td><td class="n">{b}</td><td class="n">{t}</td></tr>'
        for n, a, b, t in 어긋)

    open(OUT, "w", encoding="utf-8").write(f"""<!doctype html>
<meta charset="utf-8">
<title>투향 — 65편이 20자리를 두고 겨룬다</title>
<style>
:root {{ --bg:#fff; --ink:#15150f; --dim:#6b6b60; --line:#dcdcd2; --soft:#f6f6f1; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme=light]) {{
  --bg:#15150f; --ink:#f0f0e8; --dim:#9a9a8e; --line:#3a3a32; --soft:#1e1e17; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; padding:28px 16px 64px; background:var(--bg); color:var(--ink);
  font:15px/1.65 -apple-system,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;
  max-width:860px; margin-inline:auto; }}
h1 {{ font-size:25px; line-height:1.3; margin:0 0 4px }}
h2 {{ font-size:15px; margin:40px 0 10px; padding-bottom:6px;
  border-bottom:1px solid var(--line); letter-spacing:.02em }}
.sub {{ color:var(--dim); font-size:13px; margin:0 0 28px }}
.lead {{ font-size:17px; line-height:1.6; margin:0 0 6px }}
.lead b {{ font-size:21px }}
table {{ border-collapse:collapse; width:100% }}
th,td {{ padding:5px 6px; text-align:left; vertical-align:middle }}
tbody th {{ font-weight:600; white-space:nowrap; width:1%; font-size:13.5px;
  border-left:4px solid var(--c); padding-left:9px }}
td.seats,td.q {{ width:1%; text-align:right; color:var(--dim);
  font-variant-numeric:tabular-nums; font-size:12px; white-space:nowrap }}
td.q {{ color:var(--c); font-weight:700 }}
.cells {{ white-space:nowrap; font-size:0 }}
.al {{ display:inline-block; width:25px; height:22px; margin-right:3px;
  border-radius:4px; font:600 11px/22px ui-monospace,SFMono-Regular,Menlo,monospace;
  text-align:center; font-variant-numeric:tabular-nums }}
.seated {{ background:var(--c); color:#fff }}
.cells.ink .seated {{ color:#15150f }}
.empty {{ border:2px dashed var(--c); color:var(--c); line-height:18px; opacity:.55 }}
.wait {{ border:1px solid var(--line); color:var(--dim); background:var(--soft) }}
.gated {{ border:1px dashed var(--line); color:var(--dim); background:transparent; opacity:.6 }}
.gap {{ display:inline-block; width:14px }}
tr.out th {{ color:var(--dim); font-weight:500; font-style:italic }}
tr.out {{ border-top:1px solid var(--line) }}
.bars {{ margin:6px 0 0 }}
.bar {{ display:flex; align-items:center; gap:10px; margin:7px 0; font-size:13px }}
.bar .lab {{ width:128px; color:var(--dim); text-align:right; flex:none }}
.bar .tr {{ flex:1; background:var(--soft); height:26px; border-radius:4px;
  overflow:hidden; border:1px solid var(--line) }}
.bar .fill {{ display:block; height:100%; background:var(--ink); opacity:.30 }}
.bar .fill.mid {{ opacity:.60 }}
.bar .fill.hi {{ opacity:1 }}
.bar .num {{ width:46px; font-weight:700; font-variant-numeric:tabular-nums; flex:none }}
.note {{ color:var(--dim); font-size:13px; margin:10px 0 0 }}
.warn {{ border-left:3px solid #F82218; padding:2px 0 2px 12px; margin:14px 0 }}
table.grid td,table.grid th {{ border-bottom:1px solid var(--line); font-size:13px }}
table.grid td.n {{ text-align:center; font-variant-numeric:tabular-nums; width:1% ; white-space:nowrap }}
code {{ background:var(--soft); padding:1px 5px; border-radius:3px; font-size:12.5px }}
.legend {{ display:flex; gap:18px; flex-wrap:wrap; color:var(--dim); font-size:12.5px; margin:12px 0 0 }}
.legend span.al {{ margin-right:5px; vertical-align:-6px }}
</style>

<h1>65편이 20자리를 두고 겨룬다</h1>
<p class="sub">투향 일화원소 자리 배정 · {오늘} · <code>python3 .claude/baesun_mcmf.py --html</code> 가 찍는다</p>

<p class="lead">겪은 일은 <b>{총}</b>편인데 열 장에 놓인 의자는 <b>{sum(CHAPTERS[c]['자리'] for c in CHAPTERS)}</b>개다.
<b>{앉은수}</b>편이 앉고 <b>{총 - 앉은수}</b>편이 못 앉았다.</p>
<p class="note">못 앉은 이유는 둘로 갈린다 — <b>후보도 못 된 {len(문턱)}편</b>(마찰·연료 칸이 비어 심사 자체를 못 받는다)과,
<b>심사는 받고 밀린 {밀림}편</b>이다. 둘은 고치는 방법이 다르다.</p>

<h2>① 어디서 줄었나</h2>
<div class="bars">
  <div class="bar"><span class="lab">겪은 것</span>
    <span class="tr"><span class="fill" style="width:100%"></span></span><span class="num">{총}</span></div>
  <div class="bar"><span class="lab">심사 받을 자격</span>
    <span class="tr"><span class="fill mid" style="width:{바(통과)}"></span></span><span class="num">{통과}</span></div>
  <div class="bar"><span class="lab">자리에 앉음</span>
    <span class="tr"><span class="fill hi" style="width:{바(앉은수)}"></span></span><span class="num">{앉은수}</span></div>
</div>
<p class="note">같은 눈금 위의 세 막대다. 줄어든 폭이 곧 떨어진 수 — 문턱에서 {len(문턱)}, 자리 경합에서 {밀림}.</p>

<h2>② 열 장 좌석도 — 찬 자리와 줄 선 자리</h2>
<table>
<tbody>
{chr(10).join(줄)}
</tbody>
</table>
<div class="legend">
  <span><span class="al seated" style="--c:var(--dim);background:var(--dim);color:var(--bg)">00</span>앉았다</span>
  <span><span class="al empty" style="--c:var(--dim)">·</span>빈 자리</span>
  <span><span class="al wait">00</span>줄 섰다 (심사는 통과)</span>
  <span><span class="al gated">00</span>문턱 미달 — 줄에도 못 선다</span>
</div>
<p class="note">맨 오른쪽 숫자 = 그 장에 줄 선 편수(합 {sum(len(v) for v in 대기.values()) + len(밖)}). 왼쪽 숫자 = 의자 수.
앞쪽 네 장(새장)은 의자가 <b>하나씩</b>인데 줄은 서너 명씩이다.</p>

<h2>③ 문턱 미달 {len(문턱)}편 — 한 구간에 몰려 있다</h2>
<p>{len(gen1)}편이 <b>ep01~ep17</b>(결번 14 제외) 한 덩어리다. 이 구간이 <code>gen: 1</code> —
<code>마찰:</code>과 <code>연료:</code> 칸이 생기기 전에 쓰인 편들이다.
나머지 한 편은 ep40(<code>연료:</code>만 빔).</p>
<p class="warn">흩어진 빈칸이 아니라 <b>세대 경계</b>다. 열일곱을 하나씩 들여다볼 일이 아니라
<b>옛 서식을 새 서식으로 올리는 한 번의 작업</b>이다 — 그게 끝나면 후보가 {통과}→{통과 + len(문턱)}편이 된다.</p>

<h2>④ 장부와 솔버가 어긋난 {len(어긋)}편</h2>
<p><code>투향장:</code>은 솔버의 생성물인데, 마지막 <code>--write</code> 뒤에 값이 갈렸다.</p>
<table class="grid">
<thead><tr><th>편</th><th>제목</th><th class="n">장부</th><th class="n">솔버</th><th class="n">주제장</th></tr></thead>
<tbody>{rows_어긋}</tbody></table>
<p class="note">맨 끝 세 편(ep64·65·66)은 <code>주제장</code> dict에 항목이 아예 없다 —
솔버가 모르는 편이라 손으로 적힌 값이다. <code>--write</code> 를 돌리기 전에 그 셋을 dict에 넣어야 한다.</p>
""")
    print(f"\n🖼️  {OUT}")

def whatif(spec):
    """⛺️ 가정 — 다이나모선 한 가닥을 지우면 덮개가 어떻게 다시 앉나.

    쓰는 법:  python3 .claude/baesun_mcmf.py --whatif ep35:g5_07_순서를_타다
              python3 .claude/baesun_mcmf.py --whatif g2_05            (그 원소의 모든 가닥)

    왜 이 플래그가 생겼나 (2026-11-01) — 「NOCS 를 빼라」는 룰링을 적용하고 나서야
    g5_07 이 그 자리에 들어온 것을 알았다. **순서가 거꾸로였다.** 지우기 전에
    무엇이 대신 앉는지 보이면, 룰링이 손이 아니라 눈을 먼저 쓴다.

    ⚠️ 이 함수는 **자리(배선)를 다시 풀지 않는다.** 일화 20편은 그대로 두고
    덮개만 다시 집는다 — 다이나모선은 자리 비용에 안 들어가므로 그게 정확하다.
    일화를 빼고 싶으면 주제장/방출을 고쳐야 하고, 그건 다른 자다.
    """
    d = survivors()
    seated, covers = d["seated"], d["covers"]
    base = d["chosen"]
    ep, _, g = spec.partition(":")
    if not g:                                   # 원소만 줬다 — 접두사로 찾는다
        hits = [k for k in covers if k.startswith(ep)]
        if len(hits) != 1:
            print(f"🚨 「{ep}」로 시작하는 원소가 {len(hits)}개 — 이름을 더 적으세요: {hits[:5]}")
            return
        g, drop = hits[0], None
    else:
        hits = [k for k in covers if k.startswith(g)]
        if len(hits) != 1:
            print(f"🚨 「{g}」로 시작하는 원소가 {len(hits)}개 — 이름을 더 적으세요: {hits[:5]}")
            return
        g, drop = hits[0], ep
    if drop:   # 일화는 파일 이름 전체로 저장된다 — 「ep35」 같은 접두사를 펴 준다
        cand = sorted({e for v in covers.values() for e in v if e.startswith(drop)})
        if len(cand) != 1:
            print(f"🚨 「{drop}」로 시작하는 일화가 {len(cand)}편 — 이름을 더 적으세요: {cand[:5]}")
            return
        drop = cand[0]
    cut = dict((k, set(v)) for k, v in covers.items())
    if drop:  cut[g].discard(drop)
    else:     cut[g] = set()
    after, un2 = _greedy_cover(cut, seated)

    print(f"⛺️ 가정 — {'가닥 ' + drop + '→' + g if drop else '원소 ' + g + ' 전부'} 를 지우면")
    print(f"\n  자리를 받은 일화 {len(seated)}편은 그대로다 (배선은 안 다시 푼다)")
    print(f"  덮개 {len(base)} → {len(after)}")
    out, inn = [x for x in base if x not in after], [x for x in after if x not in base]
    for x in out: print(f"    − 빠짐 {x:44s} 덮던 일화 {sorted(covers[x] & seated)}")
    for x in inn: print(f"    + 들어옴 {x:42s} 덮는 일화 {sorted(cut[x] & seated)}")
    if not out and not inn:
        print("    = 안 바뀐다 — 그 가닥은 덮개 선택에 쓰이지 않았다(다른 원소가 이미 덮는다)")
    if un2:
        print(f"  🚨 안 덮인 불 {len(un2)} — {sorted(un2)}  (이 일화가 지면에서 받칠 것을 잃는다)")
    print("\n  읽는 법 — 일화가 자리를 지키는 한 **덮개에 빈칸은 안 생긴다.**")
    print("  원소를 그래프에서 정말로 내리려면 둘 중 하나다 —")
    print("    ① 그 일화의 🔗다이나모선에서 지운다 (여기서 재는 것)")
    print("    ② 그 일화가 자리를 잃게 한다 (주제장·방출을 고치는 다른 자)")


def main():
    if "--recount" in sys.argv:
        recount()
        return
    if "--layers" in sys.argv:
        layers()
        return
    if "--cover" in sys.argv:
        cover()
        return
    if "--whatif" in sys.argv:
        i = sys.argv.index("--whatif")
        if i + 1 >= len(sys.argv):
            print("쓰는 법: --whatif ep35:g5_07  또는  --whatif g2_05")
            return
        whatif(sys.argv[i + 1])
        return
    global 조준값, COHORT
    eps = read_eps()
    n_ep = len(eps)
    if 분리:
        keep, 조준값 = 조준값, 0              # ① 선발 — 적합을 끄고 화력으로만
        sel, _, _, _ = solve(eps)
        조준값, COHORT = keep, {eps[i]["번호"] for i in sel}
        g0 = lambda e: -((3 if e["배선"] >= 5 else (1 if e["배선"] > 0 else 0)) + e["투향방출"])
        컷 = max(g0(eps[i]) for i in sel)
        턱 = [e["이름"] for i, e in enumerate(eps) if i not in sel and g0(e) == 컷
              and all(e[g] for g in GATES)]
        print(f"① 선발 — 화력(배선·방출)으로 {len(sel)}편. 컷 g={컷} · "
              f"같은 화력인데 못 들어온 원소 {len(턱)}편 {'(선발도 그만큼 동점이다)' if 턱 else ''}")
        print(f"② 배정 — 그 {len(sel)}편 안에서만 조준(적합)으로 자리를 가른다\n")
    assign, edges, flow, total = solve(eps)
    # 룰링 할인을 보고에서 되돌린다 — 룰링이 총비용을 깎은 것처럼 보이면 거짓이다
    pinned = {i for i in assign if eps[i]["번호"] in RULINGS}
    total += PIN * len(pinned)
    assign = {i: (ch, c + PIN if i in pinned else c) for i, (ch, c) in assign.items()}
    edges = {(i, ch): (c + PIN if i in pinned else c) for (i, ch), c in edges.items()}
    ml = move_loss(eps, assign, total, flow)
    best = {i: min((c for (j, ch), c in edges.items() if j == i), default=None)
            for i in range(n_ep)}
    # 문턱 미달 = 마찰·증거·연료가 빈 원소. ① 선발에서 떨어진 것과 섞지 않는다.
    gated = [i for i, e in enumerate(eps) if not all(e[g] for g in GATES)]

    layers()

    print(f"원소 {n_ep} · 자리 {sum(m['자리'] for m in CHAPTERS.values())} · 배정 {flow} · 총비용 {total}")
    print(f"평균비용 {total/flow:.2f} · 문턱 미달 {len(gated)} (마찰·증거·연료 중 빈 칸)"
          + (f" · 문턱은 넘었으나 ① 선발에서 밀림 {n_ep - len(gated) - flow}" if 분리 else ""))
    seats = sum(m["자리"] for m in CHAPTERS.values())
    f_of = lambda ch: 자리값 - 2 * (4 if ch in NEST else (2 if ch in CAGE else 1))
    # ⚠️ sg 를 total − sf 로 빼서 구하면 검산이 아니다 (같은 식을 두 번 쓰는 것).
    #    원소 쪽 항을 frontmatter 에서 **독립으로** 합산해 남는 값을 본다.
    g_of = lambda e: -((3 if e["배선"] >= 5 else (1 if e["배선"] > 0 else 0)) + e["투향방출"])
    sf = sum(f_of(ch) for ch, _ in assign.values())
    sg = sum(g_of(eps[i]) for i in assign)
    print(f"자리값(유보가격) {자리값} — 감동이 이걸 못 넘으면 자리를 비운다 (지금 빈 자리 "
          f"{seats - flow})")
    resid = total - (sf + sg)
    print(f"쪼개짐 검산 — 총비용 {total} vs Σf(쓰인 자리) {sf} + Σg(앉은 원소) {sg} = {sf+sg}"
          f"  → 남는 값 {resid}")
    print("   남는 값 0 = 감동에 원소×장 항이 없다 = 짝짓기가 전부 동점. "
          "0이 아니면 그만큼이 조준(짝짓기가 실제로 가려지는 폭)이다.")
    print("   ※ Σf 가 상수 80 인 것은 20자리가 다 찼을 때뿐 — 자리가 비면 줄어든다.")
    # 감동 세 항의 실제 폭 = 아무도 선언하지 않은 가중치
    fits = sorted({자리값 - 2 * f for f in (1, 2, 4)})
    wires = sorted({-(3 if e["배선"] >= 5 else (1 if e["배선"] > 0 else 0)) for e in eps})
    emits = sorted({-e["투향방출"] for e in eps if e["투향방출"]})
    print(f"감동 항별 폭 — 자리종류 {max(fits)-min(fits)} · 배선 {max(wires)-min(wires)} "
          f"· 방출 {max(emits)-min(emits)}   🙋‍♀️ 폭 = 가중치인데 선언된 적이 없다\n")
    pinned_names = {eps[i]["이름"] for i in pinned}
    by_ch = defaultdict(list)
    for i, (ch, c) in assign.items():
        by_ch[ch].append((c, ml[i], eps[i]["이름"]))
    for ch in sorted(CHAPTERS):
        if by_ch[ch]:
            print(f"[{ch:>2}장 {CHAPTERS[ch]['이름']}]  자리 {CHAPTERS[ch]['자리']}")
            for c, m, nm in sorted(by_ch[ch], key=lambda t: (t[0], t[2])):
                mark = "📌" if nm in pinned_names else ("🔴" if m == 0 else "  ")
                print(f"     비용 {c:>3} · 이동손해 {'  —' if m is None else f'{m:>3}'} {mark}  {nm}")
    wait = sorted((best[i], eps[i]["이름"]) for i in range(n_ep)
                  if i not in assign and best[i] is not None)
    print(f"\n대기 화약가루 {len(wait)} (최선 비용 낮은 순 앞 10)")
    for c, nm in wait[:10]:
        print(f"     최선 {c:>3}  {nm}")

    if "--html" in sys.argv:
        html_out(eps, assign, gated, ml)

    if "--audit" in sys.argv:
        audit(eps, assign, edges, total, flow)

    if "--write" in sys.argv:
        for i, ep in enumerate(eps):
            p = os.path.join(EP_DIR, ep["file"])
            s = open(p, encoding="utf-8").read()
            end = s.index("\n---\n", 3) + 1
            fm, rest = s[:end], s[end:]
            # 투향여유는 은퇴한 자 — 키까지 지운다. 남겨 두면 다음 세션이 그걸 읽는다.
            for k in ("투향장", "투향비용", "투향여유", "투향이동손해", "투향룰링"):
                fm = re.sub(rf"^{k}:.*\n", "", fm, flags=re.M)
            ch = assign[i][0] if i in assign else None
            c = assign[i][1] if i in assign else best[i]
            fm += (f'투향장: {ch if ch else "—"}\n'
                   f'투향비용: {c if c is not None else "—"}\n'
                   f'투향이동손해: {"—" if i not in assign or ml[i] is None else ml[i]}\n')
            if ep["번호"] in RULINGS:
                fm += f'투향룰링: "{RULINGS[ep["번호"]][1]}"\n'
            open(p, "w", encoding="utf-8").write(fm + rest)
        print(f"\n✅ {n_ep}편 frontmatter에 투향장·투향비용·투향이동손해 기록 "
              f"(투향여유 키는 삭제 — 은퇴한 자)")

if __name__ == "__main__":
    main()
