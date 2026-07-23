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

# 장 번호 → reader.html 파일명 (SSOT: bookmap_3d.html SL 규약과 동일). 점 클릭 → 그 장으로.
CHAP_FILE = {
    "1": "ch1_mirror_cage", "2": "ch2_telescope_cage", "3": "ch3_glass_cage",
    "4": "ch4_clock_cage", "5": "ch5_mirror_nest", "6": "ch6_butterfly_nest",
    "7": "ch7_tulip_nest", "8": "ch8_mist_nest", "9": "ch9_raven_nest",
    "10": "ch10_epilogue",
}


# ── 계보(은하수) 데이터: reference_graph.html 흡수 (SSOT: 여기 하나) ──
GENEALOGY_JSON = r'''{"nodes":[{"id":"황금새장을열다","label":"🪞 황금새장을 열다","depth":0,"marr_layer":0,"layer":"root","r":18,"sector":3},{"id":"🐦‍⬛","label":"🐦‍⬛","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":3},{"id":"🪞","label":"🪞","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":3},{"id":"⏱️","label":"⏱️","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":2},{"id":"🌫️","label":"🌫️","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":2},{"id":"🔫","label":"🔫","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":3},{"id":"🌷","label":"🌷","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":1},{"id":"🔭","label":"🔭","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":1},{"id":"👾","label":"👾","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":0},{"id":"📝","label":"📝","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":3},{"id":"🧫","label":"🧫","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":3},{"id":"💒","label":"💒","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":1},{"id":"🫀","label":"🫀","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":3},{"id":"🦋","label":"🦋","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":0},{"id":"claude_emotions","label":"claude_emotions","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":1},{"id":"🚪","label":"🚪","depth":1,"marr_layer":1,"layer":"symbol","r":12,"sector":2},{"id":"📜camus_페스트","label":"📜 La Peste","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜quine_elementary_logic","label":"📜 Elementary Logic","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜rovelli_시간의질서","label":"📜 L'ordine del tempo","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜orwell_why_i_write","label":"📜 Why I Write","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":1},{"id":"📜austin_how_to_do_things","label":"📜 How to Do Things with Words","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜ricoeur_soi_meme_comme_un_autre","label":"📜 Soi-même comme un autre","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜노자_도덕경","label":"📜 道德經 11장","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜clausewitz_vom_kriege","label":"📜 Vom Kriege","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜girard_낭만적거짓과소설적진실","label":"📜 Mensonge romantique et vérité romanesque","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜dumas_검은튤립","label":"📜 La Tulipe noire","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":1},{"id":"📜kratzer_modality","label":"📜 The Notional Category of Modality","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜unamuno_안개","label":"📜 Niebla","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜polanyi_tacit_dimension","label":"📜 The Tacit Dimension","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜gould_lewontin_spandrels","label":"📜 The Spandrels of San Marco and the Panglossian Paradigm","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜douglass_narrative","label":"📜 Narrative of the Life of Frederick Douglass, an American Slave","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜keats_negative_capability","label":"📜 Letter to George and Tom Keats (Dec. 21, 1817)","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜homeric_hymn_hermes","label":"📜 Ὁμηρικοὶ Ὕμνοι · 헤르메스에게","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜greenwald_totalitarian_ego","label":"📜 The Totalitarian Ego — Fabrication and Revision of Personal History","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":1},{"id":"📜bourdieu_la_distinction","label":"📜 La Distinction · Le Sens pratique","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜orwell_1984","label":"📜 Nineteen Eighty-Four","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜duckworth_grit","label":"📜 Grit: The Power of Passion and Perseverance","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜flaubert_마담보바리","label":"📜 Madame Bovary","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜carlson_reference_to_kinds","label":"📜 Reference to Kinds in English (PhD dissertation)","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜sapir_status_of_linguistics","label":"📜 The Status of Linguistics as a Science","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜klein_뇌는어떻게변화를거부하는가","label":"📜 Wie wir die Welt verändern","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜goffman_presentation_of_self","label":"📜 The Presentation of Self in Everyday Life","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":1},{"id":"📜thiel_zero_to_one","label":"📜 Zero to One","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜caillois_les_jeux_et_les_hommes","label":"📜 Les Jeux et les Hommes","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜defoe_robinson_crusoe","label":"📜 Robinson Crusoe","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜kahneman_tversky_prospect_theory","label":"📜 Prospect Theory: An Analysis of Decision under Risk","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":1},{"id":"📜maples_pattern_breakers","label":"📜 Pattern Breakers","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜hwang_m_butterfly","label":"📜 M. Butterfly","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜ovid_변신이야기","label":"📜 Metamorphoses","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜tournier_vendredi","label":"📜 Vendredi ou les limbes du Pacifique","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜weber_직업으로서의정치","label":"📜 Politik als Beruf · Wissenschaft als Beruf","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":1},{"id":"📜mokyr_lever_of_riches","label":"📜 The Lever of Riches · A Culture of Growth","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜hyde_trickster_makes_this_world","label":"📜 Trickster Makes This World","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜gibbons_coase_to_culture","label":"📜 From Coase to Culture? Visible Hands Build Equilibria","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜orwell_animal_farm","label":"📜 Animal Farm","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜brinkerink_nc_pc","label":"📜 Negative and Positive Capability in Founder Behaviour","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜일연_삼국유사","label":"📜 三國遺事","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"📜aurelius_명상록","label":"📜 τὰ εἰς ἑαυτόν (Meditations)","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":2},{"id":"📜grice_logic_and_conversation","label":"📜 Logic and Conversation (in Syntax and Semantics 3)","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":1},{"id":"📜lampedusa_표범","label":"📜 Il Gattopardo","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜whorf_language_thought_reality","label":"📜 Language, Thought, and Reality","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":0},{"id":"📜harari_nexus","label":"📜 Nexus","depth":3,"marr_layer":3,"layer":"god","r":10,"sector":3},{"id":"g3_27_Keats_Negative_Capabilit","label":"g3_27_Keats_Negative_Capabilit","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_18_Bezos_Day_1","label":"g3_18_Bezos_Day_1","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g4_09_101호_101₂_101₃","label":"g4_09_101호_101₂_101₃","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_34_Orwell_1984_3_슬로건_double","label":"g3_34_Orwell_1984_3_슬로건_double","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_03_스테인굴레스","label":"g4_03_스테인굴레스","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g1_12_f_f_Fenchel_biconjugate","label":"g1_12_f_f_Fenchel_biconjugate","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_11_둥지4축_멈춤_모방_넘김_매혹","label":"g2_11_둥지4축_멈춤_모방_넘김_매혹","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_11_革新_革身","label":"g6_11_革新_革身","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g6_13_가작_假作_佳作","label":"g6_13_가작_假作_佳作","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_37_Shannon_source_coding","label":"g3_37_Shannon_source_coding","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g6_08_회전축_5_10","label":"g6_08_회전축_5_10","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g1_07_Cromwell_prior_0_1","label":"g1_07_Cromwell_prior_0_1","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_28_노자_當其無","label":"g3_28_노자_當其無","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g4_07_안개","label":"g4_07_안개","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_35_中庸_中和_희로애락_4계절","label":"g3_35_中庸_中和_희로애락_4계절","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_15_Habitus","label":"g2_15_Habitus","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g5_21_narrative_prior_4동사_공유_극","label":"g5_21_narrative_prior_4동사_공유_극","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g2_14_삼각형_모방욕망_나_중재자_대상","label":"g2_14_삼각형_모방욕망_나_중재자_대상","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g3_08_Kennedy_O_Hagan_model_di","label":"g3_08_Kennedy_O_Hagan_model_di","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_24_Appiah_Honor_Code","label":"g3_24_Appiah_Honor_Code","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g4_24_GitHub_frame공개_vs_비공개_ML","label":"g4_24_GitHub_frame공개_vs_비공개_ML","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_20_action_prior_vs_full_pri","label":"g6_20_action_prior_vs_full_pri","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_13_Caillois_4_놀이_AGON_ALEA_","label":"g3_13_Caillois_4_놀이_AGON_ALEA_","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_18_장부","label":"g4_18_장부","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g6_06_op_st_ambiguity","label":"g6_06_op_st_ambiguity","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_06_Camus_부조리_반항","label":"g3_06_Camus_부조리_반항","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_20_Wasserman_rich_vs_king","label":"g3_20_Wasserman_rich_vs_king","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g4_06_튤립구근_세_알","label":"g4_06_튤립구근_세_알","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g3_14_Bill_Aulet_24단계_beachhea","label":"g3_14_Bill_Aulet_24단계_beachhea","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_10_우로보로스","label":"g4_10_우로보로스","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_19_疑_義_비틂","label":"g5_19_疑_義_비틂","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g6_04_磁場_자장","label":"g6_04_磁場_자장","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_11_재명명_rename","label":"g5_11_재명명_rename","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_21_vanity_mirror_분장실","label":"g4_21_vanity_mirror_분장실","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g1_09_δ_사랑의_지지집합","label":"g1_09_δ_사랑의_지지집합","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_29_Cromwell_s_rule","label":"g3_29_Cromwell_s_rule","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_19_Ricœur_idem_ipse","label":"g3_19_Ricœur_idem_ipse","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g1_02_Debt_U_desire_φ_belief","label":"g1_02_Debt_U_desire_φ_belief","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g2_08_사면체_3단_깎기_수축_공명","label":"g2_08_사면체_3단_깎기_수축_공명","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_21_calibration_식민화","label":"g6_21_calibration_식민화","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_08_까마귀_빛","label":"g4_08_까마귀_빛","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_01_Girard_모방욕망","label":"g3_01_Girard_모방욕망","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g2_01_4렌즈","label":"g2_01_4렌즈","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_33_de_Finetti_coherence_Ram","label":"g3_33_de_Finetti_coherence_Ram","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_13_evaluate_재는_손","label":"g5_13_evaluate_재는_손","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g5_15_capitalize_작가_자리_협상","label":"g5_15_capitalize_작가_자리_협상","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g1_13_Selection_Variation","label":"g1_13_Selection_Variation","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g1_11_Strong_duality_gap_0_KKT","label":"g1_11_Strong_duality_gap_0_KKT","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_15_Jan_de_Witt_1671_actuari","label":"g3_15_Jan_de_Witt_1671_actuari","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_10_새장4축_도취_고집_부끄러움_연민","label":"g2_10_새장4축_도취_고집_부끄러움_연민","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g3_05_Weber_신념_책임윤리","label":"g3_05_Weber_신념_책임윤리","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_01_거울","label":"g4_01_거울","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g4_15_개_그레이하운드_벤디코_텐","label":"g4_15_개_그레이하운드_벤디코_텐","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g2_26_Nail_V_4i_Scale_V_4i","label":"g2_26_Nail_V_4i_Scale_V_4i","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g5_07_순서를_타다","label":"g5_07_순서를_타다","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_16_신념_책임윤리_위계분포_99_1","label":"g2_16_신념_책임윤리_위계분포_99_1","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g6_10_제3의_길","label":"g6_10_제3의_길","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g6_17_wit_wisdom","label":"g6_17_wit_wisdom","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_11_Greenwald_전체주의적_자아_1980","label":"g3_11_Greenwald_전체주의적_자아_1980","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g5_16_역설계_투자자_미래_풀기","label":"g5_16_역설계_투자자_미래_풀기","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_18_아우라","label":"g6_18_아우라","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g6_19_cache_warm_up","label":"g6_19_cache_warm_up","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_04_음화로_완성","label":"g5_04_음화로_완성","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"📚코끼리스텔라우주비행사가되다","label":"📚코끼리스텔라우주비행사가되다","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_25_이중나선_깎기1_5_짓기6_9","label":"g2_25_이중나선_깎기1_5_짓기6_9","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_07_사면체_cage4_nest4_회전축","label":"g2_07_사면체_cage4_nest4_회전축","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_36_Benjamin_아우라","label":"g3_36_Benjamin_아우라","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_09_8단계_새장4_둥지4","label":"g2_09_8단계_새장4_둥지4","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_22_Crucial_Third_Position","label":"g2_22_Crucial_Third_Position","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g1_14_R_1","label":"g1_14_R_1","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g1_05_μ_1_μ_ε_B","label":"g1_05_μ_1_μ_ε_B","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g5_06_장부를_펴다","label":"g5_06_장부를_펴다","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g2_29_명주실_양탄자_둥지_1D_2D_3D","label":"g2_29_명주실_양탄자_둥지_1D_2D_3D","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g1_10_파동_에너지_보존_A_B_Σ_100","label":"g1_10_파동_에너지_보존_A_B_Σ_100","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_18_부조리_구조_의미요구_침묵","label":"g2_18_부조리_구조_의미요구_침묵","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g6_03_낭만_위안","label":"g6_03_낭만_위안","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_09_분포로_적기_확률적_사고","label":"g5_09_분포로_적기_확률적_사고","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g5_22_simulation_belief","label":"g5_22_simulation_belief","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_07_Luther_Hier_stehe_ich","label":"g3_07_Luther_Hier_stehe_ich","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g6_02_새장_황금새장_둥지","label":"g6_02_새장_황금새장_둥지","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_22_창살_vs_거울","label":"g4_22_창살_vs_거울","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g2_28_건축_cage_텍스타일_nest","label":"g2_28_건축_cage_텍스타일_nest","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g2_03_ISRV","label":"g2_03_ISRV","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_30_Moon_OIL_2025","label":"g3_30_Moon_OIL_2025","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g1_06_Fubini_E_s_E_U_E_U_E_s","label":"g1_06_Fubini_E_s_E_U_E_U_E_s","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_32_클라인_뇌는_변화를_거부_착각_7","label":"g3_32_클라인_뇌는_변화를_거부_착각_7","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g2_19_segment_replicate_platfo","label":"g2_19_segment_replicate_platfo","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_25_일연_三國遺事_正_遺","label":"g3_25_일연_三國遺事_正_遺","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_02_멈춤_NC","label":"g5_02_멈춤_NC","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_02_3왕국_Prior_Likelihood_Pos","label":"g2_02_3왕국_Prior_Likelihood_Pos","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g2_12_양탄자_4모서리_thesis_수렴","label":"g2_12_양탄자_4모서리_thesis_수렴","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g1_01_dG_dF_dG_dR_dR_dF","label":"g1_01_dG_dF_dG_dR_dR_dF","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_21_novela_nivola","label":"g2_21_novela_nivola","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g4_12_다이나모_자가발전","label":"g4_12_다이나모_자가발전","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g5_20_frame_공개","label":"g5_20_frame_공개","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_13_4_산업_atomic_bit_atom_cel","label":"g2_13_4_산업_atomic_bit_atom_cel","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_23_Coase_firm_vs_market_Gib","label":"g3_23_Coase_firm_vs_market_Gib","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g4_17_섬","label":"g4_17_섬","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g2_23_Phase_2_Re_enchantment","label":"g2_23_Phase_2_Re_enchantment","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g5_03_계산끝낸물_calibrate","label":"g5_03_계산끝낸물_calibrate","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_20_분포_vs_한_점","label":"g2_20_분포_vs_한_점","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_20_파도_수면","label":"g4_20_파도_수면","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g5_14_제도화_institutionalize","label":"g5_14_제도화_institutionalize","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_10_Gould_Lewontin_spandrel","label":"g3_10_Gould_Lewontin_spandrel","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_14_기세","label":"g6_14_기세","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_10_비틂_torsion_torque","label":"g5_10_비틂_torsion_torque","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g4_05_나비_옷_살","label":"g4_05_나비_옷_살","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_17_인공선택_vs_자연선택","label":"g2_17_인공선택_vs_자연선택","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_22_Hyde_Trickster_Land_in_B","label":"g3_22_Hyde_Trickster_Land_in_B","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_14_황금새장_둥지","label":"g4_14_황금새장_둥지","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_31_Nemirovski_Yudin_Mirror_","label":"g3_31_Nemirovski_Yudin_Mirror_","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g6_12_낭만보균자","label":"g6_12_낭만보균자","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_04_Clausewitz_Schwung_기세","label":"g3_04_Clausewitz_Schwung_기세","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_02_망원경","label":"g4_02_망원경","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_09_Mokyr_인공선택","label":"g3_09_Mokyr_인공선택","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g5_12_segment_replicate_platfo","label":"g5_12_segment_replicate_platfo","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_30_거울_5쌍_1_5_2_8_3_7_4_9_5_","label":"g2_30_거울_5쌍_1_5_2_8_3_7_4_9_5_","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_21_Ash_Patel_이사회_상사_고르기","label":"g3_21_Ash_Patel_이사회_상사_고르기","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g4_19_주사기","label":"g4_19_주사기","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_16_별_빛_샹들리에_천문대_촛불_태양","label":"g4_16_별_빛_샹들리에_천문대_촛불_태양","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_17_Dumas_분포_생존","label":"g3_17_Dumas_분포_생존","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g6_09_義味","label":"g6_09_義味","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g6_01_빚_틀린_모델","label":"g6_01_빚_틀린_모델","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g1_03_τ_max_0_V_4i_1","label":"g1_03_τ_max_0_V_4i_1","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g4_25_의심혈청","label":"g4_25_의심혈청","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_05_NOCS_Diamond","label":"g2_05_NOCS_Diamond","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g4_13_윙크_한_눈만_찌름","label":"g4_13_윙크_한_눈만_찌름","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_26_Douglass_Bailey_Douglass","label":"g3_26_Douglass_Bailey_Douglass","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g3_02_Goffman_연출_role_distance","label":"g3_02_Goffman_연출_role_distance","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_23_Mirrorback_dual_update","label":"g5_23_Mirrorback_dual_update","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g2_04_3S_Scope_Sequence_Sync","label":"g2_04_3S_Scope_Sequence_Sync","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g4_11_명주실_양탄자_둥지","label":"g4_11_명주실_양탄자_둥지","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_07_다_多_세_世","label":"g6_07_다_多_세_世","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_01_한_글자_비틂","label":"g5_01_한_글자_비틂","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_23_사랑_꿈꾸고자_이해시도","label":"g6_23_사랑_꿈꾸고자_이해시도","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_04_시계","label":"g4_04_시계","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g2_06_isrVRSI_계산끝낸물","label":"g2_06_isrVRSI_계산끝낸물","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g5_05_과거_고통을_미래_연료로","label":"g5_05_과거_고통을_미래_연료로","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_16_보균자","label":"g6_16_보균자","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_24_환상_윤리_3조건","label":"g2_24_환상_윤리_3조건","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g5_24_트림_clarity_deletion","label":"g5_24_트림_clarity_deletion","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g1_04_V_4i","label":"g1_04_V_4i","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g3_12_Foucault_헤테로토피아_heteroch","label":"g3_12_Foucault_헤테로토피아_heteroch","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g2_27_NC_PC_Brinkerink","label":"g2_27_NC_PC_Brinkerink","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":3},{"id":"g3_03_Bourdieu_Habitus","label":"g3_03_Bourdieu_Habitus","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_22_4_atomic_unit_bit_atom_c","label":"g6_22_4_atomic_unit_bit_atom_c","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g3_16_Tali_Sharot_The_Influent","label":"g3_16_Tali_Sharot_The_Influent","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g5_18_함께_명명하기","label":"g5_18_함께_명명하기","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g5_08_교정_calibration","label":"g5_08_교정_calibration","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g5_17_옆에_두기_juxtaposition","label":"g5_17_옆에_두기_juxtaposition","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":2},{"id":"g6_05_소통밀도","label":"g6_05_소통밀도","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g1_08_posterior_likelihood_pri","label":"g1_08_posterior_likelihood_pri","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1},{"id":"g6_15_함께_마심","label":"g6_15_함께_마심","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":0},{"id":"g4_23_Rosa의_손바닥","label":"g4_23_Rosa의_손바닥","depth":2,"marr_layer":2,"layer":"element","r":6,"sector":1}],"edges":[{"s":"황금새장을열다","t":"🐦‍⬛"},{"s":"황금새장을열다","t":"🪞"},{"s":"황금새장을열다","t":"⏱️"},{"s":"황금새장을열다","t":"🌫️"},{"s":"황금새장을열다","t":"🔫"},{"s":"황금새장을열다","t":"🌷"},{"s":"황금새장을열다","t":"🔭"},{"s":"황금새장을열다","t":"👾"},{"s":"황금새장을열다","t":"📝"},{"s":"황금새장을열다","t":"🧫"},{"s":"황금새장을열다","t":"💒"},{"s":"황금새장을열다","t":"🫀"},{"s":"황금새장을열다","t":"🦋"},{"s":"황금새장을열다","t":"claude_emotions"},{"s":"황금새장을열다","t":"🚪"},{"s":"황금새장을열다","t":"📜camus_페스트"},{"s":"황금새장을열다","t":"📜quine_elementary_logic"},{"s":"황금새장을열다","t":"📜rovelli_시간의질서"},{"s":"황금새장을열다","t":"📜orwell_why_i_write"},{"s":"황금새장을열다","t":"📜austin_how_to_do_things"},{"s":"황금새장을열다","t":"📜ricoeur_soi_meme_comme_un_autre"},{"s":"황금새장을열다","t":"📜노자_도덕경"},{"s":"황금새장을열다","t":"📜clausewitz_vom_kriege"},{"s":"황금새장을열다","t":"📜girard_낭만적거짓과소설적진실"},{"s":"황금새장을열다","t":"📜dumas_검은튤립"},{"s":"황금새장을열다","t":"📜kratzer_modality"},{"s":"황금새장을열다","t":"📜unamuno_안개"},{"s":"황금새장을열다","t":"📜polanyi_tacit_dimension"},{"s":"황금새장을열다","t":"📜gould_lewontin_spandrels"},{"s":"황금새장을열다","t":"📜douglass_narrative"},{"s":"황금새장을열다","t":"📜keats_negative_capability"},{"s":"황금새장을열다","t":"📜homeric_hymn_hermes"},{"s":"황금새장을열다","t":"📜greenwald_totalitarian_ego"},{"s":"황금새장을열다","t":"📜bourdieu_la_distinction"},{"s":"황금새장을열다","t":"📜orwell_1984"},{"s":"황금새장을열다","t":"📜duckworth_grit"},{"s":"황금새장을열다","t":"📜flaubert_마담보바리"},{"s":"황금새장을열다","t":"📜carlson_reference_to_kinds"},{"s":"황금새장을열다","t":"📜sapir_status_of_linguistics"},{"s":"황금새장을열다","t":"📜klein_뇌는어떻게변화를거부하는가"},{"s":"황금새장을열다","t":"📜goffman_presentation_of_self"},{"s":"황금새장을열다","t":"📜thiel_zero_to_one"},{"s":"황금새장을열다","t":"📜caillois_les_jeux_et_les_hommes"},{"s":"황금새장을열다","t":"📜defoe_robinson_crusoe"},{"s":"황금새장을열다","t":"📜kahneman_tversky_prospect_theory"},{"s":"황금새장을열다","t":"📜maples_pattern_breakers"},{"s":"황금새장을열다","t":"📜hwang_m_butterfly"},{"s":"황금새장을열다","t":"📜ovid_변신이야기"},{"s":"황금새장을열다","t":"📜tournier_vendredi"},{"s":"황금새장을열다","t":"📜weber_직업으로서의정치"},{"s":"황금새장을열다","t":"📜mokyr_lever_of_riches"},{"s":"황금새장을열다","t":"📜hyde_trickster_makes_this_world"},{"s":"황금새장을열다","t":"📜gibbons_coase_to_culture"},{"s":"황금새장을열다","t":"📜orwell_animal_farm"},{"s":"황금새장을열다","t":"📜brinkerink_nc_pc"},{"s":"황금새장을열다","t":"📜일연_삼국유사"},{"s":"황금새장을열다","t":"📜aurelius_명상록"},{"s":"황금새장을열다","t":"📜grice_logic_and_conversation"},{"s":"황금새장을열다","t":"📜lampedusa_표범"},{"s":"황금새장을열다","t":"📜whorf_language_thought_reality"},{"s":"황금새장을열다","t":"📜harari_nexus"},{"s":"g3_37_Shannon_source_coding","t":"황금새장을열다"},{"s":"g3_35_中庸_中和_희로애락_4계절","t":"황금새장을열다"},{"s":"g5_21_narrative_prior_4동사_공유_극","t":"황금새장을열다"},{"s":"g3_08_Kennedy_O_Hagan_model_di","t":"황금새장을열다"},{"s":"g6_20_action_prior_vs_full_pri","t":"황금새장을열다"},{"s":"g6_06_op_st_ambiguity","t":"황금새장을열다"},{"s":"g6_04_磁場_자장","t":"황금새장을열다"},{"s":"g6_21_calibration_식민화","t":"황금새장을열다"},{"s":"g2_01_4렌즈","t":"황금새장을열다"},{"s":"g3_33_de_Finetti_coherence_Ram","t":"황금새장을열다"},{"s":"g6_17_wit_wisdom","t":"황금새장을열다"},{"s":"g6_18_아우라","t":"황금새장을열다"},{"s":"g6_19_cache_warm_up","t":"황금새장을열다"},{"s":"g3_36_Benjamin_아우라","t":"황금새장을열다"},{"s":"g1_14_R_1","t":"황금새장을열다"},{"s":"g2_29_명주실_양탄자_둥지_1D_2D_3D","t":"황금새장을열다"},{"s":"g5_22_simulation_belief","t":"황금새장을열다"},{"s":"g2_28_건축_cage_텍스타일_nest","t":"황금새장을열다"},{"s":"g2_03_ISRV","t":"황금새장을열다"},{"s":"g5_02_멈춤_NC","t":"황금새장을열다"},{"s":"g2_02_3왕국_Prior_Likelihood_Pos","t":"황금새장을열다"},{"s":"g2_13_4_산업_atomic_bit_atom_cel","t":"황금새장을열다"},{"s":"g3_10_Gould_Lewontin_spandrel","t":"황금새장을열다"},{"s":"g2_05_NOCS_Diamond","t":"황금새장을열다"},{"s":"g2_04_3S_Scope_Sequence_Sync","t":"황금새장을열다"},{"s":"g2_06_isrVRSI_계산끝낸물","t":"황금새장을열다"},{"s":"g5_24_트림_clarity_deletion","t":"황금새장을열다"},{"s":"g2_27_NC_PC_Brinkerink","t":"황금새장을열다"},{"s":"g6_22_4_atomic_unit_bit_atom_c","t":"황금새장을열다"},{"s":"g6_05_소통밀도","t":"황금새장을열다"}],"center":"황금새장을열다"}'''

