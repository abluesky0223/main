"""인메모리 지식 그래프 핵심 클래스.

사용 예시:
    kg = KnowledgeGraph()
    kg.add_node("alice", "Person", name="Alice", age=30)
    kg.add_node("bob", "Person", name="Bob")
    kg.add_edge("alice", "bob", "KNOWS", since=2020)
    kg.neighbors("alice")        # [Node("bob", ...)]
    kg.find_path("alice", "bob") # ["alice", "bob"]
"""

from __future__ import annotations

from collections import deque
from typing import Optional

from .exceptions import EdgeNotFoundError, NodeNotFoundError
from .models import Edge, Node


class KnowledgeGraph:
    """인메모리 지식 그래프.

    노드(엔티티)와 엣지(관계)를 저장하고 탐색 기능을 제공합니다.
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
        self.get_node(id)
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
        self.get_node(source)
        self.get_node(target)
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
        self.get_node(id)
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

        return None

    def subgraph(self, root: str, depth: int = 2) -> "KnowledgeGraph":
        """root에서 depth 깊이까지 BFS로 탐색한 부분 그래프를 반환합니다.

        Args:
            root: 탐색 시작 노드 id
            depth: 탐색 깊이 (기본값: 2)

        Raises:
            NodeNotFoundError: root 노드가 없을 때
        """
        self.get_node(root)

        visited: dict[str, int] = {root: 0}
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
            sub._nodes[node_id] = self._nodes[node_id]
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
        return f"KnowledgeGraph(nodes={len(self._nodes)}, edges={len(self._edges)})"
