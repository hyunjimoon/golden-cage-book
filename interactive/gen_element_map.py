#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_element_map.py — 생각 지도(element_map.html) SSOT 생성기

chapters/elements/*.md 의 frontmatter(족·족번호·chapter·star·정의)를 파싱해
"이 생각(원소)이 어느 장에 사는가"를 보여주는 자기완결 HTML을 만든다.

- 진입 = 지도(graph, bipartite: 장 허브 ↔ 원소)
- 밑 = 표(matrix, 원소×장 소속)
- 진입 UI에 수학 용어(행렬·다면체·isomorphic) 노출 금지 (독자 debate 7:1, 박순영 반대 반영)

사용: python3 interactive/gen_element_map.py   (repo 루트 또는 interactive/ 어디서든)
"""
import os, re, json, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ELEM_DIR = os.path.join(ROOT, "chapters", "elements")
OUT = os.path.join(HERE, "element_map.html")

FAMILIES = {
    1: ("1. 방정식·부등식", "#5A8A9A"),
    2: ("2. 프레임워크·구조", "#6B8E4B"),
    3: ("3. 이론·학자 anchor", "#C97B3C"),
    4: ("4. 메타포·상징", "#8B6BAA"),
    5: ("5. 연산·동작", "#4A7A6B"),
    6: ("6. 자장 고유 어휘", "#9B7A8B"),
}

# 장 번호 → 사람 이름(허브 라벨). 5·10은 회전축 거울쌍.
CHAP_NAME = {
    "1": "1 거울", "2": "2 망원경", "3": "3 스테인굴레스", "4": "4 시계",
    "5": "5 빅시스터", "6": "6 나비", "7": "7 튤립", "8": "8 안개",
    "9": "9 까마귀", "10": "10 에필로그",
}
AUX_HUB = "전반·부록·도식"  # 전/부N/dgm/session/Lex/감정/표지/feedback/전략 등


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None, ""
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([가-힣A-Za-z_]+):\s*(.*)$", line)
        if mm:
            k, v = mm.group(1), mm.group(2).strip()
            v = v.strip('"').strip("'")
            fm[k] = v
    body = text[m.end():]
    return fm, body


def title_of(body, fallback):
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def chapters_of(raw):
    """chapter frontmatter 값 → 장 허브 토큰 리스트(정규화)."""
    toks = []
    for part in str(raw).split("·"):
        p = part.strip()
        if not p:
            continue
        if re.fullmatch(r"\d+", p):
            toks.append(p)
        elif re.fullmatch(r"\d+-\d+", p):  # 범위 1-4, 6-9
            a, b = p.split("-")
            toks += [str(i) for i in range(int(a), int(b) + 1)]
        else:
            toks.append("__aux__")
    # dedup 유지순서
    seen, out = set(), []
    for t in toks:
        if t not in seen:
            seen.add(t); out.append(t)
    return out


def main():
    files = sorted(glob.glob(os.path.join(ELEM_DIR, "*.md")))
    elements = []
    for f in files:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        fm, body = parse_frontmatter(text)
        if not fm or "족번호" not in fm or "chapter" not in fm:
            continue
        try:
            fam = int(fm["족번호"])
        except ValueError:
            continue
        if fam not in FAMILIES:
            continue
        base = os.path.splitext(os.path.basename(f))[0]
        elements.append({
            "id": base,
            "title": title_of(body, base),
            "fam": fam,
            "star": str(fm.get("star", "false")).lower() == "true",
            "def": fm.get("정의", ""),
            "chaps": chapters_of(fm["chapter"]),
        })

    # 실제 등장하는 장 허브만(순서: 1..10, 그다음 aux)
    used = set()
    for e in elements:
        used.update(e["chaps"])
    chap_order = [c for c in map(str, range(1, 11)) if c in used]
    hubs = []
    for c in chap_order:
        hubs.append({"id": c, "name": CHAP_NAME.get(c, c), "aux": False})
    if "__aux__" in used:
        hubs.append({"id": "__aux__", "name": AUX_HUB, "aux": True})

    data = {
        "families": {str(k): {"name": v[0], "color": v[1]} for k, v in FAMILIES.items()},
        "hubs": hubs,
        "elements": elements,
    }
    payload = json.dumps(data, ensure_ascii=False)

    html = TEMPLATE.replace("/*__DATA__*/", payload)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    # 요약
    fam_ct = {}
    for e in elements:
        fam_ct[e["fam"]] = fam_ct.get(e["fam"], 0) + 1
    print(f"✅ {OUT}")
    print(f"   원소 {len(elements)}개 · 장 허브 {len(hubs)}개")
    for k in sorted(fam_ct):
        print(f"   족{k} {FAMILIES[k][0]:22} {fam_ct[k]:3}")
    print(f"   장 토큰: {[h['name'] for h in hubs]}")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>생각 지도 — 황금새장을열다</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700&family=Noto+Sans+KR:wght@300;400;500&display=swap');
  :root{
    --bg:#14110f; --panel:#1c1815; --line:#3a332c; --dim:#8a7f72;
    --ink:#e8e0d4; --gold:#c5a55a;
  }
  *{box-sizing:border-box;margin:0;padding:0;}
  html,body{height:100%;background:var(--bg);color:var(--ink);
    font-family:'Noto Sans KR',sans-serif;overflow:hidden;}
  #wrap{position:relative;width:100vw;height:100vh;}
  canvas{display:block;position:absolute;inset:0;cursor:grab;}
  canvas.drag{cursor:grabbing;}

  header{position:absolute;top:0;left:0;right:0;z-index:5;
    padding:18px 22px 14px;pointer-events:none;
    background:linear-gradient(180deg,rgba(20,17,15,.92),rgba(20,17,15,0));}
  h1{font-family:'Noto Serif KR',serif;font-size:22px;font-weight:700;
    color:var(--gold);letter-spacing:.5px;}
  .sub{font-size:13px;color:var(--dim);margin-top:3px;font-weight:300;}

  .toggle{position:absolute;top:18px;right:22px;z-index:6;display:flex;
    border:1px solid var(--line);border-radius:20px;overflow:hidden;
    pointer-events:auto;background:var(--panel);}
  .toggle button{background:transparent;border:none;color:var(--dim);
    font-family:'Noto Sans KR';font-size:13px;padding:7px 18px;cursor:pointer;}
  .toggle button.on{background:var(--gold);color:#14110f;font-weight:500;}

  .legend{position:absolute;left:22px;bottom:18px;z-index:6;
    display:flex;flex-wrap:wrap;gap:10px 16px;max-width:62vw;
    font-size:12px;color:var(--dim);pointer-events:auto;}
  .legend .item{display:flex;align-items:center;gap:6px;cursor:pointer;
    opacity:.95;transition:opacity .15s;user-select:none;}
  .legend .item.off{opacity:.32;}
  .legend .dot{width:11px;height:11px;border-radius:50%;flex:none;}
  .legend .star{color:var(--gold);}

  #tip{position:absolute;z-index:8;pointer-events:none;max-width:280px;
    background:#0f0d0b;border:1px solid var(--line);border-radius:8px;
    padding:9px 11px;font-size:12.5px;line-height:1.5;color:var(--ink);
    box-shadow:0 6px 24px rgba(0,0,0,.5);opacity:0;transition:opacity .1s;}
  #tip .t-title{font-weight:500;color:var(--gold);margin-bottom:3px;}
  #tip .t-meta{color:var(--dim);font-size:11px;margin-top:4px;}

  /* 표 뷰 */
  #tableView{position:absolute;inset:0;z-index:4;display:none;
    overflow:auto;padding:78px 22px 70px;background:var(--bg);}
  #tableView.show{display:block;}
  table{border-collapse:collapse;font-size:12px;width:max-content;min-width:100%;}
  th,td{border:1px solid var(--line);padding:5px 8px;white-space:nowrap;}
  th{position:sticky;top:0;background:var(--panel);color:var(--dim);
    font-weight:500;z-index:2;}
  td.name{text-align:left;max-width:340px;white-space:normal;}
  td.cell{text-align:center;color:var(--gold);font-size:14px;}
  tr.fam-head td{background:#221d18;color:var(--ink);font-weight:500;
    font-family:'Noto Serif KR';letter-spacing:.3px;}
  .star-mark{color:var(--gold);}
  td.name .df{color:var(--dim);font-size:11px;display:block;margin-top:1px;}

  a.back{position:absolute;left:22px;top:64px;z-index:6;font-size:12px;
    color:var(--dim);text-decoration:none;border-bottom:1px dotted var(--line);
    pointer-events:auto;}
  a.back:hover{color:var(--gold);}