# ── 입체 렌즈 장별 슬로건/소설/거울쌍: bookmap_3d.html 흡수 ──
CHAP_META = {
    "1": {"slogan": "장부를 펴라", "novel": "마담 보바리 (플로베르)", "mirror": 6},
    "2": {"slogan": "순서를 타라", "novel": "표범 (람페두사)", "mirror": 7},
    "3": {"slogan": "확신을 교정하라", "novel": "페스트 (카뮈)", "mirror": 8},
    "4": {"slogan": "다음 불을 피워라", "novel": "방드르디 (투르니에)", "mirror": 9},
    "6": {"slogan": "환상을 역이용하라", "novel": "M.Butterfly (황)", "mirror": 1},
    "7": {"slogan": "확률적으로 생각하라", "novel": "검은 튤립 (뒤마)", "mirror": 2},
    "8": {"slogan": "선을 넘어라", "novel": "안개 Niebla (우나무노)", "mirror": 3},
    "9": {"slogan": "의미를 만들어라", "novel": "삼국유사 (일연)", "mirror": 4},
}


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
        "chapFile": CHAP_FILE,
    }
    payload = json.dumps(data, ensure_ascii=False)

    html = TEMPLATE.replace("/*__DATA__*/", payload)
    html = html.replace("/*__GENEALOGY__*/", GENEALOGY_JSON)
    html = html.replace("/*__CHAPMETA__*/", json.dumps(CHAP_META, ensure_ascii=False))
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

  #polyhint{position:absolute;left:50%;bottom:44px;transform:translateX(-50%);z-index:7;
    display:none;font-size:11.5px;color:var(--dim);background:rgba(15,13,11,.72);
    border:1px solid var(--line);border-radius:16px;padding:6px 15px;max-width:80vw;
    text-align:center;pointer-events:none;}
  #polyhint b{color:var(--gold);font-weight:500;}
  body.poly #polyhint{display:block;}

  #genehint{position:absolute;left:50%;bottom:44px;transform:translateX(-50%);z-index:7;
    display:none;font-size:11.5px;color:var(--dim);background:rgba(15,13,11,.72);
    border:1px solid var(--line);border-radius:16px;padding:6px 15px;max-width:80vw;
    text-align:center;pointer-events:none;}
  #genehint b{color:var(--gold);font-weight:500;}
  body.gene #genehint{display:block;}

  /* 입체 렌즈 장 슬로건 카드 (bookmap_3d 흡수) */
  #polycard{position:absolute;top:64px;right:22px;z-index:8;width:250px;display:none;
    background:rgba(16,13,11,.94);border:1px solid var(--line);border-radius:10px;
    padding:14px;box-shadow:0 8px 24px rgba(0,0,0,.5);pointer-events:none;}
  #polycard.on{display:block;}
  #polycard .pc-badge{display:inline-block;font-size:10.5px;color:var(--gold);
    border:1px solid var(--line);border-radius:4px;padding:1px 7px;margin-bottom:7px;}
  #polycard .pc-title{font-family:'Noto Serif KR',serif;font-weight:700;font-size:15px;
    color:#fff;margin-bottom:3px;}
  #polycard .pc-novel{font-size:11.5px;color:var(--dim);margin-bottom:6px;}
  #polycard .pc-slogan{font-size:12.5px;color:var(--gold);font-style:italic;margin-bottom:7px;}
  #polycard .pc-mirror{font-size:11px;color:#a0aec0;border-top:1px solid var(--line);padding-top:6px;}

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
    <button id="btnGene">계보</button>
    <button id="btnPoly">입체</button>
    <button id="btnTable">표</button>
  </div>

  <div class="legend" id="legend"></div>
  <div id="tip"></div>
  <div id="polyhint">끌어서 돌리기 · <b>중심</b>에 가까울수록 여러 장을 관통하는 핵심 생각, <b>표면(꼭짓점)</b>일수록 한 장에 특화 — 깊이 = 일반성 · 꼭짓점(장)에 올리면 그 장의 <b>슬로건</b></div>
  <div id="genehint"><b>중심</b> = 이 책 · <b>안쪽 고리</b> = 감정·상징 · <b>가운데 고리</b> = 생각 · <b>바깥 고리</b> = 딛고 선 고전 원작 — 끌어서 흩어보세요</div>
  <div id="polycard">
    <div class="pc-badge"></div>
    <div class="pc-title"></div>
    <div class="pc-novel"></div>
    <div class="pc-slogan"></div>
    <div class="pc-mirror"></div>
  </div>
