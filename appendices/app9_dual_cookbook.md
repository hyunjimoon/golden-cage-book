---
modified:
  - 2026-05-04
  - 2026-05-18T04:42:33+09:00
type: 부록
---

# 부록 9 — D·S Dual AI Cookbook

> 책의 *다·세*를 *작업 도구*로 reified한 실천 가이드.
> *답이 하나면 직감, 여럿이면 과학이다.*

---

## 0. 수학 정전 — 광학 거울상 = Convex 쌍대성 (2026-05-18 추가)

> 5장 hub의 *두 거울 마주봄*은 직관 비유이자 *Convex Analysis 정전*. 책 전체 *1↔5 mirror pair, 9→5 ouroboros, dG/dF=(−)*가 **광학-쌍대 동형**으로 형식화 가능.

### 0.1 핵심 매핑 5

| 광학 거울 | Convex 쌍대 | 학자 anchor |
|:--|:--|:--|
| 거울 두 번 = 원본 (mirror² = identity) | Fenchel biconjugate: f** = f (if f convex) | Rockafellar 1970 *Convex Analysis* |
| Handedness reversal (좌↔우) | Primal min ↔ Dual max | LP/convex 정전 |
| 허상 (virtual image, 거울 뒤 가상 위치) | Dual variable λ = *shadow price* (현실 변수 아닌 수식상 존재) | KKT 1951 |
| Fermat's principle (빛 = 최소 시간 경로) | Primal optimization (시조 형태) | Fermat 1657 |
| Aberration (수차) | Non-convex *duality gap* > 0 | Bauschke-Combettes 2017 |

→ 결정적 정전: **Nemirovski-Yudin 1983 *Mirror Descent***. 광학 비유로 명명된 algorithm. Update rule: `x_{t+1} = ∇h*(∇h(x_t) − η·∇f(x_t))` — *dual space에서 gradient + primal로 mirror back*.

### 0.2 황금새장 thesis 수학 재정식화

**Primal (창업자 문제)**:
```
maximize    G(x)             # Growth (회사 가치)
subject to  F(x) ≤ B          # Funding ≤ budget
           R(x) ≥ R_min       # Reposition capability ≥ 최소
           x ∈ X               # 결정변수
```

**Dual (투자자 문제)**:
```
maximize_λ  g(λ_F, λ_R) = inf_x L(x, λ)
            L(x, λ) = G(x) − λ_F·(F(x) − B) − λ_R·(R_min − R(x))
subject to  λ_F, λ_R ≥ 0
```

**dG/dF = (−)** 의 형식적 진단:
- *함의*: F-constraint의 *shadow price λ_F가 음수* → 추가 funding이 *G 감소*
- *메커니즘*: F 증가 → R constraint 활성화 → R 감소 → G 감소
- *Strong duality 깨짐*: primal max G* < dual max g(λ)* → **duality gap > 0 = cage**
- *KKT complementary slackness 위반*: λ_F·(F* − B) ≠ 0 (자본이 *남거나 부족한데 활용 안 됨*)

### 0.3 1↔5 mirror pair = Fenchel biconjugate

```
1장 거울새장 (엠마)          ↔   5장 거울둥지 (자장 + 윈스턴)
직접 욕망 추구                =   primal: max U(가지고 싶음)
빌린 욕망 → 빚 누적           =   constraint: g(x) ≤ 0 (시장 신호 무시 비용)
       ↓ 한 축 비틂           =   Legendre transform
일의 거울 = 가치·meaning      =   dual: min cost of misalignment
*함께 짓는 frame*             =   shadow price = V(가치)

두 거울이 마주봄              =   f** = f (Fenchel biconjugate)
                              = *primal과 dual이 한 자리에서 만남*
                              = *strong duality* (gap = 0)
```

→ **두 거울 사이 황금 깃털** (책 표지 image) = *primal과 dual이 마주보는 자리에 떠 있는 optimal solution (KKT point)*.