</style>
</head>
<body>
<div id="wrap">
  <canvas id="c"></canvas>
  <div id="tableView"></div>

  <header>
    <h1>생각 지도</h1>
    <div class="sub">이 책의 생각 <b id="nCount">0</b>개가 어느 장에 사는가 — 점을 끌어 보고, 장을 눌러 그 장의 생각을 밝혀보세요</div>
  </header>
  <a class="back" href="../index.html">← 메인으로</a>

  <div class="toggle">
    <button id="btnMap" class="on">지도</button>
    <button id="btnTable">표</button>
  </div>

  <div class="legend" id="legend"></div>
  <div id="tip"></div>
</div>

<script>
const DATA = /*__DATA__*/;

/* ---------- 공통 ---------- */
const fams = DATA.families;               // {"1":{name,color},...}
const hubs = DATA.hubs;                   // [{id,name,aux}]
const elems = DATA.elements;              // [{id,title,fam,star,def,chaps}]
document.getElementById('nCount').textContent = elems.length;
const famOff = new Set();                  // 숨긴 족

/* ---------- 범례 ---------- */
const legend = document.getElementById('legend');
Object.entries(fams).forEach(([k,v])=>{
  const el=document.createElement('div');
  el.className='item';el.dataset.fam=k;
  el.innerHTML=`<span class="dot" style="background:${v.color}"></span>${v.name.replace(/^\d+\.\s*/,'')}`;
  el.onclick=()=>{el.classList.toggle('off');
    if(famOff.has(k))famOff.delete(k);else famOff.add(k);
    rebuild();if(tableOn)renderTable();};
  legend.appendChild(el);
});
const starItem=document.createElement('div');
starItem.className='item';starItem.innerHTML=`<span class="star">★</span> 핵심 생각`;
legend.appendChild(starItem);

