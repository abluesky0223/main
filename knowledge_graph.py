"""
인메모리 지식 그래프 (Knowledge Graph)

사람의 사고방식처럼 "엔티티(노드)"와 "관계(엣지)"로 지식을 표현합니다.
예시:
    - Alice --[KNOWS]--> Bob
    - Bob --[WORKS_AT]--> Google
    - Google --[LOCATED_IN]--> SiliconValley
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Optional


class NodeNotFoundError(Exception):
    """존재하지 않는 노드에 접근할 때 발생합니다."""


class EdgeNotFoundError(Exception):
    """존재하지 않는 엣지에 접근할 때 발생합니다."""


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


class KnowledgeGraph:
    """인메모리 지식 그래프.

    노드(엔티티)와 엣지(관계)를 저장하고, 탐색 및 쿼리 기능을 제공합니다.

    사용 예시:
        kg = KnowledgeGraph()
        kg.add_node("alice", "Person", name="Alice", age=30)
        kg.add_node("bob", "Person", name="Bob")
        kg.add_edge("alice", "bob", "KNOWS", since=2020)
        kg.neighbors("alice")  # [Node("bob", ...)]
        kg.find_path("alice", "bob")  # ["alice", "bob"]
    """

    def __init__(self) -> None:
        self._nodes: dict[str, Node] = {}
        self._edges: list[Edge] = []

    # ------------------------------------------------------------------ #
    #  노드 CRUD                                                           #
    # ------------------------------------------------------------------ #

    def add_node(self, id: str, label: str, **properties) -> Node:
        """노드를 추가합니다. 동일한 id가 있으면 덮어씁니다."""
        node = Node(id=id, label=label, properties=properties)
        self._nodes[id] = node
        return node

    def get_node(self, id: str) -> Node:
        """id로 노드를 가져옵니다.

        Raises:
            NodeNotFoundError: 해당 id의 노드가 없을 때
        """
        if id not in self._nodes:
            raise NodeNotFoundError(f"노드를 찾을 수 없습니다: {id!r}")
        return self._nodes[id]

    def update_node(self, id: str, **properties) -> Node:
        """노드의 속성을 부분 업데이트합니다.

        Raises:
            NodeNotFoundError: 해당 id의 노드가 없을 때
        """
        node = self.get_node(id)
        node.properties.update(properties)
        return node

    def remove_node(self, id: str) -> None:
        """노드와 그 노드에 연결된 모든 엣지를 삭제합니다.

        Raises:
            NodeNotFoundError: 해당 id의 노드가 없을 때
        """
        self.get_node(id)  # 존재 확인
        self._nodes.pop(id)
        self._edges = [
            e for e in self._edges if e.source != id and e.target != id
        ]

    def all_nodes(self) -> list[Node]:
        """모든 노드를 반환합니다."""
        return list(self._nodes.values())

    def nodes_by_label(self, label: str) -> list[Node]:
        """특정 label의 노드를 모두 반환합니다."""
        return [n for n in self._nodes.values() if n.label == label]

    # ------------------------------------------------------------------ #
    #  엣지 CRUD                                                           #
    # ------------------------------------------------------------------ #

    def add_edge(self, source: str, target: str, relation: str, **properties) -> Edge:
        """두 노드 사이에 관계(엣지)를 추가합니다.

        Raises:
            NodeNotFoundError: source 또는 target 노드가 없을 때
        """
        self.get_node(source)  # source 존재 확인
        self.get_node(target)  # target 존재 확인
        edge = Edge(source=source, target=target, relation=relation, properties=properties)
        self._edges.append(edge)
        return edge

    def get_edges(
        self,
        source: Optional[str] = None,
        target: Optional[str] = None,
        relation: Optional[str] = None,
    ) -> list[Edge]:
        """조건에 맞는 엣지를 반환합니다. 조건을 생략하면 모든 엣지를 반환합니다."""
        result = self._edges
        if source is not None:
            result = [e for e in result if e.source == source]
        if target is not None:
            result = [e for e in result if e.target == target]
        if relation is not None:
            result = [e for e in result if e.relation == relation]
        return result

    def remove_edge(self, source: str, target: str, relation: str) -> None:
        """특정 엣지를 삭제합니다.

        Raises:
            EdgeNotFoundError: 해당 엣지가 없을 때
        """
        before = len(self._edges)
        self._edges = [
            e for e in self._edges
            if not (e.source == source and e.target == target and e.relation == relation)
        ]
        if len(self._edges) == before:
            raise EdgeNotFoundError(
                f"엣지를 찾을 수 없습니다: {source!r} --[{relation}]--> {target!r}"
            )

    # ------------------------------------------------------------------ #
    #  그래프 탐색                                                          #
    # ------------------------------------------------------------------ #

    def neighbors(self, id: str, relation: Optional[str] = None) -> list[Node]:
        """해당 노드에서 직접 연결된 이웃 노드들을 반환합니다.

        Args:
            id: 출발 노드 id
            relation: 특정 관계 타입만 필터링 (생략 시 모든 관계)

        Raises:
            NodeNotFoundError: 해당 id의 노드가 없을 때
        """
        self.get_node(id)  # 존재 확인
        edges = self.get_edges(source=id, relation=relation)
        seen: set[str] = set()
        result: list[Node] = []
        for e in edges:
            if e.target not in seen:
                seen.add(e.target)
                result.append(self._nodes[e.target])
        return result

    def find_path(self, start: str, end: str) -> Optional[list[str]]:
        """BFS로 start → end 최단 경로를 찾습니다.

        Returns:
            노드 id 목록 (start 포함, end 포함).
            경로가 없으면 None을 반환합니다.

        Raises:
            NodeNotFoundError: start 또는 end 노드가 없을 때
        """
        self.get_node(start)
        self.get_node(end)

        if start == end:
            return [start]

        visited: set[str] = {start}
        queue: deque[list[str]] = deque([[start]])

        while queue:
            path = queue.popleft()
            current = path[-1]
            for edge in self.get_edges(source=current):
                neighbor = edge.target
                if neighbor == end:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        return None  # 경로 없음

    def subgraph(self, root: str, depth: int = 2) -> "KnowledgeGraph":
        """root에서 depth 깊이까지 BFS로 탐색한 부분 그래프를 반환합니다.

        Args:
            root: 탐색 시작 노드 id
            depth: 탐색 깊이 (기본값: 2)

        Raises:
            NodeNotFoundError: root 노드가 없을 때
        """
        self.get_node(root)

        visited: dict[str, int] = {root: 0}  # id → 탐색 깊이
        queue: deque[tuple[str, int]] = deque([(root, 0)])

        while queue:
            current, current_depth = queue.popleft()
            if current_depth >= depth:
                continue
            for edge in self.get_edges(source=current):
                neighbor = edge.target
                if neighbor not in visited:
                    visited[neighbor] = current_depth + 1
                    queue.append((neighbor, current_depth + 1))

        sub = KnowledgeGraph()
        for node_id in visited:
            node = self._nodes[node_id]
            sub._nodes[node_id] = node

        for edge in self._edges:
            if edge.source in visited and edge.target in visited:
                sub._edges.append(edge)

        return sub

    # ------------------------------------------------------------------ #
    #  유틸리티                                                             #
    # ------------------------------------------------------------------ #

    def __len__(self) -> int:
        return len(self._nodes)

    def __repr__(self) -> str:
        return (
            f"KnowledgeGraph("
            f"nodes={len(self._nodes)}, edges={len(self._edges)})"
        )