</div>

<script>
const DATA = /*__DATA__*/;

/* ---------- 공통 ---------- */
const fams = DATA.families;               // {"1":{name,color},...}
const hubs = DATA.hubs;                   // [{id,name,aux}]
const elems = DATA.elements;              // [{id,title,fam,star,def,chaps}]
const CHAP_FILE = DATA.chapFile || {};    // 장번호 → reader 파일명 (클릭 네비)
document.getElementById('nCount').textContent = elems.length;
const famOff = new Set();                  // 숨긴 족
let tableOn = false;                        // 표 뷰 여부 (loop보다 먼저 선언)
let polyOn = false;                         // 입체 뷰 여부
let geneOn = false;                         // 계보(은하수) 뷰 여부
const GENE = /*__GENEALOGY__*/;             // 계보 데이터 (reference_graph 흡수)
const CHAP_META = /*__CHAPMETA__*/;         // 장 슬로건/소설/거울쌍 (bookmap 흡수)

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
/* ── 클릭(드래그 아님) → 그 장의 구절로: reader.html?file=chN&q=원소이름 ── */
let pressing=false,moved=false,pDownX=0,pDownY=0,pDownNode=null;
function navTo(chaps,title){
  const cand=(chaps||[]).filter(c=>c!=='__aux__');
  const chap=(highlightHub&&cand.includes(highlightHub))?highlightHub:cand[0];
  if(!chap)return;                          // 부록 전용 원소 = 이동 안 함
  const f=CHAP_FILE[chap]; if(!f)return;
  window.location.href='reader.html?file='+f+'&q='+encodeURIComponent(title);
}