/* ---------- 그래프 물리 ---------- */
const canvas=document.getElementById('c');
const ctx=canvas.getContext('2d');
let W,H,DPR;
function resize(){DPR=window.devicePixelRatio||1;W=innerWidth;H=innerHeight;
  canvas.width=W*DPR;canvas.height=H*DPR;canvas.style.width=W+'px';
  canvas.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
addEventListener('resize',()=>{resize();});
resize();

let nodes=[], links=[], byId={};
function buildGraph(){
  nodes=[];links=[];byId={};
  // 장 허브
  hubs.forEach((h,i)=>{
    const ang=(i/hubs.length)*Math.PI*2;
    const n={id:'hub:'+h.id,kind:'hub',label:h.name,aux:h.aux,
      x:W/2+Math.cos(ang)*Math.min(W,H)*0.30,
      y:H/2+Math.sin(ang)*Math.min(W,H)*0.30,
      vx:0,vy:0,r:h.aux?9:13,deg:0};
    nodes.push(n);byId[n.id]=n;
  });
  // 원소
  elems.forEach(e=>{
    if(famOff.has(String(e.fam)))return;
    const n={id:'el:'+e.id,kind:'el',fam:e.fam,star:e.star,label:e.title,
      def:e.def,chaps:e.chaps,color:fams[e.fam].color,
      x:W/2+(Math.random()-.5)*W*0.5,y:H/2+(Math.random()-.5)*H*0.5,
      vx:0,vy:0,r:e.star?6.5:4};
    nodes.push(n);byId[n.id]=n;
    e.chaps.forEach(c=>{
      const hid='hub:'+(c==='__aux__'?'__aux__':c);
      if(byId[hid]){links.push({s:n.id,t:hid});byId[hid].deg++;}
    });
  });
}
function rebuild(){const keep={};nodes.forEach(n=>keep[n.id]=n);buildGraph();
  // 위치 승계(깜빡임 방지)
  nodes.forEach(n=>{if(keep[n.id]){n.x=keep[n.id].x;n.y=keep[n.id].y;}});}

let hoverId=null, dragId=null, highlightHub=null;
function sim(){
  const K=0.012, REP=1400, LEN_H=150;
  for(let i=0;i<nodes.length;i++){
    const a=nodes[i];
    for(let j=i+1;j<nodes.length;j++){
      const b=nodes[j];let dx=a.x-b.x,dy=a.y-b.y;
      let d2=dx*dx+dy*dy||0.01;let d=Math.sqrt(d2);
      let f=REP/d2;if(d<1){d=1;}
      const fx=dx/d*f,fy=dy/d*f;
      if(a!==dragNode){a.vx+=fx;a.vy+=fy;}
      if(b!==dragNode){b.vx-=fx;b.vy-=fy;}
    }
  }
  links.forEach(l=>{
    const a=byId[l.s],b=byId[l.t];if(!a||!b)return;
    let dx=b.x-a.x,dy=b.y-a.y;let d=Math.sqrt(dx*dx+dy*dy)||0.01;
    const target=b.kind==='hub'?LEN_H:60;
    const f=(d-target)*0.02;const fx=dx/d*f,fy=dy/d*f;
    if(a!==dragNode){a.vx+=fx;a.vy+=fy;}
    if(b!==dragNode){b.vx-=fx;b.vy-=fy;}
  });
  nodes.forEach(n=>{
    if(n===dragNode)return;
    // 허브는 중앙 쪽으로 약하게 고정
    n.vx+=(W/2-n.x)*(n.kind==='hub'?0.004:0.0016);
    n.vy+=(H/2-n.y)*(n.kind==='hub'?0.004:0.0016);
    n.vx*=0.86;n.vy*=0.86;n.x+=n.vx;n.y+=n.vy;
    n.x=Math.max(n.r+8,Math.min(W-n.r-8,n.x));
    n.y=Math.max(n.r+70,Math.min(H-n.r-60,n.y));
  });
}
let dragNode=null;

function draw(){
  ctx.clearRect(0,0,W,H);
  // 링크
  links.forEach(l=>{
    const a=byId[l.s],b=byId[l.t];if(!a||!b)return;
    let hot=false;
    if(highlightHub){hot=(l.t==='hub:'+highlightHub);}
    else if(hoverId){hot=(l.s===hoverId||l.t===hoverId);}
    ctx.strokeStyle=hot?'rgba(197,165,90,.55)':'rgba(120,110,96,.10)';
    ctx.lineWidth=hot?1.4:0.7;
    ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
  });
  // 노드
  nodes.forEach(n=>{
    if(n.kind==='hub'){
      ctx.fillStyle=n.aux?'#2a241d':'#241f19';
      ctx.strokeStyle=(highlightHub===n.id.slice(4))?'var(--gold)':'#5a4f3f';
      ctx.strokeStyle=(highlightHub===n.id.slice(4))?'#c5a55a':'#6a5f4c';
      ctx.lineWidth=(highlightHub===n.id.slice(4))?2.2:1.2;
      ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,7);ctx.fill();ctx.stroke();
      ctx.fillStyle='#e8e0d4';ctx.font="600 13px 'Noto Serif KR',serif";
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(n.label,n.x,n.y-n.r-9);
    }else{
      let dim=false;
      if(highlightHub){dim=!n.chaps.some(c=>('__aux__'===c?'__aux__':c)===highlightHub);}
      ctx.globalAlpha=dim?0.16:1;
      ctx.fillStyle=n.color;
      ctx.beginPath();ctx.arc(n.x,n.y,n.r,0,7);ctx.fill();
      if(n.star){ctx.strokeStyle='#c5a55a';ctx.lineWidth=1.6;
        ctx.beginPath();ctx.arc(n.x,n.y,n.r+2.2,0,7);ctx.stroke();}
      if(n.id===hoverId){ctx.strokeStyle='#e8e0d4';ctx.lineWidth=1.5;
        ctx.beginPath();ctx.arc(n.x,n.y,n.r+3.5,0,7);ctx.stroke();}
      ctx.globalAlpha=1;
    }
  });
}
function loop(){if(!tableOn){sim();draw();}requestAnimationFrame(loop);}
buildGraph();loop();

