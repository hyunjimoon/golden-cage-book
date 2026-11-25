#!/usr/bin/env python3
"""투향 최소충분통계 — 지면이 무엇을 비워 뒀나. 이슈가 아니라 원고를 센다.

자를 고칠 때 — 센 값이 이미 공용 지도에 적혀 있는지 먼저 본다
(순환지도_10장10공간.md). 적혀 있으면 새 자를 만들지 않는다.
"""
import re, sys, os, datetime

# 꼴: nest = 맺음 네 자리 · cage = 번호 셋 · both = 둘 다 · hinge = 어느 꼴도 안 정해졌다
CH = [("1","🪞 거울","ch1_mirror_cage","both"),   ("2","🔭 망원경","ch2_telescope_cage","cage"),
      ("3","💒 스테인굴레스","ch3_glass_cage","cage"), ("4","⏱️ 시계","ch4_clock_cage","cage"),
      ("5","🐀 101호","ch5_mirror_nest","hinge"),  ("6","🦋 나비","ch6_butterfly_nest","nest"),
      ("7","🧅 튤립구근","ch7_tulip_nest","nest"),  ("8","🌫️ 안개","ch8_mist_nest","nest"),
      ("9","🐦‍⬛ 까마귀","ch9_raven_nest","nest"),  ("10","🧫 투향","ch10_mirror_close","nest")]
ORGANS=[("§1","👁️","감각"),("§2","🧠","생각"),("§3","🫀","현실"),("§結","🤚","실천")]
P_SEC=r"^## §(1|2|3|結)"; P_SEAT=r"^\*\*(🦋|🧅|🌫️|🐦‍⬛)"; P_NUM=r"^> \*\*[①②③]\*\*"
WANT={"nest":(4,0),"cage":(0,3),"both":(4,3),"hinge":(None,None)}

root=sys.argv[1] if len(sys.argv)>1 else "chapters"
rows=[]
for num,name,slug,kind in CH:
    p=os.path.join(root,slug+".md")
    if not os.path.exists(p): rows.append((num,name,kind,None)); continue
    t=open(p,encoding="utf-8").read()
    secs={m.group(1) for m in re.finditer(P_SEC,t,re.M)}
    rows.append((num,name,kind,{
        "절":{"§1":"1" in secs,"§2":"2" in secs,"§3":"3" in secs,"§結":"結" in secs},
        "맺음":len(re.findall(P_SEAT,t,re.M)),"번호":len(re.findall(P_NUM,t,re.M)),"자":len(t)}))

if "--selftest" in sys.argv:
    # 관문은 「원고가 나아졌나」가 아니라 「자가 아직 보나」를 묻는다.
    # 아는 값에 댄다 — 2026-11-25 에 네 절을 다 가진 장이 여덟이었다.
    # 원고가 채워지면 이 수는 올라가고 관문은 통과한다. 내려가면 자가 깨진 것이다.
    full=[n for n,_,_,d in rows if d and all(d["절"].values())]
    print("FULL=%d" % len(full), full)
    print("안 가진 장:",[(n,[k for k,v in d["절"].items() if not v]) for n,_,_,d in rows if d and not all(d["절"].values())])
    print("파일 없는 장:",[n for n,_,_,d in rows if d is None])
    sys.exit(0)

blank=sum(1 for _,_,_,d in rows if d for v in d["절"].values() if not v)
off=[]
for num,name,kind,d in rows:
    if not d or kind=="hinge": continue
    ws,wn=WANT[kind]
    if d["맺음"]!=ws: off.append(f"{num}장 맺음 {d['맺음']}≠{ws}")
    if d["번호"]!=wn: off.append(f"{num}장 번호 {d['번호']}≠{wn}")