/* ---------- 입체(다면체) : stella octangula ---------- */
// bookmap_3d.html 정본 좌표(정육면체 꼭짓점) — cage4 + nest4 = 사면체 안의 사면체
const V3={'1':[1,1,1],'2':[1,-1,-1],'3':[-1,1,-1],'4':[-1,-1,1],
          '6':[-1,-1,-1],'8':[-1,1,1],'7':[1,-1,1],'9':[1,1,-1],
          '5':[0,0,0],'10':[0,0,0],'__aux__':[0,0,0]};
const CAGE_V=['1','2','3','4'], NEST_V=['6','7','8','9'];
const TETRA_E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];   // 사면체 6변
// 원소 3D 위치 = 속한 장 꼭짓점 평균 (+결정적 지터). k=1→꼭짓점, k=2→모서리, k≥3→면·내부
let _seed=1; const _rnd=()=>{_seed=(_seed*16807)%2147483647;return _seed/2147483647-0.5;};
const poly=elems.map((e,i)=>{
  let x=0,y=0,z=0,k=0;
  e.chaps.forEach(c=>{const v=V3[c]||V3['__aux__'];x+=v[0];y+=v[1];z+=v[2];k++;});
  if(k){x/=k;y/=k;z/=k;}
  const j=0.11;
  return {e,i,bx:x+_rnd()*j,by:y+_rnd()*j,bz:z+_rnd()*j,px:0,py:0,pr:0};
});
let ax=0.5, ay=0.7, dragRot=false, lastMX=0, lastMY=0, hoverPoly=-1;
function rot3(x,y,z){
  const cy=Math.cos(ay),sy=Math.sin(ay);
  let x1=x*cy+z*sy, z1=-x*sy+z*cy;
  const cx=Math.cos(ax),sx=Math.sin(ax);
  let y1=y*cx-z1*sx, z2=y*sx+z1*cx;
  return [x1,y1,z2];
}
function project(x,y,z){
  const [rx,ry,rz]=rot3(x,y,z);
  const R=Math.min(W,H)*0.24, f=3.4, d=f/(f-rz);
  return {sx:W/2+rx*R*d, sy:H*0.52-ry*R*d, z:rz, d:d};
}
function draw3d(){
  ctx.clearRect(0,0,W,H);
  const vp={}; Object.keys(V3).forEach(k=>{const v=V3[k];vp[k]=project(v[0],v[1],v[2]);});
  polyVerts=vp;   // 꼭짓점 슬로건 카드 hit-test용
  // 두 사면체 변
  function tetra(vlist,style,dash){
    ctx.strokeStyle=style;ctx.lineWidth=1.3;ctx.setLineDash(dash||[]);
    TETRA_E.forEach(([a,b])=>{const pa=vp[vlist[a]],pb=vp[vlist[b]];
      ctx.beginPath();ctx.moveTo(pa.sx,pa.sy);ctx.lineTo(pb.sx,pb.sy);ctx.stroke();});
    ctx.setLineDash([]);
  }
  tetra(CAGE_V,'rgba(203,180,135,.40)');        // 새장 사면체(금 실선)
  tetra(NEST_V,'rgba(138,182,214,.36)',[6,5]);  // 둥지 사면체(청 점선)
  // 원소 (깊이 정렬)
  const ds=[];
  poly.forEach(o=>{if(famOff.has(String(o.e.fam)))return;
    const p=project(o.bx,o.by,o.bz);o.px=p.sx;o.py=p.sy;o.pr=(o.e.star?6.5:4)*p.d*0.82;ds.push({o,p});});
  ds.sort((a,b)=>a.p.z-b.p.z);
  ds.forEach(({o,p})=>{
    const far=Math.max(0,Math.min(1,(p.z+1.4)/2.8));
    ctx.globalAlpha=0.32+0.68*far;
    ctx.fillStyle=o.e._c||(o.e._c=fams[o.e.fam].color);
    ctx.beginPath();ctx.arc(o.px,o.py,Math.max(1.6,o.pr),0,7);ctx.fill();
    if(o.e.star){ctx.strokeStyle='#c5a55a';ctx.lineWidth=1.4;
      ctx.beginPath();ctx.arc(o.px,o.py,o.pr+2,0,7);ctx.stroke();}
    if(o.i===hoverPoly){ctx.strokeStyle='#e8e0d4';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.arc(o.px,o.py,o.pr+3.5,0,7);ctx.stroke();}
    ctx.globalAlpha=1;
  });
  // 꼭짓점 라벨(8장)
  hubs.forEach(h=>{
    if(!CAGE_V.includes(h.id)&&!NEST_V.includes(h.id))return;
    const p=vp[h.id],far=Math.max(0,Math.min(1,(p.z+1.4)/2.8)),cage=CAGE_V.includes(h.id);
    ctx.globalAlpha=0.5+0.5*far;
    ctx.fillStyle=cage?'#241f19':'#1a2230';ctx.strokeStyle=cage?'#cbb487':'#8ab6d6';ctx.lineWidth=1.4;
    ctx.beginPath();ctx.arc(p.sx,p.sy,7,0,7);ctx.fill();ctx.stroke();
    ctx.fillStyle='#e8e0d4';ctx.font="600 12px 'Noto Serif KR',serif";
    ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(h.name,p.sx,p.sy-15);
    ctx.globalAlpha=1;
  });
  // 중심 ★ (5↔10 회전축)
  const c=project(0,0,0);
  ctx.globalAlpha=.92;ctx.fillStyle='#c5a55a';ctx.font="18px serif";
  ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('★',c.sx,c.sy);
  ctx.font="9.5px 'Noto Sans KR'";ctx.fillStyle='#9a8a4a';ctx.fillText('5↔10 회전축',c.sx,c.sy+15);
  ctx.globalAlpha=1;
  if(!dragRot) ay+=0.0035;   // 자동 회전
}
function polyAt(mx,my){
  let best=-1,bd=1e9;
  poly.forEach(o=>{if(famOff.has(String(o.e.fam)))return;
    const dx=mx-o.px,dy=my-o.py,d=dx*dx+dy*dy,rr=Math.max(9,o.pr+5);
    if(d<rr*rr&&d<bd){bd=d;best=o.i;}});
  return best;
}
function showTip(e,mx,my){
  const chapNames=e.chaps.map(c=>c==='__aux__'?'전반·부록':(hubs.find(h=>h.id===c)?.name||c)).join(' · ');
  tip.innerHTML=`<div class="t-title">${e.star?'★ ':''}${e.title}</div>`+
    (e.def?`<div>${e.def}</div>`:'')+`<div class="t-meta">${fams[e.fam].name} · 장 ${chapNames}`+
    (e.chaps.some(c=>c!=='__aux__')?`<br><span style="color:var(--gold)">클릭 → 그 장의 구절로 →</span>`:'')+`</div>`;
  tip.style.opacity=1;let tx=mx+14,ty=my+14;
  if(tx+290>W)tx=mx-294;if(ty+120>H)ty=my-120;
  tip.style.left=tx+'px';tip.style.top=ty+'px';
}

