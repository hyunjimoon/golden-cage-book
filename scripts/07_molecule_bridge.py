#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""07_molecule_bridge.py — 「대사 밑에 깔린 글」 한 장.

받는 사람이 편집자라 말을 평문으로 둔다. λ·점 반전·분자 같은 안쪽 낱말은 안 쓴다.
기하만 점 반전이다 — 왼쪽이 1→5로 내려가고 오른쪽이 10→6으로 내려가서 선 다섯이
가운데 한 점에서 만난다. 짝은 나란히 놓인 둘이 아니라 중심을 지나 뒤집힌 둘이다.

입체 금지(값은 공통 눈금 위 위치로) · SVG 안에 이모지 금지 · CSS 변수 금지
(rsvg-convert 가 var() 를 못 읽어 색이 검정으로 떨어진다).

    python3 scripts/07_molecule_bridge.py     → img/molecule_bridge.png
"""
import subprocess, os, pathlib

INK="#1a1a1a"; SUB="#555"; CAP="#8a8275"; BG="#fcfbf9"
CAGE="#3b6b73"      # 겪은 것 — 1~4장
NEST="#a67c32"      # 궁리한 것 — 6~9장
MID ="#6a6358"      # 5·10장
EMPTY="#ded9d0"; HOT="#e06a3b"
W,H=1480,860; LX,RX=300,1180; Y0,DY=250,104

L=[("1","거울","빌린 욕망",CAGE),("2","망원경","빌린 한 점",CAGE),("3","스테인굴레스","빌린 확신",CAGE),
   ("4","시계","빌린 질서",CAGE),("5","101호","쓴 빚",MID)]
R=[("10","101호","갚을 빚",MID),("9","까마귀","향할 명명",NEST),("8","안개","향할 협상",NEST),
   ("7","튤립구근","향할 분포",NEST),("6","나비","향할 실험",NEST)]
# 깔린 자리 — 손으로 적지 않는다. 동기화된 chapters/ 에서 직접 읽는다.
#   sync 가 vault 의 <!--글:NN--> 를 docs/essays/NN_*.md 링크로 펴 놓았으므로
#   여기서 그 링크를 세면 그림이 원고를 따라온다. 손으로 적으면 빠뜨린다(실측).
CH={"ch1":("L",0),"ch2":("L",1),"ch3":("L",2),"ch4":("L",3),"ch5":("L",4),
    "ch10":("R",0),"ch9":("R",1),"ch8":("R",2),"ch7":("R",3),"ch6":("R",4)}
TITLE={"31":"옆 물고기","32":"기억나는 변화","33":"편향 0","34":"약속 갱신","35":"감동 옮겨심기",
       "36":"여덟 번","38":"착각 판정","39":"왜 셋인가","40":"슬픔은 본질인가","43":"직렬이냐 병렬이냐",
       "44":"끈끈이 트랩","45":"안 하는 것도 하는 것","48":"양식은 그림자","49":"꿈꾸는 자",
       "50":"리어왕은 별을 모른다","51":"우연은 없다","52":"코비치는 일곱"}
import glob as _g, os as _os, re as _re
LAID=[]
for f in _g.glob(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),"chapters","*.md")):
    key=_os.path.basename(f).split("_")[0]
    if key not in CH: continue
    side,idx=CH[key]
    for no in sorted(set(_re.findall(r"docs/essays/(\d+)_", open(f,encoding="utf-8").read()))):
        LAID.append((side,idx,TITLE.get(no,no)))
LAID=sorted(set(LAID))

def esc(s): return s.replace("&","&amp;").replace("<","&lt;")
def t(x,y,s,sz=13,f=INK,a="start",w="normal",op=1.0):
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-size="{sz}" fill="{f}" text-anchor="{a}" '
            f'font-weight="{w}" opacity="{op}" font-family="Pretendard,AppleSDGothicNeo,sans-serif" '
            f'dominant-baseline="middle">{esc(s)}</text>')

o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>']
o.append(t(60,62,"대사 밑에 깔린 글",30,INK,w="bold"))
o.append(t(60,100,"소설의 한 대사 뒤에는 그 전에 쓴 글이 한 편 있다. 그 글은 겪은 것과 궁리한 것을 함께 담고 있어서, 두 장을 동시에 떠받칠 수 있다.",14.5,SUB))
o.append(t(LX-52,195,"겪은 것 — 빌렸던 때",14,CAGE,a="end",w="bold"))
o.append(t(RX+52,195,"궁리한 것 — 향할 곳",14,NEST,w="bold"))

# 짝 선 다섯 — 1↔6 … 5↔10. 가운데 한 점에서 만난다.
for i in range(5):
    y1=Y0+DY*i; y2=Y0+DY*(4-i)
    o.append(f'<line x1="{LX}" y1="{y1}" x2="{RX}" y2="{y2}" stroke="{EMPTY}" stroke-width="2"/>')
cx,cy=(LX+RX)/2,Y0+DY*2
o.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{HOT}"/>')
o.append(t(cx,cy+26,"다섯 짝이 여기서 만난다",12,HOT,a="middle",w="bold"))
o.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="{HOT}" stroke-width="1" opacity=".4"/>')

# ── 팔이 둘인 글 — 같은 제목이 양쪽에 있으면 그 선을 실선으로 긋는다. 자동이다. ──
BOTH=[nm for nm in {x[2] for x in LAID if x[0]=="L"} & {x[2] for x in LAID if x[0]=="R"}]
li={x[2]:x[1] for x in LAID if x[0]=="L"}; ri={x[2]:x[1] for x in LAID if x[0]=="R"}
ey1=ey2=None
for nm in BOTH:
    ey1,ey2=Y0+DY*li[nm],Y0+DY*ri[nm]
    o.append(f'<line x1="{LX}" y1="{ey1}" x2="{RX}" y2="{ey2}" stroke="{HOT}" stroke-width="2.6"/>')
# 상자는 선 위 왼쪽 1/4 지점에 둔다 — 가운데 교차점을 가리면 이 그림의 요점이 가려진다.


def col(items,x,side):
    for i,(no,nm,ph,c) in enumerate(items):
        y=Y0+DY*i
        o.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{c}"/>')
        o.append(t(x,y+1,no,13,"#fff",a="middle",w="bold"))
        dx = -26 if side=="L" else 26
        a  = "end" if side=="L" else "start"
        o.append(t(x+dx,y-8,nm,14,INK,a=a,w="bold"))
        o.append(t(x+dx,y+10,ph,12.5,CAP,a=a))

col(L,LX,"L"); col(R,RX,"R")

# 깔린 자리 — 기둥 바깥으로 뻗은 짧은 팔. 팔이 하나뿐인 것이 그대로 보인다.
# 한 장에 여럿이 깔렸으면 위아래로 쌓는다 — 겹쳐 찍으면 둘 다 못 읽는다.
from collections import Counter as _C
_seen=_C()
for side,i,name in LAID:
    k=(side,i); _n=sum(1 for x in LAID if (x[0],x[1])==k)
    y=Y0+DY*i+(_seen[k]-(_n-1)/2)*17; _seen[k]+=1
    if side=="L": x0,x1,c,a=LX-96,LX-122,CAGE,"end"
    else:         x0,x1,c,a=RX+96,RX+122,NEST,"start"
    o.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c}" stroke-width="1.6"/>')
    o.append(f'<circle cx="{x1}" cy="{y}" r="4" fill="{c}"/>')
    o.append(t(x1+(-12 if side=="L" else 12),y,name,12.5,c,a=a))

BY=Y0+DY*4+120
o.append(f'<line x1="60" y1="{BY-34}" x2="{W-60}" y2="{BY-34}" stroke="{EMPTY}" stroke-width="1.5"/>')
NL=len(LAID); NB=len(BOTH)
for j,(n,lab) in enumerate([("14","이렇게 쓴 글"),(str(NL),"대사 밑에 깔린 자리"),(str(NB),"두 장을 다 떠받친 글")]):
    x=120+j*300
    o.append(t(x,BY+4,n,34,HOT if n=="0" else INK,w="bold"))
    o.append(t(x+(62 if len(n)>1 else 34),BY+6,lab,13.5,SUB))
o.append(t(1020,BY-4,"짝 다섯이 전부 꿰매졌다 — 같은 글이 양쪽을 떠받친다.",13.5,SUB))
o.append(t(1020,BY+18,"한 편이 빌렸던 때와 향할 곳을 함께 담고 있어서 가능한 일이다.",13.5,CAP))
o.append(t(60,H-34,"2026-11-20 실측 · scripts/07_molecule_bridge.py",11.5,CAP,op=.8))
o.append("</svg>")

root=pathlib.Path(__file__).resolve().parent.parent
svg=root/"img/molecule_bridge.svg"; png=root/"img/molecule_bridge.png"
svg.write_text("\n".join(o),encoding="utf-8")
subprocess.run(["rsvg-convert","-w","1480",str(svg),"-o",str(png)],check=True)
print(f"✅ {png.relative_to(root)}  ({png.stat().st_size:,} bytes)")