/* ---------- 상호작용 ---------- */
const tip=document.getElementById('tip');
function nodeAt(mx,my){
  for(let i=nodes.length-1;i>=0;i--){const n=nodes[i];
    const dx=mx-n.x,dy=my-n.y;const rr=(n.r+5);
    if(dx*dx+dy*dy<=rr*rr)return n;}
  return null;
}
canvas.addEventListener('mousemove',ev=>{
  const mx=ev.clientX,my=ev.clientY;
  if(dragNode){dragNode.x=mx;dragNode.y=my;dragNode.vx=dragNode.vy=0;return;}
  const n=nodeAt(mx,my);
  hoverId=n?n.id:null;
  if(n&&n.kind==='el'){
    const chapNames=n.chaps.map(c=>{
      if(c==='__aux__')return '전반·부록';
      const h=hubs.find(h=>h.id===c);return h?h.name:c;}).join(' · ');
    tip.innerHTML=`<div class="t-title">${n.star?'★ ':''}${n.label}</div>`+
      (n.def?`<div>${n.def}</div>`:'')+
      `<div class="t-meta">${fams[n.fam].name} · 장 ${chapNames}</div>`;
    tip.style.opacity=1;
    let tx=mx+14,ty=my+14;
    if(tx+290>W)tx=mx-294;if(ty+120>H)ty=my-120;
    tip.style.left=tx+'px';tip.style.top=ty+'px';
  }else{tip.style.opacity=0;}
});
canvas.addEventListener('mousedown',ev=>{
  const n=nodeAt(ev.clientX,ev.clientY);
  if(n){
    if(n.kind==='hub'){
      const hid=n.id.slice(4);
      highlightHub=(highlightHub===hid)?null:hid;
    }else{dragNode=n;canvas.classList.add('drag');}
  }else{highlightHub=null;}
});
addEventListener('mouseup',()=>{dragNode=null;canvas.classList.remove('drag');});
canvas.addEventListener('mouseleave',()=>{tip.style.opacity=0;});
// 터치
canvas.addEventListener('touchstart',ev=>{
  const t=ev.touches[0];const n=nodeAt(t.clientX,t.clientY);
  if(n&&n.kind==='hub'){const hid=n.id.slice(4);
    highlightHub=(highlightHub===hid)?null:hid;}
  else if(n){dragNode=n;}},{passive:true});