/* ---------- 입체 꼭짓점(장) 슬로건 카드 (bookmap_3d 흡수) ---------- */
let polyVerts={};          // 최근 프레임의 꼭짓점 화면좌표 {chapId:{sx,sy}}
let hoverVert=null;        // 현재 올린 장 꼭짓점 id
const polyCard=document.getElementById('polycard');
function polyVertexAt(mx,my){
  let best=null,bd=1e9;
  [...CAGE_V,...NEST_V].forEach(id=>{
    const p=polyVerts[id];if(!p)return;
    const dx=mx-p.sx,dy=my-p.sy,d=dx*dx+dy*dy;
    if(d<196&&d<bd){bd=d;best=id;}     // 14px 반경
  });
  return best;
}
function showPolyCard(chapId){
  const m=CHAP_META[chapId];if(!m){polyCard.classList.remove('on');return;}
  const hub=hubs.find(h=>h.id===chapId);
  const isCage=CAGE_V.includes(chapId);
  polyCard.querySelector('.pc-badge').textContent=isCage?(chapId+'장 · 새장'):(chapId+'장 · 둥지');
  polyCard.querySelector('.pc-title').textContent=hub?hub.name:(chapId+'장');
  polyCard.querySelector('.pc-novel').textContent='소설: '+m.novel;
  polyCard.querySelector('.pc-slogan').textContent='「'+m.slogan+'」';
  const mm=CHAP_META[String(m.mirror)];
  polyCard.querySelector('.pc-mirror').textContent=mm?('↔ 거울쌍 '+m.mirror+'장 「'+mm.slogan+'」'):'';
  polyCard.classList.add('on');
}