### 0.4 Founder-Investor 쌍대 게임

| 자리 | Founder | Investor |
|:--|:--|:--|
| 푸는 문제 | Primal (max G) | Dual (max ROI = G/F) |
| 직접 통제 | 결정변수 x (product·hiring·strategy) | Dual variable λ (term sheet 조건) |
| 간접 통제 | term sheet 거절·재협상 | board seat·milestone·option pool |
| 보는 시선 | *내가 짓는 회사* | *내 자본의 함수* |

→ **Strong duality (gap = 0) 조건** — 둘이 *같은 KKT point*에서 만남:
- λ_F · (F(x) − B) = 0 (funding 정확히 사용)
- λ_R · (R_min − R(x)) = 0 (reposition 정확히 보존)
- 즉 **funding이 reposition을 잡아먹지 않음**

→ 실무 정전: [[Zalman_founder_investor]] — Elizabeth Joy Zalman + Jerry Neumann *Founder Vs Investor* (2024). 7장 *Red and the Wolf* (두 저자 직접 대화) = *primal-dual 만남*의 책 안 정전.

### 0.5 NOCS Diamond × 쌍대 호응

NOCS D↔Se 게이트 = *strong duality* 자리:
- C·N 위 (선택지 보존) = *primal feasible region*
- S·O 아래 (실행 확정) = *dual optimal solution*
- D↔Se 통과 = *KKT condition 충족 = complementary slackness*
- Type code (cc·cx·xr·xa 4 cell) = *2×2 dual space partitioning*. Amazon = *xa* (expand + add)

상세: [[NOCS_diamond_syntax]]

### 0.6 참고 더 읽기

- Rockafellar, *Convex Analysis* (Princeton, 1970) — Fenchel biconjugate 정전
- Nemirovski-Yudin, *Problem Complexity and Method Efficiency in Optimization* (Wiley, 1983) — Mirror Descent
- Boyd-Vandenberghe, *Convex Optimization* (Cambridge, 2004) — KKT·shadow price 교과서
- Bauschke-Combettes, *Convex Analysis and Monotone Operator Theory in Hilbert Spaces* (Springer, 2017) — 현대 정전
- [[Zalman_founder_investor]] — *primal-dual 비대칭의 실무 정전*

---

### 0.7 입구 — 어제 AI 1명을 만났습니다. 오늘 2명을 데려왔습니다.

본문 7장 *AI 실습 — 확신 Distribution*에서 한 점 vs 분포를 익혔어요. 그런데 *AI 한 명*과의 분포 사고는 한계가 있어요 — *나의 직감 + AI 한 명의 답* = 두 점. 한 점보다 낫지만 *방향*은 약해요.

***AI 두 명*을 데려오면**:
- **D** (Designer·디자이너) — 현장·위험 구역을 본다 = 책의 **다** (rotor, 몸으로 안다)
- **S** (Scientist·사이언티스트) — 규정·미달 구역을 본다 = 책의 **세** (stator, 거리 둬 본다)

두 점이 *입체적 방향*을 만들어요. **D·S = 책의 다·세 직계 derivative**.

---

## 1부. 같이 보자 — 같은 공정, 다른 시선

### 원리

```
   D (현장 위험 구역)        S (규정 미달 구역)
        ↘                       ↙
          [합의된 기준]
              ↑
        차이는 불량이 아니라 *신호*
```

### 월요일 행동

> **내 판단의 기준이 *D 관점*인지 *S 관점*인지 *먼저 말하기*.**

이 한 행동이 — *합의된 기준*을 만드는 첫 박자.

### 실습 1 — 점 하나는 직감, 점 둘은 방향

| 칸 | 적기 |
|:--|:--|
| **나의 초기 판단** | _______________________ |
| **Claude(D)의 답** | _______________________ |
| **발견한 차이점** | _______________________ |