canvas.addEventListener('touchmove',ev=>{
  if(dragNode){const t=ev.touches[0];dragNode.x=t.clientX;dragNode.y=t.clientY;
    dragNode.vx=dragNode.vy=0;}},{passive:true});
canvas.addEventListener('touchend',()=>{dragNode=null;});

/* ---------- 표 뷰 ---------- */
const tableView=document.getElementById('tableView');
let tableOn=false;
function renderTable(){
  const cols=hubs;   // 장 허브 순서
  let h='<table><thead><tr><th class="name">생각</th>';
  cols.forEach(c=>h+=`<th>${c.name}</th>`);
  h+='</tr></thead><tbody>';
  for(let f=1;f<=6;f++){
    if(famOff.has(String(f)))continue;
    const rows=elems.filter(e=>e.fam===f);
    if(!rows.length)continue;
    h+=`<tr class="fam-head"><td class="name" colspan="${cols.length+1}">`+
       `<span style="color:${fams[f].color}">●</span> ${fams[f].name}</td></tr>`;
    rows.forEach(e=>{
      h+=`<tr><td class="name">${e.star?'<span class="star-mark">★</span> ':''}${e.title}`+
         (e.def?`<span class="df">${e.def}</span>`:'')+`</td>`;
      cols.forEach(c=>{
        const inIt=e.chaps.some(x=>(x==='__aux__'?'__aux__':x)===c.id);
        h+=`<td class="cell">${inIt?'●':''}</td>`;
      });
      h+='</tr>';
    });
  }
  h+='</tbody></table>';
  tableView.innerHTML=h;
}
const btnMap=document.getElementById('btnMap'), btnTable=document.getElementById('btnTable');
btnMap.onclick=()=>{tableOn=false;tableView.classList.remove('show');
  btnMap.classList.add('on');btnTable.classList.remove('on');};
btnTable.onclick=()=>{tableOn=true;renderTable();tableView.classList.add('show');
  btnTable.classList.add('on');btnMap.classList.remove('on');tip.style.opacity=0;};
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