/* ---------- 계보(은하수) : reference_graph 흡수 ---------- */
const GENE_ROLE={0:'#efe3c0',1:'#b5a3f8',2:'#7cb0db',3:'#c5a55a'};
const GENE_SECT=[0,Math.PI/2,Math.PI,3*Math.PI/2];
const elemFam={}; elems.forEach(e=>elemFam[e.id]=e.fam);
let geneNodes=[],geneEdges=[],geneById={},geneInited=false,geneHover=null,geneDrag=null;
function geneRadii(){const R=Math.min(W,H);return {1:R*0.15,2:R*0.30,3:R*0.44,0:0};}
function geneInit(){
  const rr=geneRadii();
  if(geneInited){geneNodes.forEach(n=>n.tr=rr[n.marr_layer]||0);return;}
  // 층별 노드를 전체 원에 고르게 분포 = 동심원 3고리(sector 뭉침 제거, 반지름 하나만 뜻을 실음)
  const lc={}; GENE.nodes.forEach(n=>{lc[n.marr_layer]=(lc[n.marr_layer]||0)+1;});
  const li={};
  geneNodes=GENE.nodes.map(n=>{
    const cnt=lc[n.marr_layer]||1, i=(li[n.marr_layer]=(li[n.marr_layer]||0)+1)-1;
    const ang=(i/cnt)*Math.PI*2 + _rnd()*0.12, tr=rr[n.marr_layer]||0;
    return {...n, tr, fam:elemFam[n.id]||null,
      rad:n.marr_layer===0?13:(n.marr_layer===1?11:(n.marr_layer===3?6.5:4.2)),
      x:W/2+Math.cos(ang)*(tr+_rnd()*20), y:H/2+Math.sin(ang)*(tr+_rnd()*20), vx:0, vy:0};
  });
  geneById={}; geneNodes.forEach(n=>geneById[n.id]=n);
  geneEdges=GENE.edges.filter(e=>geneById[e.s]&&geneById[e.t]);
  geneInited=true;
}
function geneTick(){
  const cx=W/2,cy=H/2;
  geneNodes.forEach(a=>{
    if(a.marr_layer===0){a.x=cx;a.y=cy;a.vx=a.vy=0;return;}
    if(a===geneDrag)return;
    const dx=a.x-cx,dy=a.y-cy,cur=Math.hypot(dx,dy)||1,ca=Math.atan2(dy,dx);
    const rf=(a.tr-cur)*0.045; a.vx+=dx/cur*rf; a.vy+=dy/cur*rf;
    // 각도 목표 인력 제거 → 반지름 유지 + 같은 층 반발만 = 고리 위 고른 분포
  });
  for(let i=0;i<geneNodes.length;i++){const a=geneNodes[i];if(a.marr_layer===0)continue;
    for(let j=i+1;j<geneNodes.length;j++){const b=geneNodes[j];if(b.marr_layer!==a.marr_layer)continue;
      let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+.01;if(d2>16000)continue;
      const d=Math.sqrt(d2),f=200/d2,fx=dx/d*f,fy=dy/d*f;
      if(a!==geneDrag){a.vx+=fx;a.vy+=fy;} if(b!==geneDrag){b.vx-=fx;b.vy-=fy;}
    }
  }
  geneNodes.forEach(n=>{if(n===geneDrag||n.marr_layer===0)return;
    n.vx*=0.84;n.vy*=0.84;n.x+=n.vx;n.y+=n.vy;});
}
function geneDim(n){return n.marr_layer===2&&n.fam&&famOff.has(String(n.fam));}
function geneDraw(){
  ctx.clearRect(0,0,W,H);
  geneEdges.forEach(e=>{const a=geneById[e.s],b=geneById[e.t];
    const hot=geneHover&&(e.s===geneHover.id||e.t===geneHover.id);
    ctx.strokeStyle=hot?'rgba(197,165,90,.5)':'rgba(120,110,96,.07)';ctx.lineWidth=hot?1.3:0.6;
    ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();});
  geneNodes.forEach(n=>{
    const dim=geneDim(n); ctx.globalAlpha=dim?0.12:1;
    if(n.marr_layer===1){          // 감정·상징 = 이모지 그대로
      ctx.font="16px 'Noto Sans KR'";ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(n.label,n.x,n.y);
    }else{
      ctx.fillStyle=GENE_ROLE[n.marr_layer]||'#888';
      ctx.beginPath();ctx.arc(n.x,n.y,n.rad,0,7);ctx.fill();
    }
    if(geneHover&&geneHover.id===n.id){ctx.globalAlpha=1;ctx.strokeStyle='#e8e0d4';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.arc(n.x,n.y,n.rad+3,0,7);ctx.stroke();}
    ctx.globalAlpha=1;
    if(n.marr_layer===0){ctx.fillStyle='#efe3c0';ctx.font="700 14px 'Noto Serif KR',serif";
      ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(n.label,n.x,n.y-n.rad-11);}
  });
}
function geneAt(mx,my){let best=null,bd=1e9;
  geneNodes.forEach(n=>{const dx=mx-n.x,dy=my-n.y,d=dx*dx+dy*dy,rr=Math.max(11,n.rad+5);
    if(d<rr*rr&&d<bd){bd=d;best=n;}});
  return best;}
