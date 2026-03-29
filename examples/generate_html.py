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

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>온톨로지 · 지식그래프 · RAG</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "Helvetica Neue", sans-serif; background: #1a1a2e; color: #eee; }}
  h1 {{ padding: 16px 20px 6px; font-size: 18px; color: #fff; }}
  #legend {{ padding: 0 20px 12px; font-size: 12px; }}
  #graph {{ width: 100%; height: calc(100vh - 90px); border-top: 1px solid #333; }}
  #tooltip {{ position: fixed; bottom: 20px; left: 20px; background: rgba(0,0,0,.8);
              padding: 10px 14px; border-radius: 8px; font-size: 12px;
              max-width: 280px; display: none; line-height: 1.6; }}
</style>
</head>
<body>
<h1>온톨로지 · 지식그래프 · RAG 지식 구조</h1>
<div id="legend">{LEGEND}</div>
<div id="graph"></div>
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
