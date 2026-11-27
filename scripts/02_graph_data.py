# ──────────────────────────────────────────────────────────────────────────
#  6. 「이거 그냥 당신 얘기잖아요」   ·   👁️ 세 층 지도 — 주춧돌 셋이 이어졌나
#  원본  <저자 vault>/.claude/gen_graph_data.py   —   손으로 고치지 마라 — .claude/publish_scripts.py 가 찍는다
# ──────────────────────────────────────────────────────────────────────────

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_graph_data.py — Build 3-Layer Galaxy Knowledge Graph Data:
  Layer 1 (Computational): 상징_감정 (22 Emoji/Emotion Nodes)
  Layer 2 (Algorithmic): 생각원소 (154 Thinking Element Nodes)
  Layer 3 (Implementational): 경험 두 갈래 — 📜신의전언(간접·읽은 것) · 🎞️일화원소(직접·겪은 것)
  
Generates JSON for golden-cage-book/interactive/reference_graph.html
"""
import os, re, json, sys, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import molt_map as _molt          # 🐍 탈피 코일의 자(尺) — SSOT

# ⚠️ 경로 교정 2026-09-18 — 구 경로 (사람 폴더 — 역할로 가렸다) 는 **전부 존재하지 않는다.**
#   폴더가 `On/me_문현지/제품/…` 로 옮겨진 뒤에도 생성기가 안 따라와, 다섯 소스가 모두
#   `os.path.exists()` 에서 조용히 False 가 되어 **빈 층으로 그려지고 있었다.**
#   조용한 실패라 그래프는 계속 나왔고, 그래서 아무도 못 봤다 — 「없음」은 발견이 아니라 자(尺) 신호.
VAULT_ROOT = "/Users/hyunjimoon/tolzul"          # Obsidian vault 루트 (vault 이름 = tolzul)
ME_DIR     = "/Users/hyunjimoon/tolzul/시공간멜로디/On/me_문현지"
TOLZUL_DIR = os.path.join(ME_DIR, "제품/소설")
ELEMENTS_DIR = os.path.join(TOLZUL_DIR, "_채석장/2차소통/원고/diagrams/생각원소")
GODS_DIR     = os.path.join(TOLZUL_DIR, "3차소통/_연료/🗣️현재_신의전언")
# 2026-09-18 이관: 일화원소 → me_문현지/기억🎞️ · 상징_감정 → me_문현지/감정_상징
# ⚠️ 2026-10-09 재교정: 상징이 하위폴더 `대본_감정이미지`(이모지 4개)를 가리켜 L1 이 4노드로 쪼그라들어 있었다.
#    실물 이모지 .md 16개는 부모 `감정_상징/` 에 있다. 하위폴더는 그 중 다섯의 사본 — SSOT 위반, 정리 필요.
EPISODES_DIR = os.path.join(ME_DIR, "생산자", "기억")               # L3 직접경험
SYMBOLS_DIR  = os.path.join(ME_DIR, "생산자", "감정_상징")        # L1 상징·감정

for _n, _d in [("ELEMENTS", ELEMENTS_DIR), ("GODS", GODS_DIR),
               ("EPISODES", EPISODES_DIR), ("SYMBOLS", SYMBOLS_DIR)]:
    if not os.path.isdir(_d):
        raise SystemExit(f"❌ {_n}_DIR 없음 — 경로가 또 썩었다: {_d}")

import unicodedata

# ── 공개 금지 제목 (⚓ 자장 2026-10-29) ───────────────────────────────────
#  이 토큰이 든 파일은 **노드로도 라벨로도 안 나간다.** 공개 그래프는 제목만으로도 공개다.
#  같은 목록이 .claude/redact_private.py 에도 있다 — 둘 다 고칠 것.
PRIVATE_TOKENS = ()   # ⚠️ 사본에서 비웠다 — 목록 자체가 비공개 제목이다.
#   공개 사본에 적으면 「제목만으로도 공개」라는 그 룰링을 이 줄이 깬다.
#   실제 목록은 원본 .claude/gen_graph_data.py 와 .claude/redact_private.py 에 있다.
def _private(name):
    return any(t in unicodedata.normalize("NFC", name) for t in PRIVATE_TOKENS)
def _vp(abspath):
    """노드 → vault 상대경로.  없으면 "" — 화면이 「열기」를 안 띄운다.
       ⚠️ NFC 정규화 필수: macOS listdir 이 NFD 를 주면 Obsidian 이 파일을 못 찾는다."""
    if not abspath or not os.path.exists(abspath): return ""
    return unicodedata.normalize("NFC", os.path.relpath(abspath, VAULT_ROOT))

GRAPH_HTML   = os.environ.get("GRAPH_OUT",
               "/Users/hyunjimoon/golden-cage-book/interactive/reference_graph.html")

# ── 최소복잡도 문지기 (2026-09-05) ────────────────────────────────────────────
# 「사용확률」 = 두 증거의 합.  본문에 나오나(chapter) × 일화가 무나(다이나모선).
#   둘 다 100 · 하나 50 · 없음 0.   MIN_USAGE 이상만 그래프에 올린다.
#   기본 0 = 전부(기존 동작 유지).  MIN_USAGE=100 이면 창업문학 최소 골격만.
# ⚠️ chapter의 「전」은 *전 장에 걸침*이다 — 숫자 없다고 미등장으로 세면 안 된다.
# 기본 100 = 창업문학 최소 골격 (2026-09-05 자장 룰링).  전부 보려면 MIN_USAGE=0.
# 2026-09-18 기본 100→50: 점선(주장) 층이 생겼으므로 「한 발만 걸친 것」도 그린다.
#   100 = 실선만(원고가 물고 배선도 있는 것) · 50 = 실선+점선 · 0 = 전부.
MIN_USAGE = int(os.environ.get("MIN_USAGE", "50"))

# MIN_WIRE — 생각원소가 *몇 편의 일화*에 물려야 남는가. 1=한 편이라도, 2=둘 이상.
MIN_WIRE  = int(os.environ.get("MIN_WIRE", "2"))  # 2 = 자장 룰링(2026-09-05)
# DROP_LEAVES — 뿌리에만 매달린 잎을 걷는다. **기본 0 (2026-09-06)**.
#   구 판정 "god 46·symbol 18이 전원 차수 1 = 구조에 기여 없음"은 원인을 잘못 짚었다.
#   기여가 없던 게 아니라 **이을 자리가 없었다** — 그래프에 장(章) 노드가 아예 없어서
#   상징도 신의전언도 뿌리 말고는 붙을 데가 없었다. 실물은 둘 다 장으로 연결된다:
#     상징     `- **장**: [[4⏱️_시계새장]]`
#     신의전언  frontmatter `chapter: 9` · `chapter_label: "7·9장"`
#   장 스파인을 넣었으므로 잎이 아니다. Marr L1(상징)이 통째로 빠진 그래프는
#   3층 그래프가 아니다.
DROP_LEAVES = os.environ.get("DROP_LEAVES", "0") == "1"
# PRUNE — ⛺️덮개 + 💣배선으로 **가차없이 깎는다**. 기본 **켜짐**.
#   자를 여기서 새로 만들지 않는다 — .claude/baesun_mcmf.py 의 survivors() 를 불러 쓴다.
#   남기는 것: 뿌리 · 장 스파인 열 · 자리 받은 일화 · 그 일화를 덮는 생각원소
#              · 📜신의전언과 🪞상징은 **장을 덮는** 최소 집합
#   📜🪞 가 다른 불을 쓰는 까닭 — 그 둘은 일화가 부르지 않고 frontmatter 로 장에 붙는다.
#   「살아남은 노드가 부르는 것만」으로 재면 0 이 되는데, 0 은 발견이 아니라 자가 틀린 신호다(#117).
#   ⚠️ vault 루트에서 돌려야 한다 (baesun_mcmf 가 상대경로를 쓴다).
# 🚨 2026-10-31 기본값을 뒤집었다. 전에는 기본 0 이었는데, tolzul→gcb **동기화가**
#   PRUNE 없이 이 생성기를 돌려 깎은 판(53/111)을 205/702 로 되돌렸다(gcb db55f0a).
#   룰링이 「가차없이 깎는다」이면 그게 기본이어야 한다 — 기본이 아니면 아무도 안 켠다.
#   전부 그리려면 `PRUNE=0 python3 .claude/gen_graph_data.py`.
PRUNE = os.environ.get("PRUNE", "1") != "0"
if PRUNE:
    # 손잡이를 하나로 줄인다 — 문턱 셋(MIN_USAGE·MIN_WIRE·RESCUE_WIRE)과 덮개를 겹쳐 쓰면
    # 무엇이 깎았는지 못 가린다. 덮개가 깎을 때는 문턱을 전부 열어 **덮개 하나만** 자가 된다.
    # 그래서 `python3 .claude/gen_graph_data.py` 한 줄로 이 화면이 재현된다.
    MIN_USAGE = MIN_WIRE = RESCUE_WIRE = 0
# RESCUE_WIRE — 본문 미등장이어도 *이만큼* 물리면 남긴다.
#   「본문 등장 AND 배선」의 AND가 Lexicon 개념을 벌한다.
#   실측 2026-09-05: 전체 2·3위 배선인 소통밀도(9)·op_st_ambiguity(9)가 ch=Lex라 잘렸다.
#   일화 다섯 편이 무는 개념은 본문에 없어도 골격이다 — 없는 게 오히려 캘 자리다.
RESCUE_WIRE = int(os.environ.get("RESCUE_WIRE", "5"))

# ── 2026-09-18 자(尺) 교체 ────────────────────────────────────────────────────
#  구 `_in_body(ch)` 는 원소 **frontmatter 의 자기 신고**만 봤다 — 원고를 안 읽었다.
#  그래서 586 간선이 관측이 아니라 *주장*이었다. 이제 3차 원고 본문을 실제로 스캔한다.
#  ⚠️ 원소 파일 자체는 여전히 채석장에만 있다(144편). 채석장 = 재고, 원고 = 진실.
MANUSCRIPT_DIR = os.path.join(TOLZUL_DIR, "4차소통/원고")
_CH_FILE = {1:"1🪞_거울새장",2:"2🔭_망원경새장",3:"3💒_스테인굴레스새장",4:"4⏱️_시계새장",
            5:"5🐀_101",6:"6🦋_나비사용자",7:"7🌷_튤립기술자",8:"8🌫️_안개투자자",
            9:"9🐦‍⬛_까마귀협력자",10:"10🧫_101"}
def _manuscript():
    """장번호 → 본문 텍스트.  없으면 빈 문자열."""
    out={}
    for c,f in _CH_FILE.items():
        fp=os.path.join(MANUSCRIPT_DIR,f+".md")
        out[c]=open(fp,encoding="utf-8").read() if os.path.exists(fp) else ""
    return out
_MANU=_manuscript()
if not any(_MANU.values()):
    raise SystemExit(f"❌ MANUSCRIPT_DIR 이 비었다 — 자가 또 썩었다: {MANUSCRIPT_DIR}")

def _cited(eid):
    """원소 id 를 **실제로 무는** 장 번호 집합.
       맨몸 g코드와 [[경로/eid|별칭]] 위키링크를 모두 센다(부분문자열이면 둘 다 잡힌다).
       짧은 형태 gN_NN 도 같은 원소로 센다."""
    short=re.match(r"(g\d_\d\d)",eid)
    hits=set()
    for c,t in _MANU.items():
        if not t: continue
        if eid in t or (short and re.search(re.escape(short.group(1))+r"(?![0-9])",t)):
            hits.add(c)
    return hits

def _in_body(ch):
    if not ch: return False
    return any(re.fullmatch(r"(10|[1-9])(-[0-9])?|전|부[0-9]?|1-[45]|6-9", part)
               for part in re.split(r"[·\s]+", ch))

def _episode_wired():
    """일화원소 다이나모선이 무는 생각원소 → 문 일화 편수."""
    from collections import Counter
    hit = Counter()
    if not os.path.isdir(EPISODES_DIR): return hit
    for f in os.listdir(EPISODES_DIR):
        if not (f.startswith("ep") and f.endswith(".md")) or _private(f): continue
        txt = open(os.path.join(EPISODES_DIR, f), encoding="utf-8").read()
        i = txt.find("## 🔗 다이나모선")
        if i < 0: continue
        # ⚠️ 2026-09-18 — 링크 83/138 이 **전체 경로**였는데 원소 id 와 통째로 비교해
        #   교집합이 0 이었다. 실측 73 원소가 통째로 안 보였다. basename 으로 잰다.
        seen = {m.group(1).strip().split("/")[-1]
                for m in re.finditer(r"\[\[([^\]|]+)", txt[i:])}
        for k in seen: hit[k] += 1
    return hit

def parse_fm(path):
    if not os.path.exists(path): return {}
    txt = open(path, encoding="utf-8").read().split("\n")
    if len(txt) < 3 or txt[0] != "---": return {}
    try:
        end = txt.index("---", 1)
    except ValueError:
        return {}
    fm = {}
    for line in txt[1:end]:
        m = re.match(r'^([a-z_가-힣]+):\s*(.*)$', line)   # 한글 키(마찰·연료) 허용
        if not m: continue
        k, v = m.group(1), m.group(2).strip().strip('"')
        fm[k] = v
    return fm

POLES = {"🦋":"user", "🧅":"tech", "🌫️":"investor", "🐦‍⬛":"collab"}

# ── 자리 출처 `pos` — 2026-10-29 ─────────────────────────────────────────────
#  👁️ 눈의 자는 「적힌 것만 센다」인데, 정작 이 지도가 **자리를 누가 박았는지**
#  말하지 않았다. 55편의 일화가 이웃 투표로 받은 자리를, 제 입으로 신고한 자리와
#  똑같은 점으로 그렸다 — 그림이 추정을 관측으로 둔갑시킨 셈이다.
#    self — 파일이 제 장을 적었다 (상징 `- **장**:` · 신의전언 frontmatter · 원소 frontmatter)
#    obs  — 파일은 안 적었는데 **원고가 문다** (원소만. 신고보다 센 증거라 자리를 준다)
#    vote — **이웃이 투표**해 준 자리 (일화만. 일화 파일엔 장이 아예 없다)
#    none — 자리 없음. 전반·부록 열에 선다 — 숨길 결손이 아니라 **산출물**이다.
POS_SELF, POS_OBS, POS_VOTE, POS_NONE = "self", "obs", "vote", "none"

# ── 장(章) 스파인 — 네 층이 공통으로 붙는 축 (2026-09-06 신설) ──────────────
# ── 짝색 다섯 (SSOT = .claude/CLAUDE.md §거울짝) ─────────────────────────
#   1↔6 파랑 · 2↔7 보라 · 3↔8 빨강 · 4↔9 초록 · 5↔10 노랑(중앙 101).
#   색이 극이 아니라 **거울짝**을 뜻한다(재해소 2026-09-21 ⚓ 룰링).
PAIR_COLOR = {1:"#0026FB", 6:"#0026FB", 2:"#491786", 7:"#491786",
              3:"#F82218", 8:"#F82218", 4:"#006610", 9:"#006610",
              5:"#FFD53A", 10:"#FFD53A", 0:"#9a8f7a"}
# 📕·다·세·세다는 **짝이 없다** — 공간 열이 짝색 다섯을 나눠 갖고, 시간 하나와 인물 셋은
#   그 위를 가로지른다. 짝색을 주면 제 것 아닌 짝을 입는다. 그래서 따로 둔다.
NOPAIR = {"📕":"#B4443A", "🔫":"#cfc6b4", "🧫":"#cfc6b4"}
# 띠로 그리는 넷 — 상징 줄에는 안 세운다(아래 「인물 띠 넷」). 세다는 파일이 없어 띠에서만 산다.
BAND_SYMS = {"📕", "🔫", "🧫"}

# 장 이름도 글자로 쓴다 (룰링 2026-11-25 — 상징과 같은 까닭). 이모지가 제 색을 들고 와
#   짝색 다섯과 부딪혔고, 🧫이 10장과 세를 겹쳐 가리켰다. 주소는 안 바꾼다 — 라벨만 간다.
CHAP = {1:"1 거울",2:"2 망원경",3:"3 스테인굴레스",4:"4 시계",5:"5 101₂호",
        6:"6 나비",7:"7 튤립",8:"8 안개",9:"9 까마귀",10:"10 투향"}
def _chaps(*fields):
    """'5·7·부2' · '7·9장' · '1-4' · '전' · 9 → {장번호}. 부록·전반은 0(전반) 으로."""
    out=set()
    for f in fields:
        if not f: continue
        for part in re.split(r"[·,\s]+", str(f)):
            part=part.strip().replace("장","")
            if not part: continue
            m=re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
            if m:
                a,b=int(m.group(1)),int(m.group(2))
                out |= {c for c in range(min(a,b),max(a,b)+1) if c in CHAP}; continue
            if re.fullmatch(r"\d+", part) and int(part) in CHAP: out.add(int(part)); continue
            if part in ("전","전반") or part.startswith("부"): out.add(0)
    return out

nodes = []
edges = []
node_ids = set()
# 🪓 2026-11-27 가지치기 — DATA 에서 **화면이 안 읽는 밭**을 뺐다.
#   · depth · marr_layer · r : reference_graph.html 이 한 번도 안 읽는다(반지름은 RAD 가 센다).
#   · emo · emov (구 CHAP_EMO) : 감정 궤적 겹을 거두면서 읽는 눈이 사라졌다.
#     열 장 중 값이 있던 것은 **셋뿐**(5 혼재 0 · 8 바닥 −2 · 10 꼭대기 +2)이고
#     6·7·9 는 그림이 제 손으로 이어 그린 점이었다. 3/10 은 궤적이 아니다.
#     배정 자체는 살아 있다 — SSOT 는 🧠LEXICON §12감정×6연이고, 여기 싣지 않을 뿐이다.
CHAP_POLE = {6:"🦋", 7:"🧅", 8:"🌫️", 9:"🐦‍⬛"}   # 둥지 네 장 = 네 극
for c,lab in CHAP.items():
    nodes.append({"id":f"ch{c}","label":lab,"pc":PAIR_COLOR.get(c,PAIR_COLOR[0]),
                  "layer":"chapter","chap":c,
                  "pole":CHAP_POLE.get(c,""), "pos":"spine",
                  "vpath":_vp(os.path.join(MANUSCRIPT_DIR, _CH_FILE[c]+".md"))})
    node_ids.add(f"ch{c}")
nodes.append({"id":"ch0","label":"전반·부록","layer":"chapter","chap":0,"pos":"spine"})
node_ids.add("ch0")

# 1. Root Node
nodes.append({"id": "황금새장을열다", "label": "🪞 투향", "layer": "root", "chap": 0})
node_ids.add("황금새장을열다")
for c in list(CHAP)+[0]: edges.append({"s": "황금새장을열다", "t": f"ch{c}"})

# 2. Layer 1: 상징_감정 (Computational / 22 Nodes)
# L1 상징 = **이모지 파일만** (2026-09-06). 폴더에 상징 아닌 것이 섞여 있었다 —
#   세는세다로싹튼다(5~10연 감정 배정 설계) · 선악상변화(그 짝, 생리 축)
#   · claude_emotions · 감정교육 ⏱️.  넷 다 물밑 설계라 L1 노드로 서면 안 된다.
# ⑶ 🔫(多)·🧫(世) 는 키가 `**자리**` 라 위 정규식에 애초에 안 걸리지만, 걸리게 고치지 않는다.
#   두 파일이 **스스로** 「챕터 상징 아님 — 책 전체를 관통하는 메타 상징」이라 적어 두었다
#   (룰링 2026-07-28). 거기 적힌 5·10장 링크로 장을 붙이면 관측이 아니라 **파생**이고,
#   그것은 #155 의 「백필은 하지 않았다 — 파생시키면 실제값이 언제나 기대값과 같아져
#   이탈이 영영 안 읽힌다」와 같은 자리다. 전반에 둔다.
#   그 결과 10장 상징 칸은 0으로 남는다 — 숨길 결손이 아니라 산출물이다(빈칸이 다음 책).
META_SYMBOLS = {"🔫", "🧫"}
# 2026-11-08 — 보이는 글자만 간다(룰링 2026-11-07: 기술자 극의 글자는 🌷가 아니라 🧅).
#   주소는 안 바꾼다 — 상징 파일 이름 `🌷.md`도, 원고 `7🌷_튤립기술자.md`도 그대로다.
#   id 는 주소(sid)로 두고 **label 만** 갈아 끼운다. 공개 그래프가 아직 🌷를 띄우고 있었다.
GLYPH = {"🌷": "🧅"}
# ── 상징 열넷 = 글자로 쓴다 (룰링 2026-11-25) ─────────────────────────
#   까닭 둘. ⑴ **색** — 짝색 다섯(1↔6 파랑 · 2↔7 보라 · 3↔8 빨강 · 4↔9 초록 · 5↔10 노랑)이
#   배정을 끝냈는데 이모지가 제 색을 들고 와 짝색과 부딪힌다. 글자는 색을 안 들고 온다.
#   ⑵ **글리프 충돌** — 7장이 🌷/🧅 둘, 5장이 🐀/🚪 둘, 🧫이 세이면서 10장 주소였다.
#   글자로 쓰면 셋 다 사라진다. **주소(파일 이름)는 안 바꾼다 — 라벨만 간다.**
#   gcb #81 「상징 명부 — 책에 남는 열넷」이 SSOT다. 여기 없는 글자는 vault 주소일 뿐이다.
SYM14 = {"🪞":"거울", "🔭":"망원경", "💒":"스테인굴레스", "⏱️":"시계", "🐀":"쥐",
         "🦋":"나비", "🌷":"구근", "🌫️":"안개", "🐦‍⬛":"까마귀",
         "📕":"붉은 일기장", "🔫":"다", "🧫":"세"}
#   빠진 둘 — 10장 상징은 설계도에 **빈칸**이고(빈칸이 다음 책), 세다는 **파일이 없다**.
#   0으로 적지 않는다. 생기면 여기 한 줄.
_is_symbol = lambda f: bool(re.match(r"^[\U0001F000-\U0001FAFF\u2190-\u2BFF\uFE0F\u200D]+\.md$", f))
symbol_links = []
symbol_files = [f for f in os.listdir(SYMBOLS_DIR) if f.endswith(".md") and _is_symbol(f) and not _private(f)] if os.path.exists(SYMBOLS_DIR) else []
for sf in symbol_files:
    sid = sf.replace(".md", "")
    if sid in node_ids: continue
    _txt = open(os.path.join(SYMBOLS_DIR, sf), encoding="utf-8").read()
    # ⚠️ 2026-10-14 — 장 줄을 **못 읽고 있었다**. 상징 16개가 하나도 빠짐없이 「전반」에 쌓여
    #   있었고(실측 16/16), 제품지도(#135)의 상징 열이 1~10장 전부 점선이었다. 원인 셋:
    #     ⑴ 링크가 전체 경로(`[[시공간멜로디/On/.../1🪞_거울새장]]`)라
    #        `re.match(r"\d+")` 가 첫 글자 「시」에서 떨어진다 → 언제나 0
    #     ⑵ re.search 라 **첫 링크 하나만** 읽는다 → 🪞(1·5·9)·🚪(5↔10)의 나머지가 사라진다
    #   줄 전체를 잡고, 링크마다 **파일 이름만** 떼어 앞 숫자를 읽는다.
    _ml = re.search(r"^\s*-\s*\*\*장\*\*\s*:\s*(.+)$", _txt, re.M)
    _cs = set()
    if _ml and sid not in META_SYMBOLS:
        for _l in re.findall(r"\[\[(.*?)\]\]", _ml.group(1)):
            _d = re.match(r"(\d+)", _l.split("|")[0].strip().split("/")[-1])
            if _d: _cs |= _chaps(_d.group(1))
    _first = min(_cs) if _cs else 0
    if sid not in SYM14: continue          # 열넷 밖은 vault 주소일 뿐 — 책에도 그래프에도 안 간다
    # ⚠️ 2026-11-25 — **띠로 가는 넷은 줄에서 뺀다.** 둘 다 그리면 1장에서 📕이 거울을
    #   덮고, 전반 칸의 다·세가 화면 오른쪽 끝에 잘린다. 공간 열은 줄에 서고(한 장에 하나)
    #   시간 하나와 인물 셋은 **구간**이라 띠로 간다 — 같은 것을 두 꼴로 그리지 않는다.
    if sid in BAND_SYMS: continue
    nodes.append({"id": sid, "label": SYM14[sid], "layer": "symbol",
                  "pc": NOPAIR.get(sid, PAIR_COLOR.get(_first, PAIR_COLOR[0])),
                  "chap": _first, "pos": (POS_SELF if _cs else POS_NONE),
                  "pole": (sid if sid in POLES else ""),
                  "vpath": _vp(os.path.join(SYMBOLS_DIR, sf))})
    node_ids.add(sid)
    for c in (_cs or {0}): edges.append({"s": sid, "t": f"ch{c}"})
    # ⚠️ 2026-09-20 — 상징 파일의 위키링크를 **아예 안 읽고 있었다**.
    #   원소·일화만 읽은 탓에 상징 15개가 장 이름표에만 매달린 바큇살이 됐다
    #   (허브 12개를 빼면 원작 47 + 상징 15가 통째로 떨어져 나갔다).
    #   상징 루프는 다른 층보다 **먼저** 돌아 node_ids 가 아직 비어 있으므로,
    #   일화와 같은 방식으로 뒤로 미뤄 둔다 — 여기서 이으면 장 노드밖에 못 문다.
    _txt_links = re.findall(r'\[\[(.*?)\]\]', _txt)
    symbol_links.extend((sid, l.split("|")[0].strip().split("/")[-1]) for l in _txt_links)

# 3. Layer 3: 신의전언 (Implementational / Classical Primary Sources)
god_files = [f for f in os.listdir(GODS_DIR) if f.endswith(".md") and not _private(f)] if os.path.exists(GODS_DIR) else []
for gf in god_files:
    gid = gf.replace(".md", "")
    if gid in node_ids: continue
    fm = parse_fm(os.path.join(GODS_DIR, gf))
    label = fm.get("work", gid)
    if not label or label == gid:
        label = gid.replace("📜", "")
    _cs = _chaps(fm.get("chapter_label",""), fm.get("chapter",""))
    nodes.append({"id": gid, "label": "📜 " + label, "layer": "god",
                  "chap": (min(_cs) if _cs else 0),
                  "pos": (POS_SELF if _cs else POS_NONE),
                  "vpath": _vp(os.path.join(GODS_DIR, gf))})
    node_ids.add(gid)
    for c in (_cs or {0}): edges.append({"s": gid, "t": f"ch{c}"})

# 4. Layer 2: 생각원소 (Algorithmic / 154 Concept Nodes)
elem_files = [f for f in os.listdir(ELEMENTS_DIR) if f.endswith(".md") and not _private(f)] if os.path.exists(ELEMENTS_DIR) else []
_WIRE_N = _episode_wired()
_WIRED = set(_WIRE_N)
_cut = []
for ef in elem_files:
    eid = ef.replace(".md", "")
    if eid in node_ids: continue
    # ⚠️ 2026-09-20 — _obs 는 아래 엣지 두 줄이 **문턱과 무관하게** 쓴다.
    #   MIN_USAGE>0 블록 안에 두었더니 「전부 보기」(MIN_USAGE=0)가 NameError 로 터졌다.
    #   감사하려고 문을 여는 순간 자가 부러지는 꼴이라 블록 밖으로 올린다.
    _obs = _cited(eid)                          # 원고가 실제로 무는 장 (관측)
    if MIN_USAGE > 0:
        _ch = parse_fm(os.path.join(ELEMENTS_DIR, ef)).get("chapter", "")
        _usage = 100 if (_obs and eid in _WIRED) else (50 if (_obs or eid in _WIRED) else 0)
        _w = _WIRE_N.get(eid, 0)
        if _w >= RESCUE_WIRE:
            _usage = 100  # 구제: 강한 배선이 본문 부재를 상쇄
        # 원고가 물면 배선 문턱은 면제한다 — 책 안에 있는 것을 배선 없다고 지우지 않는다
        if _usage < MIN_USAGE or (not _obs and _w < MIN_WIRE):
            _cut.append((eid, _usage)); continue
    _cs = _chaps(parse_fm(os.path.join(ELEMENTS_DIR, ef)).get("chapter",""))
    # ⚠️ 2026-10-29 — 신고가 없으면 **관측된 장**에 세운다.
    #   구 코드는 _cs 가 비면 무조건 chap 0(전반) 이었다. 원고가 7장에서 무는 원소가
    #   「자리 없음」 열에 서 있었고, 동시에 ch0 로 가는 주장 간선까지 하나 얹혔다 —
    #   원고가 무는 것은 신고보다 **센 증거**다. 관측을 전반으로 깎지 않는다.
    if _cs:    _chap, _pos, _claim = min(_cs), POS_SELF, _cs
    elif _obs: _chap, _pos, _claim = min(_obs), POS_OBS, set()
    else:      _chap, _pos, _claim = 0, POS_NONE, {0}
    nodes.append({"id": eid, "label": eid, "layer": "element",
                  "chap": _chap, "pos": _pos,
                  "vpath": _vp(os.path.join(ELEMENTS_DIR, ef))})
    node_ids.add(eid)
    for c in _claim:
        edges.append({"s": eid, "t": f"ch{c}", "obs": 1 if c in _obs else 0})
    for c in sorted(_obs - _claim):             # 원고는 무는데 원소가 신고 안 한 장
        edges.append({"s": eid, "t": f"ch{c}", "obs": 1})
    # Parse wikilinks inside element file to build edges
    content = open(os.path.join(ELEMENTS_DIR, ef), encoding="utf-8").read()
    # 2026-09-06: 구 코드는 `nid in target or target in nid` 부분일치로 이었다.
    #   짧은 id가 긴 id에 먹혀 헛엣지가 생긴다(g4_01_거울 ⊂ 여러 이름). 정확 일치만 쓴다.
    for link in re.findall(r'\[\[(.*?)\]\]', content):
        target = link.split("|")[0].strip().split("/")[-1]
        if target in node_ids and target != eid:
            edges.append({"s": eid, "t": target})
# 5. Layer 3-b: 🎞️일화원소 (Implementational / 직접경험)
#    신의전언(📜 간접경험)과 같은 L3 층. 차이는 layer 값("episode") 하나.
#    엣지는 wikilink *정확 일치*로만 만든다 — 생각원소의 느슨한 부분일치와 달리
#    일화는 어떤 원소를 낳았는지가 주장이므로, 헛엣지가 곧 거짓 주장이 된다.
# ⚠️ 2026-09-18 — 「00_ 아닌 모든 .md」는 **덜렁이(Type I)** 필터였다.
#   폴더가 일화 전용일 때만 참인 규칙인데, `기억🎞️` 로 옮기며 점·향·🗣️feedback 이 같이 살게 되어
#   셋이 가짜 일화 노드로 섰다(48 → 51). 폴더가 아니라 **이름**으로 잰다 — `_episode_wired()` 와 같은 자.
episode_files = sorted(f for f in os.listdir(EPISODES_DIR)
                       if f.startswith("ep") and f.endswith(".md") and not _private(f)) if os.path.exists(EPISODES_DIR) else []
# 소심이(Type II) 대칭 점검 — 이름 규약을 안 따르는 일화가 생기면 여기서 잡힌다.
_orphan = [f for f in os.listdir(EPISODES_DIR)
           if f.endswith(".md") and not f.startswith(("ep", "00_", "점", "향", "🗣️"))]
if _orphan:
    print(f"   ⚠️ ep 로 시작 안 하는 .md {len(_orphan)}건 — 일화면 개명, 아니면 이 목록에 등록: {_orphan}")
episode_links = []
for pf in episode_files:
    pid = pf.replace(".md", "")
    fm = parse_fm(os.path.join(EPISODES_DIR, pf))
    label = "🎞️ " + pid.split("_", 1)[-1].replace("_", " ")
    # 🔥다이나모선: 마찰(고통) 기록 여부가 노드/선의 발광을 결정한다
    fric = fm.get("마찰", "")
    _pole = next((e for e in POLES if e in fm.get("극","")), "")
    # 🐍 탈피 코일 — 자(尺)는 molt_map 하나뿐이다. 날짜 파서를 여기서 또 쓰지 않는다.
    _ym, _prec = _molt.to_ym(fm.get("날짜", ""))
    nodes.append({"id": pid, "label": label,
                  "layer": "episode", "friction": fric, "dynamo": bool(fric), "pole": _pole,
                  "coil": _molt.coil_of(_ym, _prec) or "",
                  "vpath": _vp(os.path.join(EPISODES_DIR, pf))})
    node_ids.add(pid)
    content = open(os.path.join(EPISODES_DIR, pf), encoding="utf-8").read()
    for link in re.findall(r'\[\[(.*?)\]\]', content):
        # ⚠️ 2026-09-20 — basename 으로 잰다. 여기만 전체경로를 통째로 비교하고 있었다.
        #   같은 버그를 `_episode_wired()` 에서는 2026-09-18 에 이미 고쳤는데 **그리는 쪽엔
        #   안 따라왔다** — 그래서 거르는 자와 긋는 자가 다른 책을 봤다. 실측: 일화 링크
        #   626개 중 37%가 전체경로 → element↔episode 간선이 202 이어야 할 자리에 **2개**.
        #   다이나모선(L3→L2 코일)이 통째로 안 보였고, 그 없는 코일 위에서 「겔·평균 차수
        #   7.4」 진단이 나왔다. 고친 뒤 ⟨k⟩ 3.36→5.37, ch0 제거 시 최대덩어리 42%→84%.
        episode_links.append((pid, link.split("|")[0].strip().split("/")[-1]))

# 일화의 장 = 그 일화가 무는 생각원소들의 최빈 장 (2026-09-06).
#   일화 자체엔 chapter 가 없다. 없다고 전부 「전반」에 몰면 47개가 한 열에 뭉쳐
#   가로축이 죽는다 — 무는 원소가 어느 장에 사는지로 자리를 준다.
_elem_chap = {n["id"]: n.get("chap", 0) for n in nodes if n["layer"] == "element"}
_ep_votes = {}
for _pid, _t in episode_links:
    _t = _t.split("/")[-1]
    if _t in _elem_chap and _elem_chap[_t]:
        _ep_votes.setdefault(_pid, []).append(_elem_chap[_t])
def _declared_chap(eid):
    """일화가 **제 입으로** 신고한 장 = frontmatter `투향장:`.

    ⚠️ 2026-11-26 — 아래 옛 주석의 전제가 깨졌다. 「일화 파일엔 장이 아예 없다」고
       적혀 있었고 그래서 자리를 전부 투표로 줬는데, 실측하니 **67편 중 30편이
       `투향장:` 을 신고한다.** 신고가 있는데 투표로 덮으면 자리가 틀린다 —
       ep27 은 9장을 신고했는데 8장에 앉았고, ep35 는 10장을 신고했는데 2장에 앉았다.
       자리 출처의 서열(self > obs > vote)은 이미 이 파일에 적혀 있다. 그걸 지킨다.
       값 뒤에 「# … 실측 …」 주석이 붙는 일이 있어 앞 숫자만 끊어 읽는다.
    """
    for d in (EPISODES_DIR,):
        p = os.path.join(d, eid + ".md")
        if not os.path.exists(p): continue
        try: t = open(p, encoding="utf-8").read()
        except Exception: continue
        m = re.search(r"^투향장:\s*(\d{1,2})\b", t, flags=re.M)
        if m and 0 < int(m.group(1)) <= 10: return int(m.group(1))
    return None

_self_seat = 0
for n in nodes:
    if n["layer"] == "episode":
        _d = _declared_chap(n["id"])
        v = _ep_votes.get(n["id"], [])
        if _d:
            n["chap"], n["pos"] = _d, POS_SELF; _self_seat += 1
        else:
            # 신고가 없으면 자리는 남이 투표해 준 것이다 — 신고한 점과 같은 모양으로
            # 그리면 그림이 추정을 관측이라 말하게 된다. 그래서 도넛으로 남긴다.
            n["chap"] = max(set(v), key=v.count) if v else 0
            n["pos"] = POS_VOTE if v else POS_NONE
print("   🪑 일화 자리 — 제 입으로 신고 %d · 이웃 투표 %d · 없음 %d"
      % (_self_seat,
         sum(1 for n in nodes if n["layer"] == "episode" and n["pos"] == POS_VOTE),
         sum(1 for n in nodes if n["layer"] == "episode" and n["pos"] == POS_NONE)))

dynamo_ids = {n['id'] for n in nodes if n.get('dynamo')}
# 일화 → 생각원소 엣지는 모든 노드가 등록된 뒤 정확 일치로 연결
for pid, target in episode_links:
    if target in node_ids and target != pid:
        edges.append({"s": pid, "t": target, "dynamo": pid in dynamo_ids})

# 상징 → (원소·원작·일화) 도 같은 자리에서. 정확 일치만.
_sym_drawn = 0
for sid, target in symbol_links:
    if target in node_ids and target != sid:
        edges.append({"s": sid, "t": target}); _sym_drawn += 1
print(f"   🪞 상징 링크: {len(symbol_links)}개 중 {_sym_drawn}개 이음")

# 4극 — 구 get_sector 는 이름 부분일치 + `abs(hash(nid))%4` 폴백이라 절반이 난수였다(2026-09-06 폐기).
#   실데이터가 있다: 일화 frontmatter `극:` · 상징 파일명 넷 · 둥지 6~9장.
#   좌표는 층×장이 이미 쓰므로 극은 **테두리 색** 한 채널로 얹는다.
def get_sector(nid):
    return 0

# 잎 제거: 📜신의전언·🔵상징 중 뿌리에만 매달린 것
# ⚠️ 2026-09-20 — 같은 두 노드를 잇는 선을 **링크가 나올 때마다** 그었다.
#   한 편이 같은 원소를 다섯 번 부르면 다섯 줄. 실측 186/658(28%)이 겹선이라
#   평균 차수 ⟨k⟩ 가 통째로 부풀고, 그 값 위에서 「겔」 판정이 나왔다.
#   쌍으로 접되 무게(w)를 남긴다 — 여러 번 부른 것은 굵게 그리면 되지, 여러 줄이 아니다.
#   플래그(obs·dynamo)는 OR 로 합친다. 한 번이라도 관측됐으면 관측된 선이다.
def _fold(edges):
    seen = {}
    for e in edges:
        k = tuple(sorted((e["s"], e["t"])))
        if k in seen:
            t = seen[k]; t["w"] = t.get("w", 1) + 1
            for f in ("obs", "dynamo"):
                if e.get(f): t[f] = e[f]
        else:
            n = dict(e); n["w"] = 1; seen[k] = n
    return list(seen.values())

# 원고 전문 — 아래 자 둘(주춧돌 실측 · 이름 부르나)이 같이 쓴다. 한 번만 읽는다.
_PAGE_DIR = os.path.join(TOLZUL_DIR, "4차소통/원고")
_PAGE_FILES = ["0_여는물음","0_머릿말","0_인물소개","1🪞_거울새장","2🔭_망원경새장",
               "3💒_스테인굴레스새장","4⏱️_시계새장","5🐀_101","6🦋_나비사용자",
               "7🌷_튤립기술자","8🌫️_안개투자자","9🐦‍⬛_까마귀협력자","10🧫_101"]
_pages = {}
for _f in _PAGE_FILES:
    try: _pages[_f] = unicodedata.normalize("NFC", open(os.path.join(_PAGE_DIR, _f + ".md"), encoding="utf-8").read())
    except Exception: pass
_page = "".join(_pages.values())

def _name_probes(fm, nid):
    """원고가 이 책을 부를 만한 **이름**. 원고의 인용 규약이 「번호 + 한국어 제목」이고
       저자는 성만 적히므로, ⑴ 한국어 이름의 각 토막 ⑵ 파일명의 한국어 토막
       ⑶ 원제 ⑷ 번역 제목 을 다 넣는다. 두 글자 이하는 버린다 — 아무 데나 걸린다."""
    out = []
    out += [t for t in re.split(r"\s+", fm.get("author_ko", "")) if t]
    out += [t for t in re.split(r"[_\s]+", nid.replace("📜", "")) if re.search(r"[가-힣]", t)]
    for k in ("work", "work_ko", "title_ko"):
        v = fm.get(k, "")
        if v: out.append(re.sub(r"^\d{3}\s*", "", v).strip())
    seen, keep = set(), []
    for t in out:
        t = t.strip(" 『』「」\"'")
        # ⚠️ 길이 문턱이 둘이다 — 한국어 이름은 두 글자가 보통이다(「오웰」·「표범」).
        #    라틴 글자에만 >3 을 건다. 처음에 >2 하나로 재서 오웰·람페두사를 잃었다.
        _ok = len(t) >= 2 if re.search(r"[가-힣]", t) else len(t) > 3
        if _ok and t not in seen:
            seen.add(t); keep.append(t)
    return keep

_mute = []
for _n in nodes:
    if _n["layer"] != "god": continue
    try: _fm = parse_fm(os.path.join(GODS_DIR, _n["id"] + ".md")) or {}
    except Exception: _fm = {}
    _ps = _name_probes(_fm, _n["id"])
    _hit = [p for p in _ps if p in _page]
    _n["named"] = bool(_hit)
    if not _hit: _mute.append((_n["id"], _ps))
print("   📏 원고가 이름을 부르나 — 📜 %d 중 **안 부르는 것 %d**"
      % (sum(1 for n in nodes if n["layer"] == "god"), len(_mute)))
for _i, _p in _mute:
    print("      🚨 %-44s 찾아본 이름 %s" % (_i, _p))

# ── 🧱 주춧돌 셋 — 장마다 무엇이 **최종으로** 앉았나 (2026-11-27 신설) ──────────
#    원본 = 원고 폴더의 `주춧돌_셋_장마다.md` 한 표. 발행본은 gcb #166 이다.
#
#    왜 필요한가 — 자리를 일화 frontmatter 의 `투향장:` 으로 주면 **신고한 것이 전부**
#    들어온다(30편). 그런데 장마다 앉는 것은 그중 **고른 둘**이다. 표가 코멘트에만
#    있어서 생성기가 못 읽었고, 그래서 그래프와 표가 열 편 어긋나 있었다.
#    ⚠️ 표를 여기 베끼지 않는다 — 읽는다. 베끼면 SSOT 가 둘이 된다.
_CORNER_MD = os.path.join(_PAGE_DIR, "주춧돌_셋_장마다.md")
CORNER = {}
try:
    _rows = [l for l in open(_CORNER_MD, encoding="utf-8").read().split("\n")
             if re.match(r"^\|\s*\d{1,2}\s*\|", l)]
    for _l in _rows:
        _c = [x.strip() for x in _l.strip().strip("|").split("|")]
        _ch = int(_c[0])
        _split = lambda t: [x.strip() for x in t.split("·")
                            if x.strip() and x.strip() not in ("—", "(빈칸)", "**(빈칸)**")]
        CORNER[_ch] = {"ep": [x.strip("*") for x in _split(_c[1])],
                       "g":  [x.strip("*") for x in _split(_c[2])],
                       "case": [x.strip("*") for x in _split(_c[3])]}
except Exception as _e:
    print("   🚨 주춧돌 표를 못 읽었다 — 자리를 신고(투향장)로 둔다:", _e)

if CORNER:
    # ── 🧱 표가 세 층을 **통째로** 짓는다 (2026-11-27 단순화 룰링) ─────────────
    #   전에는 자가 아홉이었다 — 최소비용최대흐름·탐욕 최소덮개·문턱 셋·자리 출처 네 값·
    #   `투향장:` 신고·글자째 인용·이름 부르나. 그런데 👁️ 눈 셋이 토큰검색·통독·반증
    #   **서로 다른 방법으로 같은 답에 닿았고**, 판을 가른 자는 하나뿐이었다 —
    #   *원고를 펴서 그 장에 그게 있나 본다.* 나머지 여덟은 답을 못 바꿨다.
    #   그래서 그 하나만 남긴다. 종이에 다섯 줄로 되는 것이 이 지도의 자다.
    #   ⚠️ baesun_mcmf · jisik_cover 는 **지우지 않는다** — 「채석장에서 무엇을 고를까」를
    #      푸는 기획 도구로 제자리에 둔다. 이 지도는 「책에 무엇이 들어갔나」만 묻는다.
    #      두 물음이 한 표에 있던 것이 빚이었다.
    _drop = {n["id"] for n in nodes if n["layer"] in ("episode", "element")}
    nodes = [n for n in nodes if n["id"] not in _drop]
    edges = [e for e in edges if e["s"] not in _drop and e["t"] not in _drop]
    node_ids -= _drop

    _EPT = {}
    for _f in os.listdir(EPISODES_DIR):
        _m = re.match(r"^(ep\d+)_(.+)\.md$", _f)
        if _m: _EPT[_m.group(1)] = _m.group(2).replace("_", " ")
    for _ch, _v in sorted(CORNER.items()):
        for _e in _v["ep"]:                       # 경험 — §1 이 쥔 일화
            _id = "ex_%d_%s" % (_ch, _e)
            nodes.append({"id": _id, "label": "🎞️ " + _EPT.get(_e, _e), "depth": 3,
                          "marr_layer": 3, "layer": "episode", "r": 11, "chap": _ch,
                          "pos": POS_SELF, "pole": "", "ep": _e})
            node_ids.add(_id); edges.append({"s": _id, "t": "ch%d" % _ch, "w": 1})
        for _g in _v["g"]:                        # 지식 — §2 가 세운 것 (이름 그대로)
            _id = "kn_%d_%s" % (_ch, re.sub(r"\s+", "_", _g))
            nodes.append({"id": _id, "label": _g, "depth": 2, "marr_layer": 2,
                          "layer": "element", "r": 8, "chap": _ch,
                          "pos": POS_SELF, "pole": ""})
            node_ids.add(_id); edges.append({"s": _id, "t": "ch%d" % _ch, "w": 1})
    _ep_seat = {e: c for c, v in CORNER.items() for e in v["ep"]}
    # 🏭 사례 — 원고가 쥔 이름. **신고가 아니라 실측이다**: 그 장 원고에 글자째 있나.
    #    열 방 중 5·10 은 마디면이라 사례가 0 이고, 그 빈칸은 결손이 아니라 산출물이다.
    _CHFILE = {1:"1🪞_거울새장", 2:"2🔭_망원경새장", 3:"3💒_스테인굴레스새장",
               4:"4⏱️_시계새장", 5:"5🐀_101", 6:"6🦋_나비사용자", 7:"7🌷_튤립기술자",
               8:"8🌫️_안개투자자", 9:"9🐦‍⬛_까마귀협력자", 10:"10🧫_101"}
    _case_hit = 0
    for _ch, _v in sorted(CORNER.items()):
        for _nm in _v["case"]:
            _txt = _pages.get(_CHFILE.get(_ch, ""), "")
            _in = _nm in _txt
            _case_hit += bool(_in)
            _cid = "case_%02d_%s" % (_ch, re.sub(r"\s+", "_", _nm))
            nodes.append({"id": _cid, "label": _nm,
                          "layer": "case", "chap": _ch,
                          "pos": POS_SELF if _in else POS_NONE, "pole": ""})
            node_ids.add(_cid)
            edges.append({"s": _cid, "t": "ch%d" % _ch, "w": 1})
    _ncase = sum(len(v["case"]) for v in CORNER.values())
    _nep   = sum(len(v["ep"]) for v in CORNER.values())
    print("   🧱 주춧돌 표 — 경험 %d · 지식 %d · 사례 %d(원고가 쥔 것 %d) · 1장 빈칸 %d"
          % (_nep, len({g for v in CORNER.values() for g in v["g"]}),
             _ncase, _case_hit, 2 - len(CORNER.get(1, {}).get("ep", []))))

_before = len(edges)
edges = _fold(edges)
print(f"   🔗 겹선 접기: {_before} → {len(edges)} (겹 {_before - len(edges)})")

if PRUNE:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    if CORNER:
        # 표가 명부다. 흐름도도 덮개도 안 돌린다 — 깎을 것이 애초에 없다.
        _keep_ep = {n["id"] for n in nodes if n["layer"] == "episode"}
        _keep_el = {n["id"] for n in nodes if n["layer"] == "element"}
    else:
        import baesun_mcmf as _b
        _S = _b.survivors()
        _keep_ep, _keep_el = set(_S["seated"]), set(_S["chosen"])
    # ⚠️ 2026-11-26 — baesun 은 **배선으로 앉힌 것**만 안다. 오늘 생긴 일화는 배선이
    #   아직 없어 자리를 못 받고, 그래서 `투향장:` 을 제 입으로 적어 두어도 깎인다
    #   (ep68 — 8장을 제 입으로 신고했는데 그래프엔 0건이었다. 제목은 여기 안 적는다:
    #   이 주석은 publish_scripts.py 가 공개면 scripts/ 로 찍어 내가고, ep68 은 공개 판정 전이다).
    #   자리 출처 서열이 self > obs > vote 이므로, **신고한 자리는 투표가 못 깎는다.**

    # 📜🪞 의 불 = 장 열. 같은 탐욕 덮개를 장 위에서 돌린다.
    _claim = {n["id"]: ({n["chap"]} if n.get("chap") else set())
              for n in nodes if n["layer"] in ("god", "symbol")}
    for e in edges:
        for a, t in ((e["s"], e["t"]), (e["t"], e["s"])):
            if a in _claim and isinstance(t, str) and t.startswith("ch") and t[2:].isdigit():
                if int(t[2:]):
                    _claim[a].add(int(t[2:]))
    _lay = {n["id"]: n["layer"] for n in nodes}
    _fires = set(range(1, 11))
    # 📜 도 **같은 자 하나**로 고른다 (2026-11-27) — 덮개를 돌리지 않고 「원고가 그 책
    #   이름을 부르나」만 본다. 종이로도 된다: 책 이름을 원고에서 찾아보면 끝이다.
    _named = {n["id"] for n in nodes if n["layer"] == "god" and n.get("named")}
    _keep_god = sorted(_named)
    _god_rem = []
    # ⚠️ 2026-11-25 — **명부에는 덮개를 안 돌린다.** 돌렸더니 🪞가 1·5·9 를 덮어
    #   🐦‍⬛까마귀가 「이미 덮였다」로 떨어졌고, 📕(열 장)을 넣자 나머지 여덟이 통째로
    #   잉여가 됐다. 덮개는 **많은 것 중 고르는 자**고 열넷은 **고를 것이 아니라 명부**다.
    #   자가 틀린 게 아니라 댄 자리가 틀렸다.
    _keep_sym = [i for i, l in _lay.items() if l == "symbol"]
    _sym_rem = []

    _keep = ({"황금새장을열다"} | {n["id"] for n in nodes if n["layer"] == "chapter"}
             | _keep_ep | _keep_el | set(_keep_god) | set(_keep_sym)
             | {n["id"] for n in nodes if n["layer"] == "case"})
    _n0, _e0 = len(nodes), len(edges)
    nodes = [n for n in nodes if n["id"] in _keep]
    edges = [e for e in edges if e["s"] in _keep and e["t"] in _keep]
    print("   ⛺️ 가차없이 깎았다 — 노드 %d → %d · 선 %d → %d"
          % (_n0, len(nodes), _e0, len(edges)))
    print("      🎞️ 일화 %d(자리) · 🍇 생각원소 %d(덮개) · 📜 신의전언 %d(장 덮개) · 🪞 상징 %d(장 덮개)"
          % (len(_keep_ep), len(_keep_el), len(_keep_god), len(_keep_sym)))
    if not CORNER and _S.get("uncovered"):
        print("      🚨 안 덮인 불 %d — 지우지 않는다: %s"
              % (len(_S["uncovered"]), " ".join(sorted(_S["uncovered"]))))
    for _nm, _rem in (("📜 신의전언", _god_rem), ("🪞 상징", _sym_rem)):
        if _rem:
            print("      🚨 %s 가 못 덮은 장 %s — 그 장엔 그 층의 재료가 없다"
                  % (_nm, sorted(_rem)))

if DROP_LEAVES:
    from collections import Counter as _C
    _deg = _C()
    for e in edges: _deg[e["s"]] += 1; _deg[e["t"]] += 1
    _leaf = {n["id"] for n in nodes
             if n["layer"] in ("god", "symbol") and _deg[n["id"]] <= 1}
    if _leaf:
        nodes = [n for n in nodes if n["id"] not in _leaf]
        edges = [e for e in edges if e["s"] not in _leaf and e["t"] not in _leaf]
        print(f"   🍂 잎 제거 — 신의전언·상징 {len(_leaf)}개 (뿌리에만 매달림)")

for n in nodes:
    n.setdefault("pole", "")
    n.setdefault("pos", "")

# ── 👁️ 자리 기재 센서스 — 화면이 쓰는 숫자와 **같은 자**로 여기서도 찍는다 ──
from collections import Counter as _PC
_pc = _PC((n["layer"], n["pos"]) for n in nodes if n["layer"] not in ("root", "chapter"))
_tot = sum(_pc.values())
_nm = {"symbol": "🪞상징", "element": "🧩생각원소", "god": "📜간접경험", "episode": "🎞️직접경험"}
print("   👁️ 자리 기재 — 적힌 "
      f"{sum(v for (l, p), v in _pc.items() if p in ('self', 'obs'))}"
      f" · 이어 그린 {sum(v for (l, p), v in _pc.items() if p == 'vote')}"
      f" · 빈칸 {sum(v for (l, p), v in _pc.items() if p == 'none')} / {_tot}")
for _l in ("symbol", "element", "god", "episode"):
    print(f"      {_nm[_l]} self {_pc[(_l,'self')]} · obs {_pc[(_l,'obs')]} "
          f"· vote {_pc[(_l,'vote')]} · none {_pc[(_l,'none')]}")

# Update GRAPH_HTML with the 3-Layer DATA
# ⚠️ vpath 는 **로컬 vault 경로**다. 공개판(golden-cage-book)에 실으면 내 디스크 구조가 공개된다.
#    obsidian:// 도 남의 기기에선 어차피 안 열린다 — 공개 출력에서는 털어낸다.
_PUBLIC = "golden-cage-book" in GRAPH_HTML
if _PUBLIC:
    for _n in nodes: _n.pop("vpath", None)
    print("   🔒 공개판 출력 — vpath 제거(로컬 경로 비공개)")

# ── 🔗 닻 — 노드마다 **원고의 어느 자리**로 가나 (2026-11-27 신설) ──────────
#    왜 — 지도는 공간 축이고 원고는 시간 축이다. 둘이 같은 것을 가리키는데 서로를
#    못 가리켰다. 「이 점이 책의 어디냐」를 사람이 눈으로 찾아야 했다.
#
#    reader.html 이 이미 `?file=…&q=…` 로 **구절을 찾아 형광까지** 한다. 그러니
#    새 기계를 안 만든다 — 노드마다 **그 장 원고에 실제로 있는 구절 하나**를 재서
#    달아 주면 끝이다. 자가 하나 더 느는 게 아니라, **이미 쓰는 자의 답을 적어 두는** 것.
#
#    ⚠️ 닻은 **재서** 단다. 못 재면 장 머리로 보내고 `q` 를 비운다 — 없는 구절을
#       달면 링크가 조용히 빗나가고, 그게 바로 묵은 표의 병이었다.
# 🚫 실명 — 목록도 **거는 자리**도 `silmyeong_gate.py` 하나가 쥔다 (룰링 2026-11-27).
#    자의 단위는 「사람」이 아니라 **「사람 × 층」**이다 — 같은 이름이 일화원소에선 빚이고
#    인용에선 갚음이다. 📜읽은 것·🧩지식만 이름을 세울 수 있고, 나머지 층은 막는다.
from silmyeong_gate import NAMES as _FORBIDDEN, scan as _silmyeong, allowed_layer as _cite_ok

_RD = {1:"ch1_mirror_cage", 2:"ch2_telescope_cage", 3:"ch3_glass_cage",
       4:"ch4_clock_cage", 5:"ch5_mirror_nest", 6:"ch6_butterfly_nest",
       7:"ch7_tulip_nest", 8:"ch8_mist_nest", 9:"ch9_raven_nest",
       10:"ch10_mirror_close"}
_RDPAGE = {c: _pages.get(_CHFILE.get(c, ""), "") for c in _RD} if "_CHFILE" in dir() else {}

def _longest_shared(src, page, lo=14, hi=70):
    """src 와 page 가 **함께 쥔 가장 긴 토막**. 없으면 None.
       n-gram 집합으로 걸러서 늘린다 — 원고가 6만 자라 전수 비교는 못 쓴다."""
    if not src or not page: return None
    grams = {page[i:i+lo] for i in range(len(page) - lo + 1)}
    best = None
    i = 0
    while i <= len(src) - lo:
        g = src[i:i+lo]
        if g in grams:
            j = lo
            while i + j < len(src) and j < hi and src[i:i+j+1] in page: j += 1
            cand = src[i:i+j]
            if best is None or len(cand) > len(best): best = cand
            i += 1
        else:
            i += 1
    return best

# ⚓ 룰링 2026-11-27 (둘째) — **닻은 노드가 아니라 선이 쥔다.**
#    까닭(실측) — 노드와 장은 1:다다. 📜『The Lever of Riches』는 4장과 9장 둘에 서고,
#    『三國遺事』는 넷에 선다. 노드에 닻을 하나 달면 **나머지가 못 닿는다** —
#    1:다 노드 아홉이 선 서른을 쥐는데 노드 클릭으로 닿는 곳은 아홉뿐이었다.
#    선 하나 = (재료, 장) 한 쌍이고, 그 쌍에는 갈 자리가 **딱 하나**다.
#    ⇒ 닻을 선마다 그 **선이 가리키는 장**에서 잰다. 같은 책도 장마다 다른 구절에 선다.

def _anchor(node, chap, pg):
    """그 노드가 **그 장** 원고에서 서는 자리. 못 찾으면 빈 글자."""
    lay = node["layer"]
    if lay in ("case", "element", "symbol"):
        cand = node.get("label", "")
        if cand and cand in pg: return cand
        if cand and lay == "element":
            tok = [w for w in re.split(r"\s+", cand)
                   if len(w) > 2 and w in pg
                   and (_cite_ok(lay) or not any(b in w for b in _FORBIDDEN))]
            if tok: return max(tok, key=len)
    elif lay == "god":
        try: f2 = parse_fm(os.path.join(GODS_DIR, node["id"] + ".md")) or {}
        except Exception: f2 = {}
        c2 = [p for p in _name_probes(f2, node["id"]) if p in pg]
        if c2: return min(c2, key=lambda p: (pg.count(p), -len(p)))
    elif lay == "episode":
        epf = None
        for f3 in os.listdir(EPISODES_DIR):
            if unicodedata.normalize("NFC", f3).startswith(node.get("ep", "\0") + "_"):
                epf = os.path.join(EPISODES_DIR, f3); break
        if epf:
            src = unicodedata.normalize("NFC", open(epf, encoding="utf-8").read())
            src = re.sub(r"^---.*?\n---\n", "", src, flags=re.S)
            src = re.sub(r"\[\[[^\]]*\]\]|[*`>#|\-]", " ", src)
            return (_longest_shared(src, pg) or "").strip(" .,·\"'\u201c\u201d\u300c\u300d")
    return ""

_byid = {n["id"]: n for n in nodes}
for _n in nodes:                      # 장 노드만 제 닻을 쥔다 (그 장 머리)
    if _n["layer"] == "chapter" and (_n.get("chap") or 0) in _RD:
        _n["rd"] = _RD[_n["chap"]]
_rd_hit = _rd_miss = 0
for _e in edges:
    _c = None; _mat = None
    for _a, _b in ((_e["s"], _e["t"]), (_e["t"], _e["s"])):
        if isinstance(_b, str) and _b.startswith("ch") and _b[2:].isdigit() and int(_b[2:]) in _RD:
            _c, _mat = int(_b[2:]), _byid.get(_a)
    if _c is None or _mat is None or _mat["layer"] in ("root", "chapter"):
        continue
    _q = _anchor(_mat, _c, _RDPAGE.get(_c, ""))
    _e["rd"] = _RD[_c] + ("|" + _q if _q else "")
    _rd_hit += bool(_q); _rd_miss += (not _q)
print("   🔗 닻(선마다) — 구절까지 %d · 장 머리까지만 %d / 재료→장 선 %d"
      % (_rd_hit, _rd_miss, _rd_hit + _rd_miss))

# 🚫 실명 문지기 — 공개 저장소에 쓰기 전에 **낼 것 전부**를 층으로 가려 훑는다.
#    인용 층(📜읽은 것·🧩지식)은 이름이 서야 빚이 0이라 통과시키고 적어만 둔다.
#    나머지 층에 이름이 서면 **안 내고 멈춘다** — 거기 선 이름은 동의받은 적이 없다.
_block, _cited = [], []
for _n2 in nodes:
    _hit2 = _silmyeong(json.dumps(_n2, ensure_ascii=False))
    if not _hit2: continue
    (_cited if _cite_ok(_n2["layer"]) else _block).append((_n2, _hit2))
if _cited:
    print("   📎 인용 층에 선 이름 %d — 통과시킨다(인용은 이름이 있어야 빚이 0)" % len(_cited))
    for _n2, _h in _cited:
        print("      · %-12s %s" % (",".join(_h), _n2.get("label", _n2["id"])[:34]))
if _block:
    print("   🚨 실명 문지기 — **안 내고 멈춘다.** 인용 아닌 층에 이름이 섰다:", file=sys.stderr)
    for _n2, _h in _block:
        print("      · %-12s %-10s %s" % (",".join(_h), _n2["layer"],
                                          _n2.get("label", _n2["id"])[:34]), file=sys.stderr)
    sys.exit(1)

# ── 📏 원고가 이 이름을 부르나 (2026-11-23 신설) ────────────────────────────
#    이 그래프의 덮개는 **frontmatter 의 `chapter`** 로 장을 덮는다. 그래서 한 노드가
#    「3·5·7장」이라 적어 두기만 하면, 원고가 그 이름을 **한 번도 안 불러도** 살아남는다.
#
#    ⚠️ 이 자가 답하는 것은 **이름을 부르나** 하나뿐이다. 「쓸모가 있나」가 아니다.
#       생각원소(g…)는 원고가 이름이 아니라 **산문으로** 나르므로 이 자에 안 건다 —
#       걸면 전부 0 이 나오고, 0 은 발견이 아니라 자가 틀린 신호다(#117).
#       📜 간접경험만 잰다. 책은 이름으로 불리는 것이 정상이기 때문이다.
#
#    실측 11-23 — 📜 넷 중 둘이 이름 0 이다.
#       caillois 『Les Jeux et les Hommes』 : 카유아·카이와·Caillois·놀이와 인간 전부 0
#       hyde 『Trickster Makes This World』 : 하이드·Hyde·Trickster 0 — 다만 「트릭스터」는 4회.
#       그래서 꼬리표를 「안 쓴다」가 아니라 **「이름 안 부름」**으로 적는다. 생각은 설 수 있다.
#    🌗 지우지 않고 찍는다. 내릴지 이름을 적을지는 룰링이다.


# 📏 「글자째 인용」 자는 뗐다 (2026-11-27) — 표가 이미 **원고에 든 것만** 담으므로
#    같은 것을 두 번 재는 일이 된다. 자 하나 원칙.

# ── 인물 띠 넷 (2026-11-25 · /reader 8:0) ──────────────────────────────────
#   인물은 **점이 아니라 구간**이다. 다·세·세다는 한 장에 사는 게 아니라 몇 장에
#   걸쳐 있다가 교대한다 — 점으로 찍으면 그 교대가 안 보이고 띠로 그으면 그게 전부다.
#   노드로 세우면 장 줄을 가로지르는 선이 10 → 26 이 되어 거미줄이 된다(/reader 실측).
#   ⚠️ 자를 두 벌 만들지 않는다 — 감정은 `scripts/09_rotor_stator.py` 가 지고
#   여기서는 그 **장부를 읽기만** 한다. 장부가 없으면 lead 를 비운다(0 이 아니라 빈칸).
_CHDIR = os.path.join(TOLZUL_DIR, "4차소통/원고")
_CHF = {1:"1🪞_거울새장",2:"2🔭_망원경새장",3:"3💒_스테인굴레스새장",4:"4⏱️_시계새장",
        5:"5🐀_101",6:"6🦋_나비사용자",7:"7🌷_튤립기술자",8:"8🌫️_안개투자자",
        9:"9🐦‍⬛_까마귀협력자",10:"10🧫_101"}
_SPK = re.compile(r'^\*\*(다|세|세다):\*\*', re.M)
_say = {c: {"다":0,"세":0,"세다":0} for c in _CHF}
_book = {}
for _c, _f in _CHF.items():
    _fp = os.path.join(_CHDIR, _f + ".md")
    if not os.path.exists(_fp): continue
    _t = open(_fp, encoding="utf-8").read()
    for _m in _SPK.finditer(_t): _say[_c][_m.group(1)] += 1
    _book[_c] = _t.count("📕") > 0 or ("일기장" in _t)

# 장부에서 장별 1위 화자를 읽는다 (없으면 빈칸)
_lead = {}
_ledger = os.path.join(os.path.dirname(GRAPH_HTML), "..", "scripts", "09_rotor_stator_장부.tsv")
if os.path.exists(_ledger):
    for _ln in open(_ledger, encoding="utf-8"):
        _p = _ln.rstrip("\n").split("\t")
        if len(_p) >= 3 and _p[0] == "1위" and _p[2] in ("다","세","세다"):
            _lead[int(_p[1])] = _p[2]

_PCOL = {"다":"#F08A3C", "세":"#C9B99A", "세다":"#E07AC8"}   # 09_rotor_stator 와 같은 색
bands = []
for _who in ("세", "다", "세다"):
    _ch = sorted(c for c in _CHF if _say[c][_who] > 0)
    bands.append({"id": _who, "label": _who, "color": _PCOL[_who], "chaps": _ch,
                  "say": {str(c): _say[c][_who] for c in _ch},
                  "lead": sorted(c for c, w in _lead.items() if w == _who)})
bands.append({"id": "📕", "label": "붉은 일기장", "color": "#B4443A",
              "chaps": sorted(c for c in _CHF if _book.get(c)),
              "say": {}, "lead": [],
              "mark": [5, 10],      # 대사가 아니라 물건으로 서는 두 장 = 주탑
              # 📕 은 **넷째 인물이 아니라 셋을 꿰는 실**이다 (룰링 2026-11-26).
              #   세가 쓰고(1~4) → 다가 품고 나가고(5) → 세다의 몸이 되고(6~9) → 10 에서 갈린다.
              #   세·다·세다 옆에 나란한 레인으로 깔면 「넷째 입」으로 읽힌다. 실은 층을 **건너간다**.
              #   그래서 띠가 아니라 레인을 옮겨 다니는 한 줄로 그린다(그리기는 reference_graph.html).
              "thread": {**{c: "세" for c in (1, 2, 3, 4)}, 5: "다",
                         **{c: "세다" for c in (6, 7, 8, 9)}, 10: "찢"},
              # 「제본선」은 열다섯째 상징이 아니라 📕 의 **마지막 몸**이다 (gcb #81 열넷 유지).
              #   종이(1~4) → 품은 것(5) → 살(6~9) → 갈린 제본선(10). 그 낱말이 띠에 없어
              #   공개면에서 찾는 사람이 「아직 안 들어갔다」고 읽었다 (2026-11-26).
              "note": "5·10 은 물건으로 선다 — 실로 묶인 채 품고 나가고, 거기서 제본선이 갈린다"})
SILENT = {"5": "대사 없음 — 이 장의 감정은 임자가 안 적힌 1인칭 문장에 있다",
          "10": "대사 없음 — 이 장의 감정은 임자가 안 적힌 1인칭 문장에 있다"}
print("   🎭 인물 띠 — " + " · ".join(
    f"{b['label']} {len(b['chaps'])}장" + (f"(1위 {len(b['lead'])})" if b['lead'] else "")
    for b in bands))

data_json = json.dumps({"nodes": nodes, "edges": edges, "bands": bands, "silent": SILENT, "center": "황금새장을열다",
                        "asof": datetime.date.today().isoformat()}, ensure_ascii=False)

if os.path.exists(GRAPH_HTML):
    html_txt = open(GRAPH_HTML, encoding="utf-8").read()
    # Replace const DATA = {...};
    new_html = re.sub(r'const DATA = \{.*?\};', f'const DATA = {data_json};', html_txt, flags=re.DOTALL)
    
    # Also update role colors in GRAPH_HTML
    role_json = 'const ROLE = {0:"#efe3c0", 1:"#b5a3f8", 2:"#7cb0db", 3:"#c5a55a"};'
    new_html = re.sub(r'const ROLE = \{.*?\};', role_json, new_html)
    
    with open(GRAPH_HTML, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"✅ Successfully updated {GRAPH_HTML} with {len(nodes)} nodes and {len(edges)} edges!")
    if MIN_USAGE > 0:
        print(f"   ✂️ 최소복잡도 MIN_USAGE={MIN_USAGE} — 생각원소 {len(_cut)}개 잘림 "
              f"(100%={sum(1 for _,u in _cut if u==100)} · 50%={sum(1 for _,u in _cut if u==50)} · 0%={sum(1 for _,u in _cut if u==0)})")