function showGeneTip(n,mx,my){
  let t=n.label,meta='';
  if(n.marr_layer===0)meta='이 책';
  else if(n.marr_layer===1)meta='감정·상징';
  else if(n.marr_layer===3)meta='이 책이 딛고 선 고전 원작';
  else{const e=elems.find(x=>x.id===n.id);
    if(e){t=(e.star?'★ ':'')+e.title;meta=fams[e.fam].name.replace(/^\d+\.\s*/,'')+(e.def?' · '+e.def:'');}else meta='생각';}
  tip.innerHTML=`<div class="t-title">${t}</div>`+(meta?`<div class="t-meta">${meta}</div>`:'');
  tip.style.opacity=1;let tx=mx+14,ty=my+14;
  if(tx+290>W)tx=mx-294;if(ty+120>H)ty=my-120;
  tip.style.left=tx+'px';tip.style.top=ty+'px';
}

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
function loop(){
  if(!tableOn){ if(geneOn){geneTick();geneDraw();} else if(polyOn) draw3d(); else { sim(); draw(); } }
  requestAnimationFrame(loop);
}
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
  if(pressing){const ddx=mx-pDownX,ddy=my-pDownY;if(ddx*ddx+ddy*ddy>20)moved=true;}
  if(geneOn){
    if(geneDrag){geneDrag.x=mx;geneDrag.y=my;geneDrag.vx=geneDrag.vy=0;return;}
    const n=geneAt(mx,my);geneHover=n;
    if(n){showGeneTip(n,mx,my);}else{tip.style.opacity=0;}
    return;
  }
  if(polyOn){
    if(dragRot){ay+=(mx-lastMX)*0.008;ax+=(my-lastMY)*0.008;
      ax=Math.max(-1.4,Math.min(1.4,ax));lastMX=mx;lastMY=my;
      tip.style.opacity=0;polyCard.classList.remove('on');hoverVert=null;return;}
    const vc=polyVertexAt(mx,my);
    if(vc){hoverVert=vc;hoverPoly=-1;showPolyCard(vc);tip.style.opacity=0;return;}
    hoverVert=null;polyCard.classList.remove('on');
    const i=polyAt(mx,my);hoverPoly=i;
    if(i>=0){showTip(poly[i].e,mx,my);}else{tip.style.opacity=0;}
    return;
  }
  if(dragNode){dragNode.x=mx;dragNode.y=my;dragNode.vx=dragNode.vy=0;return;}
  const n=nodeAt(mx,my);
  hoverId=n?n.id:null;
  if(n&&n.kind==='el'){
    const chapNames=n.chaps.map(c=>{
      if(c==='__aux__')return '전반·부록';
      const h=hubs.find(h=>h.id===c);return h?h.name:c;}).join(' · ');
    tip.innerHTML=`<div class="t-title">${n.star?'★ ':''}${n.label}</div>`+
      (n.def?`<div>${n.def}</div>`:'')+
      `<div class="t-meta">${fams[n.fam].name} · 장 ${chapNames}`+
      (n.chaps.some(c=>c!=='__aux__')?`<br><span style="color:var(--gold)">클릭 → 그 장의 구절로 →</span>`:'')+`</div>`;
    tip.style.opacity=1;
    let tx=mx+14,ty=my+14;
    if(tx+290>W)tx=mx-294;if(ty+120>H)ty=my-120;
    tip.style.left=tx+'px';tip.style.top=ty+'px';
  }else{tip.style.opacity=0;}
});
canvas.addEventListener('mousedown',ev=>{
  pressing=true;moved=false;pDownX=ev.clientX;pDownY=ev.clientY;pDownNode=null;
  if(geneOn){const g=geneAt(ev.clientX,ev.clientY);
    if(g&&g.marr_layer!==0){geneDrag=g;canvas.classList.add('drag');}return;}
  if(polyOn){dragRot=true;lastMX=ev.clientX;lastMY=ev.clientY;canvas.classList.add('drag');return;}
  const n=nodeAt(ev.clientX,ev.clientY);
  pDownNode=n;
  if(n){
    if(n.kind==='hub'){
      const hid=n.id.slice(4);
      highlightHub=(highlightHub===hid)?null:hid;
    }else{dragNode=n;canvas.classList.add('drag');}
  }else{highlightHub=null;}
});
addEventListener('mouseup',()=>{
  if(pressing&&!moved){
    if(geneOn){/* 계보: 드래그 핀만, 클릭 이동 없음 */}
    else if(polyOn){
      if(hoverVert&&CHAP_FILE[hoverVert]){window.location.href='reader.html?file='+CHAP_FILE[hoverVert];}
      else if(hoverPoly>=0)navTo(poly[hoverPoly].e.chaps,poly[hoverPoly].e.title);
    }
    else if(pDownNode&&pDownNode.kind==='el'){navTo(pDownNode.chaps,pDownNode.label);}
  }
  pressing=false;pDownNode=null;dragNode=null;dragRot=false;geneDrag=null;canvas.classList.remove('drag');
});
canvas.addEventListener('mouseleave',()=>{tip.style.opacity=0;});
// 터치
canvas.addEventListener('touchstart',ev=>{
  const t=ev.touches[0];
  pressing=true;moved=false;pDownX=t.clientX;pDownY=t.clientY;pDownNode=null;
  if(geneOn){const g=geneAt(t.clientX,t.clientY);if(g&&g.marr_layer!==0)geneDrag=g;return;}
  if(polyOn){dragRot=true;lastMX=t.clientX;lastMY=t.clientY;hoverPoly=polyAt(t.clientX,t.clientY);return;}
  const n=nodeAt(t.clientX,t.clientY);pDownNode=n;
  if(n&&n.kind==='hub'){const hid=n.id.slice(4);
    highlightHub=(highlightHub===hid)?null:hid;}
  else if(n){dragNode=n;}},{passive:true});
