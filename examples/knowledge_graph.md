# 온톨로지 · 지식그래프 · RAG 지식 구조

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

```mermaid
flowchart LR
    classDef Paradigm fill:#4A90D9,color:#fff,stroke:#2c6fad
    classDef Concept fill:#27AE60,color:#fff,stroke:#1e8449
    classDef Standard fill:#E67E22,color:#fff,stroke:#ca6f1e
    classDef Tool fill:#8E44AD,color:#fff,stroke:#6c3483
    classDef Component fill:#C0392B,color:#fff,stroke:#922b21

    ontology["온톨로지"]:::Paradigm
    knowledge_graph["지식그래프"]:::Paradigm
    rag["RAG"]:::Paradigm
    triple["Triple"]:::Concept
    class["Class"]:::Concept
    property["Property"]:::Concept
    instance["Instance"]:::Concept
    inference["Inference"]:::Concept
    entity["Entity"]:::Concept
    relation["Relation"]:::Concept
    embedding["Embedding"]:::Concept
    chunk["Chunk"]:::Concept
    context["Context"]:::Concept
    query["Query"]:::Concept
    rdf["RDF"]:::Standard
    owl["OWL"]:::Standard
    sparql["SPARQL"]:::Standard
    cypher["Cypher"]:::Standard
    neo4j["Neo4j"]:::Tool
    protege["Protégé"]:::Tool
    weaviate["Weaviate"]:::Tool
    chromadb["ChromaDB"]:::Tool
    llamaindex["LlamaIndex"]:::Tool
    vector_db["Vector DB"]:::Component
    retriever["Retriever"]:::Component
    llm["LLM"]:::Component
    encoder["Encoder"]:::Component

    ontology -->|CONTAINS| triple
    ontology -->|CONTAINS| class
    ontology -->|CONTAINS| property
    ontology -->|CONTAINS| instance
    ontology -->|ENABLES| inference
    ontology -->|USES| rdf
    ontology -->|USES| owl
    owl -->|EXTENDS| rdf
    ontology -->|USES| protege
    class -->|CONTAINS| instance
    property -->|FEEDS_INTO| triple
    knowledge_graph -->|CONTAINS| entity
    knowledge_graph -->|CONTAINS| relation
    knowledge_graph -->|STORED_IN| triple
    knowledge_graph -->|USES| ontology
    knowledge_graph -->|QUERIES| sparql
    knowledge_graph -->|QUERIES| cypher
    knowledge_graph -->|STORED_IN| neo4j
    entity -->|FEEDS_INTO| embedding
    rdf -->|USES| triple
    sparql -->|QUERIES| rdf
    cypher -->|QUERIES| neo4j
    rag -->|CONTAINS| chunk
    rag -->|USES| embedding
    rag -->|USES| vector_db
    rag -->|CONTAINS| retriever
    rag -->|USES| llm
    rag -->|FEEDS_INTO| context
    chunk -->|FEEDS_INTO| embedding
    embedding -->|STORED_IN| vector_db
    query -->|FEEDS_INTO| retriever
    retriever -->|QUERIES| vector_db
    retriever -->|FEEDS_INTO| context
    context -->|FEEDS_INTO| llm
    encoder -->|ENABLES| embedding
    weaviate -->|CONTAINS| vector_db
    chromadb -->|CONTAINS| vector_db
    llamaindex -->|USES| retriever
    llamaindex -->|ENABLES| rag
    knowledge_graph -->|FEEDS_INTO| rag
    ontology -->|ENABLES| knowledge_graph
    knowledge_graph -->|FEEDS_INTO| embedding
    ontology -->|FEEDS_INTO| rag
    sparql -->|ENABLES| retriever
    owl -->|ENABLES| knowledge_graph
    triple -->|FEEDS_INTO| knowledge_graph
    inference -->|ENABLES| knowledge_graph
    inference -->|ENABLES| rag
```