o=[]
A=o.append
A("# 투향 — 무엇이 비었나")
A("")
A(f"> **지면 격자 빈칸 {blank}/40 · 맺음 꼴 어긋남 {len(off)}.** 실측 {datetime.date.today()}.")
A("> 센 것은 **이슈가 아니라 지면**(`chapters/*.md`)이다. 자동 생성 — 직접 편집하지 않는다.")
A("")
A("## 1. 격자 — 장 열 × 기관 넷")
A("")
A("| 장 | "+" | ".join(f"{s} {g} {k}" for s,g,k in ORGANS)+" | 빈칸 |")
A("|:--|"+":--:|"*5)
cb=[0]*4
for num,name,kind,d in rows:
    if d is None: A(f"| {num} {name} | "+" | ".join(["—"]*4)+" | 파일 없음 |"); continue
    cs=[];rb=0
    for i,(s,_,_) in enumerate(ORGANS):
        ok=d["절"][s]; cs.append("✓" if ok else "🈳")
        if not ok: rb+=1; cb[i]+=1
    A(f"| {num} {name} | "+" | ".join(cs)+f" | {rb if rb else '·'} |")
A("| **빈칸** | "+" | ".join(f"**{c}**" if c else "·" for c in cb)+f" | **{blank}** |")
A("")
A("🈳 = 그 절이 지면에 없다. 패턴 `^## §(1|2|3|結)` · 코퍼스 `chapters/ch*.md` 열 파일.")
A("")
A("⚠️ **5장과 10장의 🈳는 아직 「빈칸인지 꼴이 다른지」가 안 갈렸다.** 5장은 마디면이고 10장은 끝 방이라")
A("네 절 꼴을 안 따를 수 있다. 빈칸으로 두고, 가르는 것은 사람 몫이다 — 0으로 메우지 않는다.")
A("")
A("## 2. 맺음 꼴 — 제 꼴과 어긋난 칸만")
A("")
A("| 장 | 꼴 | 글자 | 맺음 네 자리 | 번호 셋 |")
A("|:--|:--|--:|:--:|:--:|")
for num,name,kind,d in rows:
    if d is None: A(f"| {num} {name} | {kind} | — | — | — |"); continue
    ws,wn=WANT[kind]
    f=lambda v,w:("—" if w is None else (str(v) if v==w else f"**{v}** (기대 {w})"))
    A(f"| {num} {name} | {kind} | {d['자']:,} | {f(d['맺음'],ws)} | {f(d['번호'],wn)} |")
A("")
A("꼴 — **nest** 둥지·끝 방은 맺음 네 자리(🦋🧅🌫️🐦‍⬛) · **cage** 새장은 번호 셋(①②③) ·")
A("**both** 1장은 둘 다 쥔다 · **hinge** 5장은 어느 꼴도 안 정해졌으므로 기대를 안 건다.")
A("굵은 수만 손이 갈 자리다. 기대와 같은 수는 설계대로 선 것이다.")
A("")
A("## 3. 뺀 것 — 닿지 않거나, 거짓 0을 주어서")
A("")
A("- **이슈 라벨 세기** — 장×렌즈 이슈 수는 *말이 있나*를 재고 *지면이 비었나*를 못 잰다.")
A("  이슈 0건은 빈칸이 아니라 아무도 그 칸을 말하지 않은 것이고, 열 건이어도 지면은 안 움직인다.")
A("- **이월 비트** — 꼴이 셋(이탤릭 카메라 · 블록 · 둘 다)이라 한 패턴으로 세면 거짓 0이 난다.")
A("  맞는 값은 이미 적혀 있다 — `순환지도_10장10공간.md` 「이월 비트는 10/10 섰다」.")
A("- **앞 장 받음** — 꼴이 셋 이상(세다 입 · 인용 · 저자 서술)이라 같은 병이 난다. 짝 축은 5/5 선다(2026-11-25 실측).")
A("- **원고 안의 🙋‍♀️ 잔차** — 지면에서 걷히므로(`strip_scaffolding.awk`) 이 표는 못 본다. vault 쪽 자다.")
if off:
    A(""); A("### 어긋난 칸"); [A(f"- {x}") for x in off]
print("\n".join(o))
