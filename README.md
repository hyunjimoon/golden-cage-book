# 투향: Opening the Golden Cage

책 홈페이지: https://hyunjimoon.github.io/golden-cage-book/

> 왜 이른 자원이 창업을 가두는가 — 그리고 어떻게 그 새장을 *둥지*로 여는가.

**저자**: 문현지 (Angie Hyunji Moon) 
**출판**: 민음사 (검토 중)
**근거 논문**: 
1. [Golden Cage: Paradox of Early Funding and Growth](https://github.com/hyunjimoon/golden-cage-thesis) — MIT SM Thesis (2026), N = 168,011
> abstract: Flexibility predicts startup growth, yet the funding that enables growth systematically suppresses flexibility. The mechanism is belief-based sorting. When founders commit to specific strategies, investors who share those beliefs fund; skeptics self-select out. The resulting board lacks cognitive diversity to advocate pivots. I formalize this phenomena as golden cage theory: founders cannot reposition because governance lacks advocates for alternatives.

> Analyzing 168,011 U.S. ventures, I establish three empirical regularities. First, early funding predicts less repositioning. Second, repositioning predicts success. Third, the early funding and growth correlation varies systematically by industry: negative where dominant designs constrain exploration (e.g. Hardware and Mobility), neutral or positive where uncertainty releases the cage (Software and Quantum).

> Three contributions emerge. Empirically, the funding-growth paradox holds as a robust regularity across 168,011 ventures. Theoretically, belief-based sorting in governance explains why commitment and flexibility trade off. Prescriptively, founders can balance commitment and flexibility with the 3S framework: Scope (commit to thesis, not architecture—moderate breadth outperforms both extremes), Sequencing (stage capital from non-dilutive to thesisdriven VC, delaying governance lock-in until market signals clarify), and Synchronization (match capability investment to market validation, avoiding the traps of over-building or over-promising).

2. Optimal Ignorance: Designing Promise Precision to Convert Uncertainty into Adaptive Capacity (2025)
> abstract: Entrepreneurial ventures must calibrate promise precision—the specificity of external commitments that mobilize stakeholders yet constrain adaptation. Precision creates a fundamental tension: specific promises mobilize resources but kill adaptability; vague promises preserve options but repel stakeholders. This paper develops the Optimal Ignorance Level (OIL) framework that controls judgment and belief precision into one variable by formulating success probability as a random variable and objective value. The solution prescribes a threshold rule: maintain strategic ambiguity until value exceeds integration costs fourfold, then earn precision proportional to the square root of the value-to-cost ratio. The key intuition is that entrepreneurial ignorance, when honestly signaled through vague promises, preserves adaptive capacity. A comparative case (Tesla vs. Better Place) illustrates how trajectories of precision, value, and information integration cost align with the model’s predictions, while acknowledging contextual confounds.

3. STRAP-ping Stakeholders for Entrepreneurial Decision-Making (2025)
> abstract: Entrepreneurs face extreme uncertainty across multiple stakeholder domains, yet lack principled frameworks to coordinate these uncertainties eﬃciently. This research introduces STRAP (Strategic Threshold Resolution for Actionable Priorities), a decision framework built on a fundamental equivalence: systematically reducing uncertainty directly increases venture success probability. STRAP transforms entrepreneurship into a structured cycle of Perception (modeling stakeholder uncertainties using Bayesian logit models) and Action (selecting experiments that maximize information gain per resource unit). The framework explicitly maps venture attributes to stakeholder choice probabilities, quantiﬁes uncertainty through information-theoretic entropy, and optimizes sequential action selection through a primal-dual formulation. My key contribution demonstrates that successful ventures should target the “bottleneck” uncertainty oﬀering the highest uncertainty reduction per resource unit while balancing stakeholder thresholds through dual variables. Using Sublime Systems’ low-carbon cement commercialization as a case study, I demonstrate that STRAP-guided decision making achieves a I2% reduction in weighted uncertainty while meeting all stakeholder thresholds.


---

## 한 문장

창업가가 **자기를 설득하며 지은 새장**(1–4장)을, **101호**(5장)에서 한 번 멈춰 세고, **중심을 지나 뒤집어** **이해관계자를 이해하는 둥지**(6–9장)로 바꾼 뒤 제자리에서 닫는(10장) — **열 장짜리 창업 소설**.

> 변환은 **점 반전(−I)이지 회전이 아니다.** 거울짝 다섯(1↔6 · 2↔7 · 3↔8 · 4↔9 · 5↔10)의 중점이 **한 점(101호)**에서 만나는 것이 그 증명이다.
> 짝마다 바뀌는 것은 **한 축 위의 한 항**뿐이다 — 믿음 → **실험**(6장) · 관조 → **분포**(7장) · 확신 → **협상**(8장) · 작란 → **명명**(9장). 일연이 *正*을 *遺*로 비튼 것과 같은 크기의 변경이다.
> *쓰는 법*은 소설이 아니라 부록이 맡는다(부록 3 「한글같은 삶소설」).

## 핵심 방정식

```
dG/dF = (dG/dR) × (dR/dF) = (+) × (−) = (−)
```

방향전환(R)이 성장(G)을 만들지만, 자원(F)이 방향전환 억압. 미국 벤처 168,011건 실증 — 방향 바꾼 자(Movers)가 머문 자(Stayers)보다 **2.60배** 성장.

## 열 장 — 네 극과 진단 질문

『투향』은 한 장마다 **문학의 은유**로 갇힘을 진단하고 **운영의 수(數)**로 그 진단을 보정한다. 두 척추가 각 장 *안에서* 만나므로 밖에서 볼 표는 하나다 — **무엇을 빌렸고 누가 그것을 되재는가**, 그리고 **그 장이 당신에게 묻는 것**.

| 장 | 극 — 1부가 쌓고, 2부가 짝을 붙인다 | 그 장이 당신에게 묻는 것 |
| :--- | :--- | :--- |
| **1장 🪞 거울새장** — 엠마 | **D** 욕망 *(빌린 욕망)* | 이 백로그 티켓·욕망은 경쟁사를 흉내 낸 '빌린 욕망'인가, **볼 사람을 빼도 남는** 사용자 진짜 통증인가? |
| **2장 🔭 망원경새장** — 살리나 | **+B** 믿음 *(빌린 품위)* | 완벽한 관조적 시장 진단이 오히려 '한 발도 안 떼고 **움직이지 않을 알리바이**'로 쓰이고 있지 않은가? |
| **3장 💒 스테인굴레스** — 파늘루 | **+A** 행동 *(빌린 확신)* | 바깥이 안 보이는 투명한 확신의 유리벽에 갇혀, 타인의 렌즈 속 굴절률과 **되물음을 모욕으로** 치부하고 있지 않은가? |
| **4장 ⏱️ 시계새장** — 로빈슨 | **+M** 자 *(빌린 자)* · 🏝️섬 | 단 하나의 정사(正史) 자(尺)로 시간을 톱니바퀴처럼 묶어두어, 정사가 버린 **유사(遺事)의 유실**을 방치하고 있지 않은가? |
| **5장 🐀 101₂호** — 윈스턴 | **·점** — 한 축(다↔세)만 남는다 | 불탄 잿더미에서 **빚의 장부를 펴고** 내 모델의 잔재를 직시하며 멈추었는가? |
| **6장 🦋 나비둥지** — 송 릴링 | **D–U** 🦋 사용자 | 다운로드 수치가 아니라 사용자가 **매일 자발적으로 켜는 손가락**으로 욕망의 정렬을 재고 있는가? |
| **7장 🧅 튤립둥지** — 코르넬리우스 | **B–T** 🧅 기술자 | 100% 확신을 버리고 구근 세 알을 손바닥에 나누어 올려, **99%로 반증을 견디며** 매일 보정하는가? |
| **8장 🌫️ 안개둥지** — 아우구스토 | **A–I** 🌫️ 투자자 | 과잉 자본의 늪(dG/dF가 음수인 구간)을 차단하고, **미래 옵션을 지키는 전략적 모호성**을 수호하고 있는가? |
| **9장 🐦‍⬛ 까마귀둥지** — 일연 | **M–C** 🐦‍⬛ 협력자 · ◉상 | 잰 값을 겨루는 게 아니라 **자(尺) 자체를 공동 감사**하여, 다음 사람에게 비워둔 채 빛을 넘기고 있는가? |
| **10장 🧫 101₃호** — 세다 | **↗향** — 셋으로 갈린다 | 책장을 닫는 순간 손바닥 위에서 **다시 1장으로** 회환하되, 그 방을 닫지 않고 **다음 사람이 자기 이름으로 주울 자리**를 비워 두었는가? |

> **극이 곧 거울짝이다** — **D** 1↔6 🦋 · **B** 2↔7 🧅 · **A** 3↔8 🌫️ · **M** 4↔9 🐦‍⬛ · 회전축 5↔10. 1부는 네 극을 **쌓고**(D → +B → +A → +M), 2부가 거기에 짝을 하나씩 붙여 **축**을 세운다. 그래서 짝의 앞쪽은 *나에게* 묻고, 뒤쪽은 같은 물음을 *이해관계자에게* 되묻는다 — 이해관계자는 2부의 산출물이라 1~4장 행에는 서지 않는다.
> **여덟 장 × 4칸(경험·지식·사례·실천) = 32칸에 빈칸 0** — 2026-11-08 실측. 5·10장은 칸이 아니라 **자리 수**다([#45](https://github.com/hyunjimoon/golden-cage-book/issues/45)). 2·3·4장의 §2 지식은 초고라 저자 검토 전이다. 비는 칸이 생기면 **채우지 않고 ⚓로 표시한다** — 빈칸은 산출물이고, 채점에서는 calibration gap(0점)이다.
> 재는 법 = [`RUBRIC.md`](RUBRIC.md). 렌즈당 0–3점 · 10장 × 4렌즈 × 3점 = **120점** — 채점은 **열 장 전부를 네 렌즈로** 보므로, 위 표의 극 배정과는 다른 자다.

> **핵심 이동 — 과거의 고통을 미래의 연료로.** 1–4장에서 *나에게* 한 진단(모르고 빌린 욕망·접어버린 가능성·그어버린 선·훔친 불)이, 6–9장에서 *이해관계자에게* 되쓰인다. 남을 이해하는 유일한 길은, 내가 먼저 그 새장에 갇혀봤다는 것. **상처가 렌즈가 된다.**

## 가치제안 — 알은 빼고, 둥지만 공유한다

완성된 제품(알)을 보여주는 대신, 사용자·기술자·투자자·협력자 *각자의 알*을 품을 수 있는 **빈 둥지**(가치제안서)를 공유한다. 둥지가 넷을 모두 품으면 — 책은 새장이 아니라 둥지가 된다.

## 방법 — 짓고 · 펼치고 · 내보내고 · 다시 못박다

이 책은 **Nail → Scale → Sail → re-Nail**의 규율로 쓰인다. 외부(독자·편집자)의 반응이 내 예측과 어긋난 자리를 덮지 않고, 그 오차를 설계로 되먹여 다시 못박는다(*보정, calibration*). 완성이 아니라 *보정*을 마쳤을 때, 함께 넓힐 자격이 생긴다.

## 함께 여실 분께 (예비 협력자)

- **편집·출판** — 원고를 독자의 "삶을 바꾸는 이야기"로 벼리는 생산과정
- **번역·해외진출** — 각 둥지 장이 그 작품의 언어권 시장으로 열리는 입구
- **AI 활용 제작** — 다중 에이전트로 외서검토·감정궤적·구조정합을 돕는 파이프라인

문의는 이슈 또는 저자에게. *하나로 접기 전에 옵션을 펼쳐 두는 편이, 결국 더 빨리 좋은 책에 닿는다고 믿습니다.*

## 디렉토리

```
chapters/       ch0 도입 · ch1–4 새장 · ch5 회전축 · ch6–9 둥지 · ch10 에필로그
appendices/     부록 (낭만의심 3부작 · 한글같은 삶소설 · 프롬프팅 예시 · 산업별 빚)
interactive/    인터랙티브 (주기율표, 감정궤적, 본문 뷰어)
docs/           CHANGELOG · INTENT
img/            다이어그램
```
---

*빌린 것을 갚으면, 새장이 둥지가 된다.*
