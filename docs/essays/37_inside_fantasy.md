# 환상 속에서 만든 것이 살아난다

> 처음 쓴 자리 — [#146](https://github.com/hyunjimoon/golden-cage-book/issues/146#issuecomment-6182256266) · 본문에서 만나는 자리 — **1 거울 · 6 나비**

---

🚨tbe🚨

[“‘AI가 쓴 소설’도 문학상 받을 수 있나?”···프랑스 4대 문학상 발칵](https://n.news.naver.com/article/032/0003476384?lfrom=kakao)

> AI를 활용한 출판물이 늘면서, 논란의 초점은 AI 사용 여부를 넘어 AI 사용이 의심되는 작품을 어떻게 평가할 것인가로 옮겨가고 있다

요약: ai모델을 내포하지 않은 의심의 품질은, 의심해봐야

---
https://github.com/hyunjimoon/golden-cage-book/issues/105#issuecomment-5659471480 의 

1. 👁️🧠관찰/궁리: 행위자 모델을 내포할 수록 평가자 품질이 높아짐 "good regulator of a system must be a model of that system"

2. 🫀🤚실천: 느리게 변하는 📍맥락고정. 그 장 위에서 여러 쌍의 {행위자, 평가자} 모델 움직임 관찰. 현실성있는 움직임의 상상일수록 효율적. 문턱 넘어 양질전환되면 효과적. 해당 장의 수렴을 상호작용시켜 안정적일 결합분포를 관찰. 즉, 시간 벌고, 또 전파되는 동안 번 시간으로 앞선 빚 (📍맥락 고정) 상환
e.g. 길이 1000인 4개 탐색체인 돌려서, 각 체인마다 앞 500개는 지형탐색 warmup단계에 쓴 후 버리고 (오염됨), 그 후 500 * 4= 2000개 
각 체인마다 1000개씩 뽑으면 수렴할 확률이 높은데, 이 비교적 안정적일 미래 수렴점 제안으로 번 시간에 다음 수렴점 찾는 행위 반복 🧬


관찰과 실천이 융합된 계산방법 발전 역사 a.k.a. 샘플링 방법 or 통계 계산

(tbe) **관찰과 실천 융합** (융합: 녹아 합해짐)이라 표현한 이유를 따져보자. 통계는 세금 잘 걷고자 만들어진 학문이다. 전체 인구를 모델로 구현한 후, 현상파악하는 눈의 기능이 다 일거 같지만, 우리는 매년 세금 내고 제도도 매년 변한다. 즉 피드백이 있다. 이 순환 구조 안에서 끊임없이 최적화할 목적함수 (예: 전체 국민 복지의 표현 i.e. total welfare)와 해당 목적함수 증가시키려는 제도적 방안이 개발된다. 

(🌉다리 문장1)

그렇게 환상, 즉 모델 상, 속에서 개발된 방법론들은 그 자체로 생명력을 가진다는 folk theorem 이름은 피노키오 원리. 자매품: 마음과 손 #127 , 하향과 상향 함께 https://github.com/hyunjimoon/golden-cage-book/issues/143#issuecomment-5569986812

> [The Pinocchio Principle](https://www.stat.columbia.edu/~gelman/research/published/parameterization.pdf): A model that is created solely for computational reasons can take on a life of its own.

--- 
통계 계산 역사 중 특기할만한 세 알고리즘:

a. accept-reject (tbc)

b. hamiltonian monte carlo (hmc): 베이즈 계산의 혁명적 알고리즘. ergodic 이론 연구했던 stanis ulam이🎟️ ~~개발~~ (edit 26.10.28. 이 알고리즘을 구현해 오픈소스로 만든 단체가 stan의 이름을 딴것) 기존 알고리즘들은 N차원 위치만 추적. 각 입자의 운동N차원 운동량의 차원확장을 통해 (#155 의 symplectic에 실수 -> (실수, 허수) 원리와 유사하다 봄) (위치, 운동량)의 차원확장을 통해 안 보이던 흐름을 탐지해 고차원 공간에서 효율적인 공간탐색 가능케함. 

c. particle filtering: 한 샘플은 한 샘플뿐일뿐, 입자가 합쳐져 중요도에 비례하는 질량을 가진 새 입자로 새롭게 태어나는 **종분화 형식** 이런 문법 없는 hmc 단점 보안. 새 입자생성 문법과 종분화 내용 표현의 관계 🎟️🎟️🎟️

---
🎟️위키 중 ulam이 1) ergodic theory연구했고, 2)핵연료 추진체 지지했고, 3) 메두사 프로젝트 참여했음이 눈에 들어온다. 시선의 빼앗김은 1)은 관심사 (ergodic)와 공간 겹침 인력 (뉴욕, 보스턴), 2)는 과정의 필요 (핵연료의 과정), 3)은 상징의 필요 (뱀)로 추정됨.

1. ergodic: 자연현상이라 믿는 비가역성에 도전해볼, 그나마 성공확률 높은 접근은 시간평균이 공간평균으로 수렴하게 설계하자는 내 ergodic life철학 
"해당 시스템의 위상 공간에서 시스템 상태들의 공간에 대해 평균하면 시간에 따라 평균적으로 동일한 행동" 에르고딕 정리

2. 링크 https://en.wikipedia.org/wiki/Nuclear_pulse_propulsion 가 내포하는 링크

3. https://en.wikipedia.org/wiki/Nuclear_pulse_propulsion#Medusa

중 눈길 간 문장

> Medusa spacecraft works by throwing bombs into a sail that's ahead of it

보며 생각난 #108 역인과와 #155 의 처형당한 후 죄 짓기 🎟️🎟️

<img width="400" height="300" alt="Image" src="https://github.com/user-attachments/assets/ea3b15b6-b8a9-407f-bfbd-9a49134641cf" />

---

🎟️🎟️"throwing bombs into a sail that's ahead of it": 자장 혼동을 핵분열로 주는 원리 궁리. 아래 사진에서 자기장 균형을 이뤄 정지해있는 차와 달리 인류역사는 계속 앞으로 움직인다. 물리 시스템과 물리+화학/생물이 추가된 시스템에서 동력의 유한 vs 무한성의 차이를 보이는 이유는 후자가 계속해서 쓸만한 환상을 만들기 때문. 감각기억->단기기억->장기기억 과정의 비틂이 그 동력이라는 가설. 

<img width="300" height="300" alt="Image" src="https://github.com/user-attachments/assets/72861044-b554-4c02-aa51-13ad4dddad41" />

---
🎟️🎟️🎟️
새 입자생성 문법과 종분화 내용 표현의 관계 

- #106 "틈새시장을 희미하게 인식하고, 기존 기술을 땜질식으로 가져다 임시변통으로 수요를 충족시키려는 선적응 노력 많이 할수록 기술분화 가능성 커짐" 즉, 기존 기술로 새 필요 덮으려는 노력에 덮개 찢기며 기술 종 분화
- #107 선넘기와 개미반례 + 선적응 잘 할 수록 종분화 잘 할 것 
- #143 스타인벡의 팔랑크스는 낱개의 사람이 가질 수 없는 감정 가짐)

<img width="300" height="300" alt="Image" src="https://github.com/user-attachments/assets/24a24d65-d4e7-414b-9ffc-16902c821da9" />
