from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Node:
    """지식 그래프의 엔티티(개체)를 나타냅니다.

    Attributes:
        id: 고유 식별자. 예: "alice", "google"
        label: 엔티티 종류. 예: "Person", "Company", "City"
        properties: 엔티티의 속성. 예: {"name": "Alice", "age": 30}
    """

    id: str
    label: str
    properties: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Node({self.id!r}, label={self.label!r}, props={self.properties})"


@dataclass
class Edge:
    """두 노드 사이의 관계를 나타냅니다.

    Attributes:
        source: 출발 노드 id
        target: 도착 노드 id
        relation: 관계 종류. 예: "KNOWS", "WORKS_AT", "LOCATED_IN"
        properties: 관계의 속성. 예: {"since": 2020, "weight": 0.8}
    """

    source: str
    target: str
    relation: str
    properties: dict = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"Edge({self.source!r} --[{self.relation}]--> {self.target!r})"