**월요일 행동**: 내 판단 1개를 Claude에게 같은 질문으로 확인해보기.

### 실습 1 시범 사례 — Toluene 화학약품 재고 관리

| 측면 | **생산팀 (D 관점)** | **컴플라이언스/안전팀 (S 관점)** |
|:--|:--|:--|
| Primary Goal | 라인 가동 유지 | 규정 위반 0건 |
| 인용 | *"안전 재고 확보가 우선. 유연한 관리가 필요하다."* | *"보안/유통기한 초과 시 사고 위험. 즉각 폐기해야 한다."* |
| 충돌 지점 | **운영의 현실 vs 안전 규정** | |

**월요일 행동**: 이번 주 부서 간(D와 S) 충돌이 발생한 *현장 사례 1건* 메모하기.

→ **차이를 *불량* 아니라 *신호*로 읽는 동작**이 핵심. 책 6장 *Crucial Third Position*(안과 밖의 경계 위)의 작업 도구화.

---

## 2부. 같이 키우자 — 빈 곳에 기준을 채우다

### 원리

```
[현장 모르는 D] + [기준 모르는 S]
              ↓
      [공정 규정 문서 입력]
              ↓
       판단이 정교해진다
```

### 메커니즘

D는 *현장 위험*을 보지만 *규정의 정확한 텍스트*를 모름. S는 *규정의 정확한 텍스트*를 보지만 *현장 운영의 현실*을 모름.

→ **두 agent에게 *공통의 reference document*를 주면** — 각자의 약점이 메워져요. 서로의 *맹점*에 *기준*이 채워집니다.

### 월요일 행동

> **Claude 프로젝트에 *우리 공정 규정 문서* 1개 업로드하기.**

Claude의 Projects 기능을 쓰면 — D와 S 두 conversation 모두 *같은 문서*를 reference. 두 agent의 *판단이 정교해지고*, *합의된 기준*이 더 빨리 떠오릅니다.

### 실습 2 — D·S Dual AI 프로토콜 (4 단계)

```
Step 1. Q (질문 정의)
  "이 결정에 대해 어떤 정보가 필요한가?"

Step 2. D (현장 시선)
  Claude with D persona:
  "당신은 현장 디자이너입니다. 운영의 현실에서 이 질문을 보세요."

Step 3. S (규정 시선)
  Claude with S persona:
  "당신은 규정 사이언티스트입니다. 규정·기준에서 이 질문을 보세요."

Step 4. 합의 (Author 자장)
  D와 S의 답을 *나란히 놓고*, 차이점에서 *신호*를 읽어 합의된 기준을 적는다.
```

### 실습 3 — D·S Persona Prompt 템플릿

**D Prompt (현장 시선)**:
```
당신은 [도메인]의 현장 디자이너입니다.
이 질문을 *운영의 현실 + 위험 구역* 관점에서 답해주세요.
규정의 텍스트보다 *실제 작동*과 *유연성*을 우선합니다.

질문: [Q]
```

**S Prompt (규정 시선)**:
```
당신은 [도메인]의 규정 사이언티스트입니다.
이 질문을 *규정·기준 + 미달 구역* 관점에서 답해주세요.
현장 유연성보다 *정확한 기준*과 *위반 0건*을 우선합니다.

질문: [Q]
```

### 실습 4 — Q→D→S→융합 4 step

매일 한 결정에 대해:

1. *질문* 1줄 적기 (구체적·답할 수 있는 형태로)
2. *D Claude*에 입력 → 답 받기 (3-5 줄로)
3. *S Claude*에 입력 → 답 받기 (3-5 줄로)
4. **차이점**을 보고 — *합의된 기준* 1줄 적기

→ **30분 안에 *3 시점 (자장·D·S)* 분포를 확보**. 한 점이 아니라 *입체적 방향*.

---

## 3부. Plan v2 Multi-Agent Delegation과 결합 (5/4 결정)