canvas.addEventListener('touchmove',ev=>{
  const t=ev.touches[0];
  if(pressing){const ddx=t.clientX-pDownX,ddy=t.clientY-pDownY;if(ddx*ddx+ddy*ddy>25)moved=true;}
  if(geneOn&&geneDrag){geneDrag.x=t.clientX;geneDrag.y=t.clientY;geneDrag.vx=geneDrag.vy=0;return;}
  if(polyOn&&dragRot){ay+=(t.clientX-lastMX)*0.008;ax+=(t.clientY-lastMY)*0.008;
    ax=Math.max(-1.4,Math.min(1.4,ax));lastMX=t.clientX;lastMY=t.clientY;return;}
  if(dragNode){dragNode.x=t.clientX;dragNode.y=t.clientY;
    dragNode.vx=dragNode.vy=0;}},{passive:true});
canvas.addEventListener('touchend',()=>{
  if(pressing&&!moved){
    if(polyOn){if(hoverPoly>=0)navTo(poly[hoverPoly].e.chaps,poly[hoverPoly].e.title);}
    else if(pDownNode&&pDownNode.kind==='el'){navTo(pDownNode.chaps,pDownNode.label);}
  }
  pressing=false;pDownNode=null;dragNode=null;dragRot=false;geneDrag=null;});

/* ---------- 표 뷰 ---------- */
const tableView=document.getElementById('tableView');
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
      const cands = e.chaps.filter(x=>x!=='__aux__');
      const chap = cands[0];
      const linkFile = CHAP_FILE[chap];
      const clickAttr = linkFile ? `style="cursor:pointer;" onclick="window.location.href='reader.html?file=${linkFile}&q=${encodeURIComponent(e.title)}'"` : '';
      h+=`<tr ${clickAttr}><td class="name">${e.star?'<span class="star-mark">★</span> ':''}${e.title}`+
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
const btnMap=document.getElementById('btnMap'),btnGene=document.getElementById('btnGene'),
      btnPoly=document.getElementById('btnPoly'),btnTable=document.getElementById('btnTable');
let _routing=false;
function setView(v){
  tableOn=(v==='table');polyOn=(v==='poly');geneOn=(v==='gene');
  tableView.classList.toggle('show',tableOn);
  if(tableOn)renderTable();
  if(geneOn)geneInit();
  document.body.classList.toggle('poly',polyOn);
  document.body.classList.toggle('gene',geneOn);
  btnMap.classList.toggle('on',v==='map');
  btnGene.classList.toggle('on',v==='gene');
  btnPoly.classList.toggle('on',v==='poly');
  btnTable.classList.toggle('on',v==='table');
  tip.style.opacity=0;highlightHub=null;hoverPoly=-1;hoverVert=null;
  polyCard.classList.remove('on');geneHover=null;geneDrag=null;
  const hash={map:'#map',gene:'#gene',poly:'#poly',table:'#table'}[v];
  if(hash&&location.hash!==hash){_routing=true;location.hash=hash;_routing=false;}
}
btnMap.onclick=()=>setView('map');
btnGene.onclick=()=>setView('gene');
btnPoly.onclick=()=>setView('poly');
btnTable.onclick=()=>setView('table');
/* ---------- URL 해시 렌즈 라우팅 (딥링크: 리다이렉트 stub이 바로 해당 렌즈로) ---------- */
function viewFromHash(){
  const h=(location.hash||'').toLowerCase();
  if(h==='#gene')return 'gene';
  if(h==='#poly'||h==='#3d')return 'poly';
  if(h==='#table'||h==='#matrix')return 'table';
  if(h==='#map')return 'map';
  return null;                                   // 없거나 모르는 해시 → 기본 지도
}
addEventListener('hashchange',()=>{if(_routing)return;const v=viewFromHash();if(v)setView(v);});
(function(){const v=viewFromHash();if(v&&v!=='map')setView(v);})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
