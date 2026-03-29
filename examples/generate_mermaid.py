"""지식 그래프를 GitHub에서 바로 보이는 Mermaid 마크다운으로 내보냅니다."""
import sys, os, io, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(os.path.dirname(__file__), "ontology_kg_rag.py")).read())

STYLES = {
    "Paradigm":  "fill:#4A90D9,color:#fff,stroke:#2c6fad",
    "Concept":   "fill:#27AE60,color:#fff,stroke:#1e8449",
    "Standard":  "fill:#E67E22,color:#fff,stroke:#ca6f1e",
    "Tool":      "fill:#8E44AD,color:#fff,stroke:#6c3483",
    "Component": "fill:#C0392B,color:#fff,stroke:#922b21",
}

lines = ["```mermaid", "flowchart LR"]

# classDef
for label, style in STYLES.items():
    lines.append(f"    classDef {label} {style}")
lines.append("")

# 노드
for node in kg.all_nodes():
    name = node.properties.get("name", node.id)
    lines.append(f'    {node.id}["{name}"]:::{node.label}')
lines.append("")

# 엣지
for edge in kg.get_edges():
    lines.append(f'    {edge.source} -->|{edge.relation}| {edge.target}')

lines.append("```")

md = f"""# 온톨로지 · 지식그래프 · RAG 지식 구조

> 자동 생성된 Mermaid 다이어그램 — `python examples/generate_mermaid.py` 로 재생성

## 색상 범례

| 색상 | 종류 | 예시 |
|------|------|------|
| 🔵 파랑 | Paradigm | 온톨로지, 지식그래프, RAG |
| 🟢 초록 | Concept | Triple, Embedding, Context |
| 🟠 주황 | Standard | OWL, RDF, SPARQL, Cypher |
| 🟣 보라 | Tool | Neo4j, LlamaIndex, Weaviate |
| 🔴 빨강 | Component | LLM, Retriever, Vector DB |

## 그래프

{chr(10).join(lines)}
"""

out = os.path.join(os.path.dirname(__file__), "knowledge_graph.md")
with open(out, "w", encoding="utf-8") as f:
    f.write(md)

print(f"생성 완료: {out}")