이 cookbook은 5월 4일 결정된 *Multi-Agent Delegation Plan v2* (도구/agent_delegation_v1_3voice.md) 와 동형:

| Plan v2 | AIS framework | 책 mapping |
|:--|:--|:--|
| **Author** (자장+main LLM) | 합의 자장 | 다·세 voice 통합자 |
| **Verifier** (🔴 fact-check) | S agent (규정·정확) | 세 (거리 둬 본다) |
| **Curator** (sync·정리) | — (역할 후순위) | (작업 인프라) |
| (Maker = D·작가) | D agent (현장·실행) | 다 (몸으로 안다) |

→ **D·S = 책 다·세의 *작업 분업 형태*. 책의 *원리*가 *실천*으로 reified.**

### 실용 적용

- **Phase 3 ★ task별**: Author = D (작가 직관) / Verifier = S (사실·정합) / Curator = (sync 인프라)
- **★C Ørsted vs 포스코 dry run** (5/4 commit 8129dd29): *D·S 분업으로 paired case* 작성한 것이 직접 사례
- **NotebookLM 슬라이드** (★E deliverable): D·S 두 agent에게 다른 instruction → 두 결과 비교 → 합의

---

## 4부. 책 thesis와의 정합

| 책 chapter·thesis | AIS·D·S 형태 |
|:--|:--|
| 1장 거울새장 (모방욕망) | D·S 없이 한 점 — 빌린 욕망 |
| 5장 ★멈춤 (알면서 입기) | D 답 받고 *바로 안 따름* (★멈춤) |
| 6장 자기 서사 (Crucial Third Position) | D·S 두 자리에서 *경계 위* 작가 자리 |
| **7장 분포 사고 (PLoT)** | **점 1개 → 점 2개 → 입체적 방향**. 직접 정합 ★ |
| 8장 책임 (Phase 1+2) | D·S 합의로 *부순 자리에 새 거울 띄우기* |

→ **AIS가 가장 정합하는 chapter는 7장**. 본문 7장 4.2 *AI 실습 확장*에서 호명하고 — 본 부록에서 cookbook 풀어쓰기.

---

## 5부. 메타 — 왜 *D·S*인가

### 책 character의 자연 derivative

자장의 책에는 두 voice가 있어요 — **다 (몸으로 안다, rotor) + 세 (거리 둬 본다, stator)**. NotebookLM이 책을 학습하면 — 자연스럽게 *D (Designer)·S (Scientist)*로 reified.

이건 *우연*이 아니라 *책의 형식이 작업 도구로 변환된* 자연스러운 흐름. 책의 *서사*가 *분업*으로 굳어진 것.

### 박혜진 편집자에게 보일 때

이 cookbook은 *책 본문의 실천 도구*. 박혜진 미팅에서 — *책의 다·세*가 *현장 도구 D·S*가 되는 자리를 보여주면, **책이 *읽고 끝나는* 것이 아니라 *매일 작동하는* 도구임을 입증**.

★E 박혜진 deliverable 묶음의 *실용 컴포넌트*.

---

## 6부. 다음 trigger

- [ ] 7장 4.2 본문에 1 단락 호명 추가
- [ ] 본 부록 + 5/4 NotebookLM 슬라이드 통합 (★E deliverable)
- [ ] *공정 규정 문서* 후보 — 자장의 *작업 SSOT* (vault structure) 업로드 실험
- [ ] 실습 1·2·3·4 month-long trial → 결과를 *부록 9 v2*에 반영

---

*문서 버전: v1*
*작성: 자장 + main LLM, 2026-05-04*
*근거: AIS Dual AI Framework PDF (제조 현장을 위한 AI 협력 가이드 Day 2, NotebookLM 2026-05-04)*
*책 정합: 7장 *언어를 합의하라* 직접 적용*
*다음 갱신: month-long trial 후 v2*
