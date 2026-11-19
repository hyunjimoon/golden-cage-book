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
# 깔린 자리 — (쪽, 줄index, 글 제목). 2026-11-20 실측 5자리.
LAID=[("L",1,"안 하는 것도 하는 것"),("L",2,"편향 0"),("L",3,"기억나는 변화"),
      ("R",1,"코비치는 일곱"),("R",0,"왜 셋인가")]

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

# ── 될 모습 하나 — 2↔7 선 위에 점선으로. 아직 아니라는 것이 점선으로 보인다. ──
ey1,ey2=Y0+DY*1,Y0+DY*3
o.append(f'<line x1="{LX}" y1="{ey1}" x2="{RX}" y2="{ey2}" stroke="{HOT}" '
         f'stroke-width="2.2" stroke-dasharray="7 6" opacity=".85"/>')
# 상자는 선 위 왼쪽 1/4 지점에 둔다 — 가운데 교차점을 가리면 이 그림의 요점이 가려진다.
mx,my=LX+(RX-LX)*0.27,ey1+(ey2-ey1)*0.27
o.append(f'<rect x="{mx-152}" y="{my-64}" width="304" height="50" rx="6" fill="{BG}" '
         f'stroke="{HOT}" stroke-width="1.2" stroke-dasharray="4 4"/>')
o.append(f'<line x1="{mx}" y1="{my-14}" x2="{mx}" y2="{my-2}" stroke="{HOT}" stroke-width="1.2"/>')
o.append(t(mx,my-48,"이렇게 되면 — 글 한 편이 팔 둘",12.5,HOT,a="middle",w="bold"))
o.append(t(mx,my-28,"「안 하는 것도 하는 것」 겪은 쪽 2장 · 궁리한 쪽 7장",12.5,SUB,a="middle"))

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
for side,i,name in LAID:
    y=Y0+DY*i
    if side=="L": x0,x1,c,a=LX-96,LX-122,CAGE,"end"
    else:         x0,x1,c,a=RX+96,RX+122,NEST,"start"
    o.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c}" stroke-width="1.6"/>')
    o.append(f'<circle cx="{x1}" cy="{y}" r="4" fill="{c}"/>')
    o.append(t(x1+(-12 if side=="L" else 12),y,name,12.5,c,a=a))

BY=Y0+DY*4+120
o.append(f'<line x1="60" y1="{BY-34}" x2="{W-60}" y2="{BY-34}" stroke="{EMPTY}" stroke-width="1.5"/>')
for j,(n,lab) in enumerate([("14","이렇게 쓴 글"),("5","대사 밑에 깔린 자리"),("0","두 장을 다 떠받친 글")]):
    x=120+j*300
    o.append(t(x,BY+4,n,34,HOT if n=="0" else INK,w="bold"))
    o.append(t(x+(62 if len(n)>1 else 34),BY+6,lab,13.5,SUB))
o.append(t(1020,BY-4,"팔이 둘인 글이 하나라도 생기면 짝이 글로 꿰매진다.",13.5,SUB))
o.append(t(1020,BY+18,"지금은 다섯 자리 모두 팔이 하나뿐이라, 선 다섯이 비어 있다.",13.5,CAP))
o.append(t(60,H-34,"2026-11-20 실측 · scripts/07_molecule_bridge.py",11.5,CAP,op=.8))
o.append("</svg>")

root=pathlib.Path(__file__).resolve().parent.parent
svg=root/"img/molecule_bridge.svg"; png=root/"img/molecule_bridge.png"
svg.write_text("\n".join(o),encoding="utf-8")
subprocess.run(["rsvg-convert","-w","1480",str(svg),"-o",str(png)],check=True)
print(f"✅ {png.relative_to(root)}  ({png.stat().st_size:,} bytes)")
