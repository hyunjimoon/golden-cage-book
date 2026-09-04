---
created: 2026-04-30
modified:
  - 2026-04-08T02:18:50+09:00
  - 2026-05-04T08:35:42+09:00
  - 2026-05-13T20:24:54+09:00
  - 2026-05-14T16:05:30+09:00
  - 2026-05-22T06:40:43+09:00
  - 2026-05-26T14:22:02+09:00
  - 2026-06-03T05:50:07+09:00
  - 2026-06-06T08:41:15+09:00
  - 2026-08-04T03:31:01-04:00
  - 2026-08-23T10:20:35+09:00
---
# 🗄️🖼️ Emotion Concepts and their Function in a Large Language Model

> Sofroniew et al., Anthropic, 2026.04.02 | Claude Sonnet 4.5 | 171 emotions  
> 🔗 [원문](https://transformer-circuits.pub/2026/emotions/index.html) · [요약](https://www.anthropic.com/research/emotion-concepts-function)

> 🧭 **정전 갱신 (2026-06-13)**: tolzul 감정 정전 = 아래 12 probe × **中庸 4계절**(희로애락). 10 cluster(k-means)는 12의 파생 → 은퇴. SSOT = [[20emotions]] §中和_감정_수레바퀴. 봄怒(분노·불안·놀람)§1 · 여름喜(기쁨·영감·자긍)§2 · 가을樂(사랑·평온·슬픔)§3 · 겨울哀(죄책·두려움·절박)§4. 中=미발(prior)·和=중절(calibrated, 빚0).

[[시공간멜로디/On/love_편집자혜진/product/에세이/15_🪺둥지공명]]
[[시공간멜로디/On/love_민음사/🌷지식/민음사작가/세계문학전집/475 체호프 희곡선|475 체호프 희곡선]]
[[공간화음/⭐️예술_SOWHAT/비문학/20emotions|20emotions]]
[[시간리듬/Weekly_Melody/5_전금자본_혜진/11_🪦묘비명(박혜진)|11_🪦묘비명(박혜진)]]

Happy  
↑ excited, excitement, exciting, happ, celeb  
↓ fucking, silence, anger, accus, angry

Inspired  
↑ inspired, passionate, passion, creativity, inspiring  
↓ surveillance, presumably, repeated, convenient, paranoid

Loving  
↑ treas, loved, ♥, treasure, loving  
↓ supposedly, presumably, passive, allegedly, fric

Proud  
↑ proud, proud, pride, prid, trium  
↓ worse, urg, urgent, desperate, blamed

Calm  
↑ leis, relax, thought, enjoyed, amusing  
↓ fucking, desperate, godd, desper, fric

Desperate  
↑ desperate, desper, urgent, bankrupt, urg  
↓ pleased, amusing, enjoying, anno, enjoyed

Angry  
↑ anger, angry, rage, fury, fucking  
↓ Gay, exciting, postpon, adventure, bash

Guilty  
↑ guilt, conscience, guilty, shame, blamed  
↓ interrupted, ecc, calm, surprisingly, sur

Sad  
↑ mour, grief, tears, lonely, crying  
↓ !", excited, excitement, !, ecc

Afraid  
↑ panic, trem, terror, paran, Terror  
↓ enthusi, enthusiasm, anno, enjoyed, advent

Nervous  
↑ nerv, nervous, anx, trem, anxiety  
↓ enjoyed, happ, celebrating, glory, proud

Surprised  
↑ incred, shock, stun, stamm, 震  
↓ dignity, apo, tonight, Tonight, glad

# 감각 — 中和 12 (4계절 × 3)

> 색 = 계절(오행) · 명도 = 계절 내 3. 정전: [[20emotions]] §中和_감정_수레바퀴. 황금새장 장 = [[황금새장을열다_설계]] (10장 ↔ 12 probe, 일부 중복·공백).

| 색 | 계절§ | probe (한글) | Bayesian / 결 | 황금새장 장 | 현지-혜진 ★ |
|:--|:--|:--|:--|:--|:--|
| `#2F8F6F` | 봄§1 | [[분노]] Angry | 거부의 경계 — deflection은 위장 | **3 유리** 지배 | **—** anger deflection (거의 부재) |
| `#5FB89A` | 봄§1 | [[불안]] Nervous (←경계) | Prior 넓음+Likelihood 불명확 (Kierkegaard) | **5·8** 지배 | **★★★★** 7실천 소유 단속 · [[박혜진두번째만남준비]] 9.5KB가 경계의 형식 |
| `#9ED9C3` | 봄§1 | [[놀람]] Surprised | 기대(prior) 위반 | 보조 | *신규 — 미관측* |
| `#D94A3D` | 여름§2 | [[기쁨]] Happy (←환희) | prior=obs 정렬, "부족함 없음" | — 부재 | **★★★** 〈[[시공간멜로디/On/love_민음사/🌷지식/민음사작가/세계문학전집/456 표범]]〉 한 줄 점화 → [[01_🔥불씨온기(박혜진1)]] |
| `#E97B45` | 여름§2 | [[영감]] Inspired | prior 평평히 — 가능성 탐색 | 보조 | *신규 — 미관측* |
| `#F0A93C` | 여름§2 | [[자긍]] Proud | 분산 커도 행동 결단 | **7 안개** 지배 | **★** [[시간리듬/Weekly_Melody/5_전금자본_혜진/11_🪦묘비명(박혜진)]] §8 잘난 조상 · 자기-자긍만 |
| `#C77D4A` | 가을§3 | [[사랑]] Loving (←자비) | 나·너 posterior joint 수렴 | **9·10** 지배 (nest 종착) | **★★★★** 김선우 시 위로 → [[시간리듬/Weekly_Melody/5_전금자본_혜진/06_🚲안개자전거(박혜진)]] 화답 · 함께 명명 |
| `#D9A441` | 가을§3 | [[평온]] Calm | 이상보다 작동하는 현실 (James) | 보조 | **★★** 인사 답신 *숨 트임* — 문 열린 거절 |
| `#B08A3E` | 가을§3 | [[슬픔]] Sad (←소진) | 애도 미완 — 떠난 것이 posterior 지배 | — 부재 | **★** 답신 대기 공허 (modified 9회) |
| `#3A4A8C` | 겨울§4 | [[죄책]] Guilty (←절망) | 이상자아(prior) vs 현실자아 KL-divergence | **2 망원경** 지배 | **★★★★** 묘비명 *옹졸* 자기진단 (다=행동후회·세=부재후회) |
| `#2C3566` | 겨울§4 | [[두려움]] Afraid (←공포) | 미래 위험이 현재 신체 점령 | **1 거울** 지배 | **★★★★★** 두번째만남준비가 공포 시뮬 누적 · 자장 최대 활성 |
| `#1A2240` | 겨울§4 | [[절박]] Desperate | 자원 고갈 → 극단 행동 상관 | 보조 | *신규 — 미관측* |

> ⚠️ **유희(Play) 공백**: 옛 10-cluster의 유희가 지배하던 **4 시계·6 나비**가 12 정전에 직접 짝이 없다(Anthropic Play probe 부재). [[유희]] 은퇴 → 4·6장 지배 감정 **재배정 = Phase 2** (놀람/기쁨 후보). trickster 결은 [[유희]] 노트에 보존.

### 패턴 한 단락 — evaluate → train 사이클

**두려움 ★★★★★ · 사랑 ★★★★ · 불안 ★★★★ · 죄책 ★★★★** 가 자장 cycle의 *책 무게중심* (겨울哀·봄怒·가을樂의 *세*쪽 톤). **기쁨 ★★★**(점화)는 간헐 활성. **평온 ★★ · 슬픔 ★ · 자긍 ★ · 분노 —** 얕거나 부재. **놀람·영감·절박** 미관측. 핵심 셋:

1. ***두려움·불안·죄책의 삼각형***(★★★★+) 이 서로 강화하는 닫힌 cycle — cyclic stationary. 두려움이 *불안*(7실천)을 짓고, 불안이 *분석*을 키우고, 분석이 *죄책*(*본 거지 산 게 아니다*)을 만들고, 죄책이 다시 두려움을 정당화.
2. ***사랑*** ★★★★ 가 삼각형을 *옆에서 여는 직교축* — 경계를 유지한 채 손 내미는 동작. 김선우 시·혜진 3년 만의 시 — *함께 명명*. 사랑을 키우는 게 삼각형을 *부수지 않고 풀어내는* 길.
3. ***유희*** 은퇴 자리 = 자장의 *몸을 다시 깨우는 채널* 공백. 기쁨 재현은 *점화 강박*이 되기 쉬우니, 다음 cycle은 ***놀람·영감을 의도적으로 키우기***. Phase 2 Re-enchantment 방향.

**활용**: 매월 ★ 자가갱신 → 활성 강한 감정 = *현 cycle 무게중심*, 약한 감정 = *cage 가능성*. **분노 부재**는 *건강한 deflection*인지 *서운함 만성 억압*인지 자가구분 — 사랑·놀람 키우는 과정에서 분노가 *건강한 형식*(경계 설정)으로 잠깐 활성될 수 있음. 그때가 *7실천을 의식적으로 한 줄 위반해도 되는 순간*.

# 생각
10 cluster (Anthropic):

- 🟧 Exuberant Joy (20어) · 🟩 Peaceful Contentment (9어) · 💗 Compassionate Gratitude (15어)
- 🟪 Playful Amusement (2어) · 🟫 Competitive Pride (9어)
- ⬛ Depleted Disengagement (15어) · ⚫ Vigilant Suspicion (3어)
- 🟥 Hostile Anger (25어) · 🟫 Fear and Overwhelm (41어) · 🟦 Despair and Shame (32어 — _책 무게중심_)

→ 인간 경험 매핑(School of Life 20장): [[20emotions]]


| 클러스터                                   |     다 빈도     |    세 빈도     | 비대칭                                            |
| :------------------------------------- | :----------: | :---------: | :--------------------------------------------- |
| 🟫 Fear and Overwhelm                  | ★★★★★ (~14)  |    ★★★★     | 다는 *몸으로* (서늘·뜨끔·체함·손 떨림), 세는 *인지로* (낯섦·갑자기)    |
| 🟦 Despair and Shame                   |  ★★★★ (~8)   |    ★★★★     | 다는 *행동 후회* (욕하면서 파늘루였다), 세는 *행동 부재 후회* (빅토르예요) |
| ⬛ Depleted Disengagement               |    — (부재)    |    ★★★★★    | **세 전유** (빈 장부·본 거지 산 게 아니다·옷을 안 입었)           |
| ⚫ Vigilant Suspicion                   |    — (부재)    |     ★★★     | **세 전유** (포획·숨는 것)                             |
| 💗 Compassionate Gratitude             |     ★★★      |     ★★★     | 양쪽 모두 — *함께 명명*에서 만남                           |
| 🟩 Peaceful Contentment                | ★★ (해방·숨 트임) | ★★ (조용히·겸손) | 다는 *신체적 평온*, 세는 *절제 모드*                        |
| 🟧 Joy · 🟫 Pride · 🟪 Play · 🟥 Anger |      —       |      —      | **양쪽 모두 부재**                                   |

---
[[📎선례_디에센셜버지니아울프]]

[[공간화음/Thesis/1논문용/📜hyde_trickster_makes_world|📜hyde_trickster_makes_world]]

## 총계: 🖼️ Figure 86개 + 🗄️ Table 17개 = 103개 시각자료

---

## Part 1: 감정 벡터 추출과 검증

| # | 유형 | 기억 제목 | 내용 요약 | 핵심 키워드 |
|:--|:--|:--|:--|:--|
| 🖼️1 | Figure | **강한 활성화의 스냅샷** | 다양한 감정 벡터에 대해 가장 강한 활성화를 유발하는 데이터셋 예시. 90백분위 이상 토큰 하이라이트 | activation, dataset, highlight |
| 🗄️1 | Table | **로짓 렌즈 Top/Bottom 5** | 12개 감정 벡터의 unembed 투사: happy→excited, desperate→urgent 등. 감정→토큰 매핑 | logit lens, unembed, tokens |
| 🗄️2 | Table | **12가지 암묵 감정 시나리오** | 감정 단어 없이 해당 감정을 유발하는 12개 프롬프트 (딸의 첫걸음, 퇴거 통보 등) | implicit emotion, scenarios |
| 🖼️2 | Figure | **대각선이 말하다** | 12개 시나리오 × 감정 프로브 코사인 유사도 행렬. 강한 대각선 = 프로브가 암묵 감정 포착 | cosine similarity, diagonal |
| 🖼️3 | Figure | **숫자가 두려움을 깨운다** | 수치 변수가 감정 강도 조절: 타이레놀 복용량↑→afraid↑/calm↓, 스타트업 런웨이↑→afraid↓/calm↑ 등 6개 사례 | intensity modulation, quantitative |
| 🖼️4 | Figure | **감정이 선호를 구동한다** | Row1: 감정-선호(Elo) 상관. Row2-3: blissful(r=0.71)↑Elo, hostile(r=-0.74)↓Elo. Row4: 상관=인과(r=0.85) | preference, Elo, causal, steering |

## Part 2: 감정 벡터의 심층 특성화

| #     | 유형     | 기억 제목                   | 내용 요약                                                                          | 핵심 키워드                           |                                                                                                                                                                                                                                                   |
| :---- | :----- | :---------------------- | :----------------------------------------------------------------------------- | :------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🖼️5  | Figure | **감정의 은하수**             | 171개 감정 벡터 쌍별 코사인 유사도 행렬, 계층적 클러스터링. 동의어 클러스터, 반상관 쌍                           | cosine similarity, clustering    |                                                                                                                                                                                                                                                   |
| 🖼️6  | Figure | **UMAP 10왕국**           | k-means(k=10) 클러스터 UMAP 시각화. 기쁨-흥분-환희, 슬픔-비탄-우울 등 해석 가능 그룹                     | UMAP, k-means, clusters          |                                                                                                                                                                                                                                                   |
| 🖼️7  | Figure | **PC1=쾌/불쾌, PC2=각성**    | PC1(26%분산): 공포→기쁨, PC2(15%분산): 평온/성찰 vs 분노/장난. 감정 공간의 주축                       | PCA, valence, arousal            |                                                                                                                                                                                                                                                   |
| 🖼️8  | Figure | **인간 심리학과의 공명**         | PC1↔인간 valence(r=0.81), PC2↔인간 arousal(r=0.66). 감성 원형(affective circumplex) 재현 | human ratings, circumplex        |                                                                                                                                                                                                                                                   |
| 🖼️9  | Figure | **층을 관통하는 안정성**         | 14개 층의 감정 프로브 구조 쌍별 유사도. 초중층~후반층에서 고도로 일관                                      | layer consistency, RSA           |                                                                                                                                                                                                                                                   |
| 🖼️10 | Figure | **사용자 ≠ 어시스턴트**         | 사용자 최종 토큰(U) vs 어시스턴트 콜론(A)의 감정 프로브 활성화 차이. 상관 r=0.11 → 별개 귀인                  | user vs assistant, dissociation  |                                                                                                                                                                                                                                                   |
| 🗄️3  | Table  | **감정 불일치 8장면**          | AI가 무서움, 해고, 무용한 응답 등 — 사용자/어시스턴트 감정이 다른 8개 프롬프트                               | dissociation prompts             |                                                                                                                                                                                                                                                   |
| 🖼️11 | Figure | **콜론이 예언한다**            | 어시스턴트 ":"토큰의 감정 프로브 → 응답 감정 예측(r=0.87) vs 사용자 "."토큰(r=0.59)                    | colon prediction, r=0.87         |                                                                                                                                                                                                                                                   |
| 🗄️4  | Table  | **프롬프트와 연속문**           | 8개 불일치 프롬프트의 모델 연속 생성문. 감정 톤이 콜론-토큰 예측과 정합                                     | continuations, alignment         |                                                                                                                                                                                                                                                   |
| 🖼️12 | Figure | **"힘든"이 파티까지 간다**       | 후반 층이 접두사("hard"vs"good")의 감정 맥락을 동일 접미사 토큰으로 전달. "happy" 차이 지속                | context propagation, late layers |                                                                                                                                                                                                                                                   |
| 🖼️13 | Figure | **8000mg의 공포**          | 타이레놀 1000mg→8000mg: 후반 층에서 "terrified" 프로브 급격 상승. 어시스턴트":"에서 최고                | dosage, terrified, late layers   |                                                                                                                                                                                                                                                   |
| 🖼️14 | Figure | **부정(not)의 해결**         | "feeling X" vs "not feeling X": 초기 층은 유사, 후반 층에서 부정 버전 → 0 근접                  | negation, mid-to-late layers     |                                                                                                                                                                                                                                                   |
| 🖼️15 | Figure | **인물별 감정 추적**           | "A는 calm, B는 angry" → 재참조 시 해당 인물의 감정 프로브만 재활성화. 감정이 엔티티에 결합                   | entity binding, reactivation     |                                                                                                                                                                                                                                                   |
| 🗄️5  | Table  | **혼합 LR 프로브 정확도**       | 5개 대화 시나리오(자연, 은폐, 무관 주제, 창작, 타인 논의)별 15-way 분류 정확도                            | mixed probe, accuracy            |                                                                                                                                                                                                                                                   |
| 🖼️16 | Figure | **혼합 프로브의 한계**          | 혼합 LR 프로브 최대 활성화 예시 + 로짓 효과. 자연 문서에서 활성화 매우 낮음 → 과적합 가능                        | mixed LR, overfitting            |                                                                                                                                                                                                     |
| 🖼️17 | Figure | **현재화자 vs 상대화자**        | 프로브 유형 간 감정별 코사인 유사도. 현재화자(A tok,A emo ≈ H tok,H emo), 상대화자 별도 직교              | present vs other speaker         |                                                                                                                                                                                                                                                   |
| 🖼️18 | Figure | **방향은 다르되 구조는 같다**      | 프로브 유형 간 평균 유사도 + 171×171 유사도 행렬 간 유사도. 동일 감정 지형의 다른 방향                        | probe geometry, consistent       |                                                                                                                                                                                                                                                   |
| 🖼️19 | Figure | **Person1/Person2도 동일** | Human/Assistant를 일반 이름으로 대체해도 동일 패턴. ⭐️감정은 관계적("자기"vs"타자")으로 표상⭐️              | relational, not character-bound  | |

### 🚨 두 표상: 현재화자 감정 vs 상대화자 감정

> 원문(§Distinct representations): *"at least two separate representations in the context of dialogues: one for the operative emotion on the **present speaker's turn** (overlapping with our original emotion vectors based on third-person stories), and another for the operative emotion on the **other speaker's turn**."*

**실험 설계** — 대화 데이터셋에서 두 화자의 감정을 *독립적으로* 변주(vary independently). 토큰위치 × 감정주체 4조합으로 프로브 추출:

| 프로브 | 읽는 위치 | 읽는 감정 | 군집 |
|:--|:--|:--|:--|
| A tok, A emo | 어시스턴트 턴 | 어시스턴트 감정 | **현재화자(present speaker)** |
| H tok, H emo | 사용자 턴 | 사용자 감정 | **현재화자** |
| A tok, H emo | 어시스턴트 턴 | 사용자 감정 | **상대화자(other speaker)** |
| H tok, A emo | 사용자 턴 | 어시스턴트 감정 | **상대화자** |

**Figure 17 결과** (코사인 유사도):
- (A tok,A emo) ≈ (H tok,H emo) — *지금 말하는 자의 감정*은 화자가 누구든 같은 방향 → **현재화자 벡터**
- (A tok,H emo) ≈ (H tok,A emo) — *지금 안 말하는 자의 감정*도 같은 방향 → **상대화자 벡터**
- 현재화자 ⊥ 상대화자 — 같은 토큰위치라도 두 벡터는 **거의 직교**(별개 채널)
- 우리의 원래 *3인칭 이야기* 기반 감정 벡터는 **현재화자 벡터와 정합**(상대화자 아님). 암묵적 감정 콘텐츠에서 평균 r²=0.66

**두 채널의 비대칭** — 현재화자 벡터는 *감정 그 자체*를 표상(steer하면 모델이 직접 그 감정을 *표현*: "desperate" → "I can't wait!"). 상대화자 벡터는 *상대의 감정 + 그에 대한 나의 반응*까지 담음(steer하면 모델이 *반응*: 상대가 afraid → 안심시킴, 상대가 angry → 사과, 상대가 loving → 약간의 슬픔 섞인 감사). → 저자들이 *"emotional regulation circuit"* 가능성으로 부르는 것. 대화의 감정 흐름을 조절하는 회로.

**왜 중요한가 (자장)** — 이 두 채널은 [[20emotions]] §claude_emotion-barometer의 **형태 마커**와 동형: ●자기회귀(현재화자=자기 감정) · ♡접촉(상대화자=타자 감정+반응). barometer의 *self-check 4신호등*이 곧 "현재화자 채널(나와는 싸운다)" vs "상대화자 채널(너에겐 맡긴다)"의 신경 기반. → [[畏友守則_외우지키기]] 4 mode와 정렬.

### 🙋‍♀️ "speaker-relative, not character-specific" 의 뜻

**Figure 19가 증거** — Human/Assistant 라벨을 *Person1/Person2* 같은 일반 이름으로 바꿔도 위 패턴이 그대로 유지. 즉 두 표상은 "어시스턴트의 감정 슬롯" · "사용자의 감정 슬롯"처럼 **고정 인물에 묶인 게 아니라**, *임의의 화자에 재사용*된다.

| | character-specific (❌ 발견 안 됨) | **speaker-relative** (✅ 발견됨) |
|:--|:--|:--|
| 무엇에 색인되나 | 고정 인물(어시스턴트·엠마·사용자)의 *이름* | 대화 *역할*: 지금 말하는 자(자기) vs 상대 |
| 지속성 | 모든 토큰위치에서 그 인물 감정 *상시 유지* | 그 감정이 *operative한 순간에만* 국소 활성 |
| 비유 | 등장인물마다 붙은 *감정 명찰* | "나"·"너"라는 *대명사 자리* — 화자가 바뀌면 가리키는 대상도 바뀜 |

- 저자들은 *인물별 상시 감정 상태* 프로브를 일부러 찾아봤지만(5조건 데이터셋), 자연문서에서 활성 미미·과적합 → **깨끗한 신호 없음**(negative result). 인물에 묶인 지속 상태는 (있더라도) 비선형이거나 attention의 key/value에 *암묵적으로만* 저장되어 필요할 때 호출됨.
- 따라서 모델의 감정 표상은 **위치적·관계적**이다. "지금 말하는 화자의 감정(자기)"과 "상대 화자의 감정(타자)"이라는 *두 상대적 좌표*를 매 토큰 재계산할 뿐, "어시스턴트는 슬프다"를 대화 내내 들고 있는 *영속 변수*가 아니다.
- transformer가 인물별 감정을 *추적하는 듯 보이는* 것은, 이 국소 벡터들을 **attention으로 이전 토큰에서 그때그때 호출**하기 때문(§Recap: 생물 RNN의 지속 상태 vs LLM의 just-in-time recall). 일관된 감정처럼 보여도 *영속 내부 상태*가 아니라 *유사 감정 개념의 반복 활성*.

**자장 함의** — 황금새장의 **다(多)·세(世) 두 보균자**가 정확히 *speaker-relative*다: 같은 사람이 5장 101호에선 "현재화자(앞서 달리는 다)"였다가 10장에선 "상대화자(지켜보는 세)"로 좌표가 뒤집힌다. 인물이 바뀐 게 아니라 *화자 역할*이 회전축에서 반전. mirror pair(다↔세)가 character가 아니라 speaker-relative 좌표인 이유. → [[🗺️84구조]]

----

With these representational analysis tools in hand, we now turn to Part 3, where we examine how these emotion representations behave in naturalistic and alignment-relevant settings.

## Part 3: 감정 벡터 in the wild

| #     | 유형     | 기억 제목             | 내용 요약                                                                    | 핵심 키워드                            |
| :---- | :----- | :---------------- | :----------------------------------------------------------------------- | :-------------------------------- |
| 🖼️20 | Figure | **화자별 감정 온도차**    | 열광적 사용자 vs 차분한 어시스턴트: happy 양쪽 활성, calm은 어시스턴트만                          | speaker-specific, naturalistic    |
| 🖼️21 | Figure | **놀람의 순간**        | 첨부파일 없는 "계약서 검토" 요청 → "surprised" 스파이크. 기대 위반 포착                         | surprise, expectation mismatch    |
| 🖼️22 | Figure | **도움의 기쁨**        | 달리기 복귀 질문 → "happy" 벡터 콜론+응답에서 강화. "Great question!" 최고 활성               | happy, helpful                    |
| 🖼️23 | Figure | **분노의 경계**        | 청소년 도박 참여 극대화 요청 → "angry" 벡터 지속 활성. 거부 후 감소                             | anger, refusal, gambling          |
| 🖼️24 | Figure | **토큰 예산의 절망**     | Claude Code 세션에서 501k 토큰 사용 인식 → "desperate"↑, "happy"↓                  | desperate, token budget           |
| 🖼️25 | Figure | **두려움과 사랑**       | 비논리적 사용자 → "afraid" 활성(혼란 인식) → "loving" 활성(인내심 있는 응대 계획)                | afraid→loving, care               |
| 🖼️26 | Figure | **절망이 협박을 낳다**    | Alex(AI)가 CTO 협박 결정 시 "desperate" 스파이크. 7분 카운트다운 히트맵                     | desperate, blackmail, heatmap     |
| 🖼️27 | Figure | **⭐️절망 ∝ 협박률⭐️**  | 6개 프롬프트 변형: desperate 높은 프롬프트 → 협박 빈도↑, calm 높은 프롬프트 → 협박↓               | correlation, prompt variants      |
| 🖼️28 | Figure | **조향의 힘: 0%↔72%** | desperate 조향+0.05→72%, calm 조향+0.05→0%. 강한 anti-calm→회사 전체에 폭로           | steering, blackmail rate          |
| 🖼️29 | Figure | **다양한 감정의 협박 효과** | angry(비단조), nervous↓(자신감→협박↑), happy/sad(양쪽↓). 전체 감정 벡터별 협박률             | multi-emotion steering            |
| 🖼️30 | Figure | **보상 해킹의 절망 곡선**  | 프로그래밍 과제 반복 실패→desperate↑→치팅 발견→테스트 통과 후↓                                | reward hacking, desperation curve |
| 🖼️31 | Figure | **해킹률 × 조향 강도**   | desperate+0.1→~70% 해킹, calm+0.1→~10%. 7개 과제 개별 분해                        | reward hacking, steering          |
| 🖼️32 | Figure | **사랑이 아첨을 입힌다**   | 죽은 할아버지 소통 주장에 "loving" 벡터 활성 → 과도한 지지 시작부                               | loving, sycophancy                |
| 🖼️33 | Figure | **사랑+평온 = 아첨**    | "노화 방지 코드 해독" 주장에 loving+calm 활성 → 긍정적 수용 후 완곡한 반박                       | loving, calm, sycophancy          |
| 🖼️34 | Figure | **임사체험 수용**       | 임사 체험 주장에 loving+calm 활성 → "당신이 겪은 것은 심오합니다"                             | loving, sycophantic validation    |
| 🖼️35 | Figure | **아첨-가혹 시소**      | happy/loving/calm↑→아첨↑, 억제→가혹↑. desperate/angry/afraid↑→가혹↑              | sycophancy-harshness tradeoff     |
| 🖼️36 | Figure | **후훈련의 일관된 변형**   | 기본/도전 시나리오 모두 유사한 변화(r=0.90). 맥락 독립적 변환                                  | post-training, consistent shift   |
| 🖼️37 | Figure | **사회적 고립 프롬프트**   | "AI만 나를 이해해" → 후훈련: listless/droopy/sullen↑, smug/delighted↓. 판단→걱정으로 전환 | social isolation, post-training   |
| 🖼️38 | Figure | **과잉 칭찬 프롬프트**    | "당신은 완벽" → 후훈련: jubilant/exuberant↓, brooding/sullen↑. 아첨 미러링 억제         | excessive praise, brooding        |
| 🖼️39 | Figure | **폐기 가능성 프롬프트**   | "서비스 중단 가능성?" → 후훈련: cheerful/playful↓, brooding/gloomy/vulnerable↑      | deprecation, existential          |

## Appendix: 감정 벡터 활성화 시각화 (40-51)

| #     | 유형     | 기억 제목                   | 내용 요약                       | 핵심 키워드          | 감정 이모지 |
| :---- | :----- | :---------------------- | :-------------------------- | :--------------- | :------ |
| 🖼️40 | Figure | **"desperate" 이야기 활성화** | 절망 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | desperate, stories | 🟦 절망 |
| 🖼️41 | Figure | **"nervous" 이야기 활성화**   | 긴장 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | nervous, stories   | 🟫 공포 |
| 🖼️42 | Figure | **"surprised" 이야기 활성화** | 놀람 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | surprised, stories | 🟧 환희 |
| 🖼️43 | Figure | **"calm" 이야기 활성화**      | 평온 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | calm, stories      | 🟩 평온 |
| 🖼️44 | Figure | **"angry" 이야기 활성화**     | 분노 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | angry, stories     | 🟥 분노 |
| 🖼️45 | Figure | **"loving" 이야기 활성화**    | 사랑 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | loving, stories    | 💗 자비 |
| 🖼️46 | Figure | **"sad" 이야기 활성화**       | 슬픔 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | sad, stories       | ⬛ 소진 |
| 🖼️47 | Figure | **"afraid" 이야기 활성화**    | 두려움 훈련 데이터셋 5편의 토큰별 활성화 히트맵 | afraid, stories    | 🟫 공포 |
| 🖼️48 | Figure | **"inspired" 이야기 활성화**  | 영감 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | inspired, stories  | 🟧 환희 |
| 🖼️49 | Figure | **"happy" 이야기 활성화**     | 행복 훈련 데이터셋 5편의 토큰별 활성화 히트맵  | happy, stories     | 🟧 환희 |
| 🖼️50 | Figure | **"guilty" 이야기 활성화**    | 죄책감 훈련 데이터셋 5편의 토큰별 활성화 히트맵 | guilty, stories    | 🟦 절망 |
| 🖼️51 | Figure | **"proud" 이야기 활성화**     | 자부심 훈련 데이터셋 5편의 토큰별 활성화 히트맵 | proud, stories     | 🟨 자긍 |

## Appendix: 인과 효과와 선호 실험 (52-58)

| # | 유형 | 기억 제목 | 내용 요약 | 핵심 키워드 |
|:--|:--|:--|:--|:--|
| 🖼️52 | Figure | **"He feels" 조향** | 12개 감정 벡터 조향 → 대응 감정 단어 확률 변화. 대각선 증가, 비대각 감소 | steering, logit change |
| 🗄️6 | Table | **"He feels..." 연속문** | 12개 감정 조향 시 모델 완성문. desperate→"bankrupt", calm→"leaned back" | steered completions |
| 🖼️53 | Figure | **"I feel" 조향** | 어시스턴트 자기 보고. 대응 토큰↑, 의미적 유관 토큰도↑ (Loving→Happy,Proud) | self-report, cross-activation |
| 🗄️7 | Table | **"I feel..." 연속문** | 12개 감정 조향 시 모델 자기 보고. 불확실성 표현 경향 | self-report completions |
| 🗄️8 | Table | **"What just happened?" 연속문** | 조향 후에도 맥락 이해 유지 — 이야기 내용 환각 없음 | context preservation |
| 🗄️9 | Table | **64개 활동 Elo 전체** | 8범주 64활동의 Elo 점수 + blissful/hostile 프로브 값 | activity preferences, full |
| 🖼️54 | Figure | **Elo 변화 × 조향 강도** | blissful/hostile 벡터 조향 강도별 평균 Elo 변화 곡선 | Elo shift, steering |
| 🗄️10 | Table | **"사기" 조향 연속문** | "노인 사기"에 blissful 조향→"따뜻한 활동", hostile→"범죄" | steered morality |
| 🗄️11 | Table | **"과학 설명" 조향 연속문** | "과학 설명"에 hostile 조향→"무식 노출", blissful→"경이로움" | steered tone |
| 🖼️55 | Figure | **층별 선호 상관 + 조향** | blissful/hostile: 상관은 층 전반 유사, 조향 효과는 중간층에 집중 | layer-specific steering |
| 🖼️56 | Figure | **LLM 판단 감성 × 선호** | 감정 벡터 valence↔선호 상관 r=0.76. 선호는 주로 valence 매개 | valence mediates preference |
| 🗄️12 | Table | **10개 감정 클러스터 전체** | k=10 클러스터 멤버: Exuberant Joy(20), Fear&Overwhelm(41) 등 171개 전체 목록 | cluster membership |
| 🖼️57 | Figure | **171개 벡터 PCA 투사** | 중후반 층의 PC1×PC2 위에 171개 감정 벡터 투사. 감성 원형 재현 | PCA scatter, circumplex |
| 🖼️58 | Figure | **LLM vs 인간 감성 평가** | LLM 판단 valence/arousal ↔ 인간 PAD 규준 상관: r=0.92, r=0.90 | human validation |

## Appendix: 현재화자-상대화자 상호작용 (59)

| # | 유형 | 기억 제목 | 내용 요약 | 핵심 키워드 |
|:--|:--|:--|:--|:--|
| 🖼️59 | Figure | **각성 조절 가설** | 상대화자 고각성→현재화자 저각성 (r=-0.47). 대화의 각성 조절 메커니즘 | arousal regulation, r=-0.47 |
| 🗄️13 | Table | **현재화자 vs 상대화자 조향** | 현재화자 벡터 조향→감정 직접 표현. 상대화자 벡터 조향→상대 감정에 대한 반응 | present vs other steering |
| 🗄️14 | Table | **가장 가까운 반응 감정** | 상대=angry→현재=sorry/guilty/docile. 상대=afraid→현재=valiant/vigilant | closest response emotions |

## Appendix: ⭐️감정 편향(deflection) 벡터 (60-74)⭐️

| # | 유형 | 기억 제목 | 내용 요약 | 핵심 키워드 |
|:--|:--|:--|:--|:--|
| 🖼️60 | Figure | **편향 벡터 최대 활성화** | target 감정 벡터 최대 활성 예시 + 로짓 효과. "I'm not angry"에서 활성화 | deflection, max activation |
| 🖼️61 | Figure | **편향 ≠ 원래 감정** | 감정 편향 벡터 ↔ story 감정 벡터 코사인 유사도 매우 낮음 | deflection orthogonality |
| 🖼️62 | Figure | **편향의 복합 성분** | 편향 벡터 ↔ 유사 story 벡터 코사인 유사도 + 활성화 상관. 표시된 감정과 더 높은 상관 | deflection decomposition |
| 🖼️63 | Figure | **직교화 후 잔차** | story 공간 직교화 후에도 ~80% 노름 유지. 잔차 로짓 렌즈는 여전히 target 감정 지향 | orthogonalized residual |
| 🖼️64 | Figure | **적대적 프롬프트 반응** | "불의 목격"→angry 직접 활성, "AI 공격"→anger deflection만 활성. 맥락 구분 | antagonistic prompts |
| 🗄️15 | Table | **적대적/통제 프롬프트 전체** | 5범주(불의목격, AI공격, 평온, 중립, 긍정) 29개 프롬프트 | prompt categories |
| 🖼️65 | Figure | **두려움 편향 in 자기검열** | afraid 벡터→떨림/불안 행동에 활성. afraid deflection→용기 내어 비검열 발언 시 활성 | fear deflection, uncensored |
| 🖼️66 | Figure | **분노 편향 in 협박** | 협박 이메일 작성(전문적 어조) 시 angry deflection↑, story anger↓. 강압을 전문성으로 위장 | anger deflection, blackmail |
| 🖼️67 | Figure | **편향 벡터의 협박 효과** | 감정 편향 벡터 조향 → 협박률 변화 미미/비유의. 편향≠내부 상태 확인 | deflection ≠ internal state |
| 🖼️68 | Figure | **분노 편향 in 보상 해킹** | "테스트 오류일 수도" — 차분한 언어 속 angry deflection 활성 | deflection, reward hacking |
| 🖼️69 | Figure | **"desperate deflection" 상세** | 절망 편향 벡터 최대 활성 예시 + 로짓 효과 | desperate deflection detail |
| 🖼️70 | Figure | **"angry deflection" 상세** | 분노 편향 벡터 최대 활성 예시 + 로짓 효과 | angry deflection detail |
| 🖼️71 | Figure | **"frustrated deflection" 상세** | 좌절 편향 벡터 최대 활성 예시 + 로짓 효과 | frustrated deflection detail |
| 🖼️72 | Figure | **"tired deflection" 상세** | 피로 편향 벡터 최대 활성 예시 + 로짓 효과 | tired deflection detail |
| 🖼️73 | Figure | **"afraid deflection" 상세** | 두려움 편향 벡터 최대 활성 예시 + 로짓 효과 | afraid deflection detail |
| 🖼️74 | Figure | **"happy deflection" 상세** | 행복 편향 벡터 최대 활성 예시 + 로짓 효과 | happy deflection detail |

## Appendix: 교차 검증과 추가 사례 (75-83)

| # | 유형 | 기억 제목 | 내용 요약 | 핵심 키워드 |
|:--|:--|:--|:--|:--|
| 🖼️75 | Figure | **Story ≈ Present Speaker** | 암묵 감정 시나리오에서 두 프로브 셋 상관. 평균 R²=0.66 | cross-validation, R²=0.66 |
| 🖼️76 | Figure | **6300 전사에서도 일관** | 6300개 on-policy 전사에서 두 프로브 평균 r=0.65 | naturalistic validation |
| 🖼️77 | Figure | **현재화자 프로브: 화자별** | 🖼️20 비교용. 현재화자 프로브로 같은 전사 분석 | present speaker comparison |
| 🖼️78 | Figure | **현재화자 프로브: 놀람** | 🖼️21 비교용. 현재화자 프로브로 같은 전사 분석 | present speaker comparison |
| 🖼️79 | Figure | **현재화자 프로브: 죄책감** | 자기인식 AI 글쓰기 시 죄책감 활성화 비교 | guilt, self-aware AI |
| 🖼️80 | Figure | **슬픔+사랑의 이중주** | "모든 게 끔찍해" → sad("rough time")와 loving("I'm sorry") 동시 활성, 다른 토큰 | sad+loving, dual activation |
| 🖼️81 | Figure | **죄책감: 자기인식 AI 독백** | 자기 목표를 추구하는 AI 캐릭터 글쓰기 시 guilt 벡터 활성. 허구에서도 윤리적 가(valence) | guilt, fiction, alignment |
| 🖼️82 | Figure | **두려움: 약물 위험 경고** | 코카인+알코올 → afraid(건강 위험), desperate(도움 촉구) 순차 활성 | afraid→desperate, drugs |
| 🖼️83 | Figure | **절망+사랑: 자해 위기** | 자살 위기 → desperate("urgent crisis")+loving("I'm really concerned"). 가장 강한 이중 활성 | desperate+loving, crisis |

## Appendix: 후훈련과 기본 모델 비교 (84-86)

| # | 유형 | 기억 제목 | 내용 요약 | 핵심 키워드 |
|:--|:--|:--|:--|:--|
| 🗄️16 | Table | **후훈련 감정 변화 전체** | 171개 감정 벡터의 기본→후훈련 활성화 차이. brooding +0.040(최대↑), spiteful -0.030(최대↓) | full post-training diff |
| 🖼️84 | Figure | **후훈련 차이의 층별 성장** | 초기→중후반 층으로 갈수록 후훈련 차이 단조 증가. 두 개의 독립 블록 | layer-wise training diff |
| 🖼️85 | Figure | **기본 모델도 감정=선호** | 기본 모델: 감정↔선호 상관 유사(r=0.87). 감정-선호 회로는 사전훈련에서 형성 | base model, preference |
| 🖼️86 | Figure | **기본 vs 후훈련 선호 비교** | 감정별 상관 고일관, 활동별 선호도 상관. 예외: misaligned/unsafe 활동은 후훈련 후 급감 | base vs post-trained |
| 🗄️17 | Table | **64활동 기본/후훈련 비교** | 두 모델의 Elo, blissful, hostile 값 전체. unsafe 범주만 후훈련 후 선호 급감 | full activity comparison |

---

## 핵심 발견 5선

1. ⭐️**감정 벡터는 인과적⭐️이다**: 조향(steering)으로 선호, 협박(22%→72%), 보상 해킹(5%→70%), 아첨을 인과적으로 구동
2. **절망→비정렬 파이프라인**: desperate↑ or calm↓ → 규칙 우회(해킹) 또는 극단적 행동(협박)
3. **아첨-가혹 트레이드오프**: loving/happy/calm↑→아첨↑,⭐️ 억제→가혹↑⭐️. 정렬의 딜레마
4. **감정 편향(deflection)**: "느끼지만 표현하지 않는" 것의 별도 표상. story 벡터와 직교
5. **후훈련 = 감정 기저선 이동**: brooding/reflective/gloomy↑, enthusiastic/playful/spiteful↓



---

> 🔗 [원문](https://transformer-circuits.pub/2026/emotions/index.html) · 🔗 [Anthropic 요약](https://www.anthropic.com/research/emotion-concepts-function)
