"""
지식 그래프를 인터랙티브 HTML로 내보냅니다. (vis.js CDN, 설치 불필요)

사용법:
    python examples/generate_html.py
    python -m http.server 8080
    → 브라우저에서 http://localhost:8080/examples/knowledge_graph.html
"""
import sys, os, io, json, contextlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(os.path.dirname(__file__), "ontology_kg_rag.py")).read())

COLORS = {
    "Paradigm":  {"bg": "#4A90D9", "border": "#2c6fad"},
    "Concept":   {"bg": "#27AE60", "border": "#1e8449"},
    "Standard":  {"bg": "#E67E22", "border": "#ca6f1e"},
    "Tool":      {"bg": "#8E44AD", "border": "#6c3483"},
    "Component": {"bg": "#C0392B", "border": "#922b21"},
}

nodes_data = []
for i, node in enumerate(kg.all_nodes()):
    c = COLORS.get(node.label, {"bg": "#888", "border": "#555"})
    nodes_data.append({
        "id":    node.id,
        "label": node.properties.get("name", node.id),
        "title": f"<b>{node.properties.get('name', node.id)}</b><br>{node.label}<br><i>{node.properties.get('desc', '')}</i>",
        "color": {"background": c["bg"], "border": c["border"],
                  "highlight": {"background": c["bg"], "border": "#fff"}},
        "font":  {"color": "#ffffff", "size": 13},
        "shape": "ellipse",
        "size":  20 if node.label == "Paradigm" else 14,
    })

edges_data = []
for i, edge in enumerate(kg.get_edges()):
    edges_data.append({
        "id":     i,
        "from":   edge.source,
        "to":     edge.target,
        "label":  edge.relation,
        "arrows": "to",
        "font":   {"size": 9, "color": "#555", "align": "middle"},
        "color":  {"color": "#aaaaaa", "highlight": "#555"},
        "smooth": {"type": "curvedCW", "roundness": 0.1},
    })

LEGEND = "\n".join(
    f'<span style="background:{c["bg"]};color:#fff;padding:3px 10px;border-radius:12px;margin:3px;display:inline-block;">{label}</span>'
    for label, c in COLORS.items()
)

# 인사이트: 경로 탐색 결과
def fmt_path(p):
    return " → ".join(p) if p else "경로 없음"

INSIGHTS = [
    {
        "title": "OWL → LLM 경로",
        "path":  fmt_path(kg.find_path("owl", "llm")),
        "desc":  "표준(OWL)이 KG 스키마를 정의하고, KG가 RAG에 지식을 공급하고, RAG가 LLM을 강화하는 흐름"
    },
    {
        "title": "Triple → Context 경로",
        "path":  fmt_path(kg.find_path("triple", "context")),
        "desc":  "온톨로지의 최소 단위 트리플이 KG를 거쳐 RAG의 컨텍스트로 변환되는 경로"
    },
    {
        "title": "Inference → LLM 경로",
        "path":  fmt_path(kg.find_path("inference", "llm")),
        "desc":  "온톨로지 추론 능력이 RAG를 통해 LLM에 도달 — 두 단계로 직행"
    },
    {
        "title": "세 패러다임 공통 허브",
        "path":  ", ".join(sorted(
            {n.id for n in kg.subgraph("ontology", depth=4).all_nodes()} &
            {n.id for n in kg.subgraph("knowledge_graph", depth=4).all_nodes()} &
            {n.id for n in kg.subgraph("rag", depth=4).all_nodes()} -
            {"ontology", "knowledge_graph", "rag"}
        )),
        "desc":  "세 패러다임 모두에서 도달 가능한 노드 — RAG가 온톨로지·KG의 지식을 소비하는 접점"
    },
]

INSIGHTS_HTML = "\n".join(f"""
  <div class="insight">
    <div class="insight-title">{i['title']}</div>
    <div class="insight-path">{i['path']}</div>
    <div class="insight-desc">{i['desc']}</div>
  </div>""" for i in INSIGHTS)

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>온톨로지 · 지식그래프 · RAG</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Helvetica Neue", sans-serif; background: #1a1a2e; color: #eee; display: flex; flex-direction: column; height: 100vh; }}
  h1 {{ padding: 14px 20px 4px; font-size: 17px; color: #fff; flex-shrink: 0; }}
  #legend {{ padding: 0 20px 8px; font-size: 12px; flex-shrink: 0; }}
  #main {{ display: flex; flex: 1; overflow: hidden; }}
  #graph {{ flex: 1; border-top: 1px solid #333; }}
  #sidebar {{ width: 300px; background: #16213e; border-top: 1px solid #333; border-left: 1px solid #333;
              overflow-y: auto; padding: 14px; flex-shrink: 0; }}
  #sidebar h2 {{ font-size: 13px; color: #aaa; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
  .insight {{ background: #0f3460; border-radius: 8px; padding: 10px 12px; margin-bottom: 10px; }}
  .insight-title {{ font-size: 12px; color: #4A90D9; font-weight: bold; margin-bottom: 4px; }}
  .insight-path {{ font-size: 11px; color: #7ED321; font-family: monospace; margin-bottom: 5px; word-break: break-all; }}
  .insight-desc {{ font-size: 11px; color: #bbb; line-height: 1.5; }}
  #tooltip {{ position: fixed; bottom: 20px; left: 20px; background: rgba(0,0,0,.85);
              padding: 10px 14px; border-radius: 8px; font-size: 12px;
              max-width: 240px; display: none; line-height: 1.6; z-index: 10; }}
</style>
</head>
<body>
<h1>온톨로지 · 지식그래프 · RAG 지식 구조</h1>
<div id="legend">{LEGEND}</div>
<div id="main">
  <div id="graph"></div>
  <div id="sidebar">
    <h2>인사이트</h2>
    {INSIGHTS_HTML}
  </div>
</div>
<div id="tooltip"></div>
<script>
const nodes = new vis.DataSet({json.dumps(nodes_data, ensure_ascii=False)});
const edges = new vis.DataSet({json.dumps(edges_data, ensure_ascii=False)});
const options = {{
  physics: {{
    solver: "forceAtlas2Based",
    forceAtlas2Based: {{ gravitationalConstant: -60, springLength: 120, springConstant: 0.08 }},
    stabilization: {{ iterations: 200 }},
  }},
  interaction: {{ hover: true, tooltipDelay: 100 }},
  layout: {{ improvedLayout: true }},
}};
const network = new vis.Network(
  document.getElementById("graph"),
  {{ nodes, edges }},
  options
);
const tip = document.getElementById("tooltip");
network.on("hoverNode", p => {{
  const n = nodes.get(p.node);
  tip.innerHTML = n.title;
  tip.style.display = "block";
}});
network.on("blurNode", () => tip.style.display = "none");
</script>
</body>
</html>
"""

out = os.path.join(os.path.dirname(__file__), "knowledge_graph.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"생성 완료: {out}")
print("실행: python -m http.server 8080")
print("접속: http://localhost:8080/examples/knowledge_graph.html")
