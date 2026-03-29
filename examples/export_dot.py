"""지식 그래프를 DOT 형식으로 출력합니다."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# 시나리오 그래프 재사용 (출력 억제)
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(os.path.dirname(__file__), "ontology_kg_rag.py")).read())

# 레이블별 색상
COLORS = {
    "Paradigm":  "#4A90D9",  # 파랑
    "Concept":   "#7ED321",  # 초록
    "Standard":  "#F5A623",  # 주황
    "Tool":      "#9B59B6",  # 보라
    "Component": "#E74C3C",  # 빨강
}

lines = ['digraph KnowledgeGraph {', '  rankdir=LR;',
         '  node [fontname="Helvetica", fontsize=11, style=filled, fontcolor=white];',
         '  edge [fontsize=9, color="#888888"];', '']

for node in kg.all_nodes():
    color = COLORS.get(node.label, "#888888")
    name  = node.properties.get("name", node.id)
    lines.append(f'  "{node.id}" [label="{name}", fillcolor="{color}", shape=ellipse];')

lines.append('')
for edge in kg.get_edges():
    lines.append(f'  "{edge.source}" -> "{edge.target}" [label="{edge.relation}"];')

lines.append('}')
print('\n'.join(lines))
