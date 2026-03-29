"""
온톨로지 · 지식그래프 · RAG 지식 구조 탐색 예시

노드 레이블:
  Paradigm   - 패러다임/접근법 (예: 온톨로지, 지식그래프, RAG)
  Concept    - 핵심 개념 (예: Triple, Embedding, Entity)
  Standard   - 표준/언어 (예: OWL, RDF, SPARQL)
  Tool       - 도구/시스템 (예: Neo4j, Weaviate, ChromaDB)
  Component  - 구성 요소 (예: Vector DB, LLM, Retriever)

관계 타입:
  CONTAINS   - 포함한다
  USES       - 사용한다
  EXTENDS    - 확장한다
  ENABLES    - 가능하게 한다
  STORED_IN  - 저장된다
  QUERIES    - 질의한다
  FEEDS_INTO - 입력으로 들어간다
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from knowledge_graph import KnowledgeGraph

kg = KnowledgeGraph()

# ────────────────────────────────────────────────
# 패러다임 노드
# ────────────────────────────────────────────────
kg.add_node("ontology",        "Paradigm",  name="온톨로지",       desc="개념과 관계를 형식적으로 정의하는 지식 표현 체계")
kg.add_node("knowledge_graph", "Paradigm",  name="지식그래프",     desc="엔티티와 관계를 그래프로 저장·탐색하는 구조")
kg.add_node("rag",             "Paradigm",  name="RAG",            desc="외부 지식을 검색해 LLM 생성에 활용하는 기법")

# ────────────────────────────────────────────────
# 핵심 개념 노드
# ────────────────────────────────────────────────
kg.add_node("triple",      "Concept", name="Triple",      desc="주어-술어-목적어로 이루어진 지식의 최소 단위")
kg.add_node("class",       "Concept", name="Class",       desc="동일한 속성을 가진 개체들의 집합")
kg.add_node("property",    "Concept", name="Property",    desc="클래스 간 또는 클래스-값 간의 관계를 정의")
kg.add_node("instance",    "Concept", name="Instance",    desc="클래스의 구체적인 개별 개체")
kg.add_node("inference",   "Concept", name="Inference",   desc="정의된 규칙으로 새로운 지식을 자동 도출")
kg.add_node("entity",      "Concept", name="Entity",      desc="지식그래프의 노드: 실세계의 사물·개념·사람")
kg.add_node("relation",    "Concept", name="Relation",    desc="지식그래프의 엣지: 엔티티 간의 관계")
kg.add_node("embedding",   "Concept", name="Embedding",   desc="텍스트·그래프를 고차원 벡터로 변환한 표현")
kg.add_node("chunk",       "Concept", name="Chunk",       desc="문서를 검색 가능한 단위로 분할한 조각")
kg.add_node("context",     "Concept", name="Context",     desc="LLM 프롬프트에 삽입되는 검색된 관련 정보")
kg.add_node("query",       "Concept", name="Query",       desc="사용자의 질문 또는 검색 요청")

# ────────────────────────────────────────────────
# 표준/언어 노드
# ────────────────────────────────────────────────
kg.add_node("rdf",     "Standard", name="RDF",     desc="트리플 기반 데이터 모델 표준 (W3C)")
kg.add_node("owl",     "Standard", name="OWL",     desc="온톨로지 기술 언어, RDF를 확장")
kg.add_node("sparql",  "Standard", name="SPARQL",  desc="RDF 그래프를 위한 쿼리 언어")
kg.add_node("cypher",  "Standard", name="Cypher",  desc="프로퍼티 그래프를 위한 쿼리 언어 (Neo4j)")

# ────────────────────────────────────────────────
# 도구 노드
# ────────────────────────────────────────────────
kg.add_node("neo4j",     "Tool", name="Neo4j",     desc="프로퍼티 그래프 DB, Cypher 사용")
kg.add_node("protege",   "Tool", name="Protégé",   desc="OWL 온톨로지 편집 도구")
kg.add_node("weaviate",  "Tool", name="Weaviate",  desc="벡터+그래프 하이브리드 검색 DB")
kg.add_node("chromadb",  "Tool", name="ChromaDB",  desc="경량 임베딩 벡터 스토어")
kg.add_node("llamaindex","Tool", name="LlamaIndex", desc="지식 인덱싱·RAG 오케스트레이션 프레임워크")

# ────────────────────────────────────────────────
# 컴포넌트 노드
# ────────────────────────────────────────────────
kg.add_node("vector_db",  "Component", name="Vector DB",  desc="고차원 임베딩을 저장하고 ANN 검색을 제공")
kg.add_node("retriever",  "Component", name="Retriever",  desc="질의와 유사한 청크를 검색하는 모듈")
kg.add_node("llm",        "Component", name="LLM",        desc="대규모 언어 모델: 컨텍스트를 받아 답변 생성")
kg.add_node("encoder",    "Component", name="Encoder",    desc="텍스트를 임베딩 벡터로 변환하는 모델")

# ────────────────────────────────────────────────
# 관계 정의
# ────────────────────────────────────────────────

# 온톨로지 내부 구조
kg.add_edge("ontology",        "triple",       "CONTAINS")
kg.add_edge("ontology",        "class",        "CONTAINS")
kg.add_edge("ontology",        "property",     "CONTAINS")
kg.add_edge("ontology",        "instance",     "CONTAINS")
kg.add_edge("ontology",        "inference",    "ENABLES")
kg.add_edge("ontology",        "rdf",          "USES")
kg.add_edge("ontology",        "owl",          "USES")
kg.add_edge("owl",             "rdf",          "EXTENDS")
kg.add_edge("ontology",        "protege",      "USES")
kg.add_edge("class",           "instance",     "CONTAINS")
kg.add_edge("property",        "triple",       "FEEDS_INTO")

# 지식그래프 내부 구조
kg.add_edge("knowledge_graph", "entity",       "CONTAINS")
kg.add_edge("knowledge_graph", "relation",     "CONTAINS")
kg.add_edge("knowledge_graph", "triple",       "STORED_IN")
kg.add_edge("knowledge_graph", "ontology",     "USES",      note="스키마/어휘 정의에 활용")
kg.add_edge("knowledge_graph", "sparql",       "QUERIES")
kg.add_edge("knowledge_graph", "cypher",       "QUERIES")
kg.add_edge("knowledge_graph", "neo4j",        "STORED_IN")
kg.add_edge("entity",          "embedding",    "FEEDS_INTO")
kg.add_edge("rdf",             "triple",       "USES")
kg.add_edge("sparql",          "rdf",          "QUERIES")
kg.add_edge("cypher",          "neo4j",        "QUERIES")

# RAG 내부 구조
kg.add_edge("rag",             "chunk",        "CONTAINS")
kg.add_edge("rag",             "embedding",    "USES")
kg.add_edge("rag",             "vector_db",    "USES")
kg.add_edge("rag",             "retriever",    "CONTAINS")
kg.add_edge("rag",             "llm",          "USES")
kg.add_edge("rag",             "context",      "FEEDS_INTO")
kg.add_edge("chunk",           "embedding",    "FEEDS_INTO")
kg.add_edge("embedding",       "vector_db",    "STORED_IN")
kg.add_edge("query",           "retriever",    "FEEDS_INTO")
kg.add_edge("retriever",       "vector_db",    "QUERIES")
kg.add_edge("retriever",       "context",      "FEEDS_INTO")
kg.add_edge("context",         "llm",          "FEEDS_INTO")
kg.add_edge("encoder",         "embedding",    "ENABLES")
kg.add_edge("weaviate",        "vector_db",    "CONTAINS")
kg.add_edge("chromadb",        "vector_db",    "CONTAINS")
kg.add_edge("llamaindex",      "retriever",    "USES")
kg.add_edge("llamaindex",      "rag",          "ENABLES")

# 도메인 간 연결 (핵심!)
kg.add_edge("knowledge_graph", "rag",          "FEEDS_INTO", note="KG를 RAG의 외부 지식으로 활용")
kg.add_edge("ontology",        "knowledge_graph", "ENABLES", note="온톨로지가 KG의 스키마 역할")
kg.add_edge("knowledge_graph", "embedding",    "FEEDS_INTO", note="그래프 임베딩(node2vec 등)")
kg.add_edge("ontology",        "rag",          "FEEDS_INTO", note="구조화된 어휘를 RAG에 제공")
kg.add_edge("sparql",          "retriever",    "ENABLES",    note="SPARQL 기반 구조적 검색")

# 경로 연결 보완 (방향성으로 끊기는 구간 연결)
kg.add_edge("owl",     "knowledge_graph", "ENABLES",    note="OWL 어휘가 KG 스키마 기반")
kg.add_edge("triple",  "knowledge_graph", "FEEDS_INTO", note="트리플이 KG의 기본 데이터 단위")
kg.add_edge("inference", "knowledge_graph", "ENABLES",  note="추론으로 KG 지식 확장")
kg.add_edge("inference", "rag",           "ENABLES",    note="추론 결과를 RAG 컨텍스트로 활용")


# ────────────────────────────────────────────────
# 탐색 시나리오
# ────────────────────────────────────────────────

SEP = "─" * 55

print(f"\n{SEP}")
print(f"  그래프 크기: {kg}")
print(SEP)

# 1. 세 패러다임 직접 연결 관계
print("\n[1] 세 패러다임의 직접 연결")
for rel in ["ontology", "knowledge_graph", "rag"]:
    direct = kg.get_edges(source=rel)
    targets = [f"{e.target}({e.relation})" for e in direct]
    print(f"  {rel:20s} → {', '.join(targets[:5])} ...")

def show_path(kg, start, end, label):
    path = kg.find_path(start, end)
    if path:
        print(f"  {' → '.join(path)}")
    else:
        print(f"  경로 없음 ({start} → {end})")

# 2. 경로 탐색: OWL → LLM
print(f"\n[2] OWL 에서 LLM 까지 최단 경로")
show_path(kg, "owl", "llm", "")

# 3. 경로 탐색: triple → context
print(f"\n[3] Triple 에서 Context 까지 (온톨로지 → KG → RAG 횡단)")
show_path(kg, "triple", "context", "")

# 4. 경로 탐색: inference → llm (추론 능력의 흐름)
print(f"\n[4] Inference 에서 LLM 까지 경로")
path = kg.find_path("inference", "llm")
if path:
    print("  " + " → ".join(path))
else:
    print("  경로 없음")

# 5. 지식그래프 서브그래프 (depth=1)
print(f"\n[5] '지식그래프' 노드 기준 직접 연결 (depth=1)")
sub = kg.subgraph("knowledge_graph", depth=1)
nodes = [f"{n.id}({n.label})" for n in sub.all_nodes() if n.id != "knowledge_graph"]
print("  노드: " + ", ".join(nodes))

# 6. RAG 서브그래프 (depth=1)
print(f"\n[6] 'RAG' 노드 기준 직접 연결 (depth=1)")
sub = kg.subgraph("rag", depth=1)
nodes = [f"{n.id}({n.label})" for n in sub.all_nodes() if n.id != "rag"]
print("  노드: " + ", ".join(nodes))

# 7. 세 패러다임 모두 포함하는 공통 허브 찾기
print(f"\n[7] 세 패러다임에서 모두 도달 가능한 공통 노드")
reachable = {}
for paradigm in ["ontology", "knowledge_graph", "rag"]:
    sub = kg.subgraph(paradigm, depth=4)
    reachable[paradigm] = {n.id for n in sub.all_nodes()}

common = reachable["ontology"] & reachable["knowledge_graph"] & reachable["rag"]
common -= {"ontology", "knowledge_graph", "rag"}
print("  " + ", ".join(sorted(common)))

# 8. 각 개념의 desc 출력 (경로 위 노드 설명)
print(f"\n[8] OWL → LLM 경로 위 개념 설명")
path = kg.find_path("owl", "llm")
if path:
    for node_id in path:
        node = kg.get_node(node_id)
        print(f"  [{node.label}] {node.properties['name']:15s} : {node.properties['desc']}")

print(f"\n{SEP}\n")
