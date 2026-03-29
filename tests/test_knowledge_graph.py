"""
지식 그래프 테스트

실제 사람의 사고방식처럼 구성된 시나리오를 바탕으로 테스트합니다.
  - 사람들이 서로를 알고 있다 (KNOWS)
  - 사람들이 회사에서 일한다 (WORKS_AT)
  - 회사는 도시에 위치한다 (LOCATED_IN)
"""

import pytest

from knowledge_graph import Edge, EdgeNotFoundError, KnowledgeGraph, Node, NodeNotFoundError


@pytest.fixture
def graph() -> KnowledgeGraph:
    """빈 지식 그래프를 반환합니다."""
    return KnowledgeGraph()


@pytest.fixture
def social_graph() -> KnowledgeGraph:
    """사람들의 인간관계와 직장 정보가 담긴 그래프입니다.

    Alice --[KNOWS]--> Bob --[KNOWS]--> Carol
      |                 |
      +--[KNOWS]------> Carol
    Bob --[WORKS_AT]--> Google
    Google --[LOCATED_IN]--> SiliconValley
    """
    kg = KnowledgeGraph()
    kg.add_node("alice", "Person", name="Alice", age=30)
    kg.add_node("bob", "Person", name="Bob", age=28)
    kg.add_node("carol", "Person", name="Carol", age=35)
    kg.add_node("google", "Company", name="Google", founded=1998)
    kg.add_node("silicon_valley", "City", name="Silicon Valley")

    kg.add_edge("alice", "bob", "KNOWS", since=2018)
    kg.add_edge("alice", "carol", "KNOWS", since=2020)
    kg.add_edge("bob", "carol", "KNOWS", since=2019)
    kg.add_edge("bob", "google", "WORKS_AT", role="Engineer")
    kg.add_edge("google", "silicon_valley", "LOCATED_IN")
    return kg


# ======================================================================
#  노드 CRUD
# ======================================================================


class TestNodeCreate:
    def test_add_node_returns_node(self, graph):
        node = graph.add_node("alice", "Person", name="Alice")
        assert isinstance(node, Node)
        assert node.id == "alice"
        assert node.label == "Person"
        assert node.properties["name"] == "Alice"

    def test_add_node_stores_multiple_properties(self, graph):
        graph.add_node("alice", "Person", name="Alice", age=30, city="Seoul")
        node = graph.get_node("alice")
        assert node.properties["age"] == 30
        assert node.properties["city"] == "Seoul"

    def test_add_node_with_same_id_overwrites(self, graph):
        graph.add_node("alice", "Person", name="Alice")
        graph.add_node("alice", "Person", name="Alice Updated")
        assert graph.get_node("alice").properties["name"] == "Alice Updated"

    def test_graph_size_increases_after_add(self, graph):
        assert len(graph) == 0
        graph.add_node("alice", "Person")
        assert len(graph) == 1
        graph.add_node("bob", "Person")
        assert len(graph) == 2


class TestNodeRead:
    def test_get_node_returns_correct_node(self, social_graph):
        alice = social_graph.get_node("alice")
        assert alice.id == "alice"
        assert alice.label == "Person"
        assert alice.properties["name"] == "Alice"

    def test_get_nonexistent_node_raises_error(self, graph):
        with pytest.raises(NodeNotFoundError, match="dave"):
            graph.get_node("dave")

    def test_nodes_by_label_returns_only_matching(self, social_graph):
        people = social_graph.nodes_by_label("Person")
        assert len(people) == 3
        assert all(n.label == "Person" for n in people)

    def test_nodes_by_label_returns_empty_for_unknown(self, social_graph):
        assert social_graph.nodes_by_label("Robot") == []

    def test_all_nodes_returns_every_node(self, social_graph):
        nodes = social_graph.all_nodes()
        assert len(nodes) == 5


class TestNodeUpdate:
    def test_update_node_changes_property(self, social_graph):
        social_graph.update_node("alice", age=31)
        assert social_graph.get_node("alice").properties["age"] == 31

    def test_update_node_does_not_remove_other_properties(self, social_graph):
        social_graph.update_node("alice", age=31)
        assert social_graph.get_node("alice").properties["name"] == "Alice"

    def test_update_node_adds_new_property(self, social_graph):
        social_graph.update_node("alice", email="alice@example.com")
        assert social_graph.get_node("alice").properties["email"] == "alice@example.com"

    def test_update_nonexistent_node_raises_error(self, graph):
        with pytest.raises(NodeNotFoundError):
            graph.update_node("nobody", age=99)


class TestNodeDelete:
    def test_remove_node_deletes_it(self, social_graph):
        social_graph.remove_node("carol")
        with pytest.raises(NodeNotFoundError):
            social_graph.get_node("carol")

    def test_remove_node_also_removes_connected_edges(self, social_graph):
        social_graph.remove_node("bob")
        # bob이 source 또는 target인 엣지가 모두 삭제되어야 함
        edges = social_graph.get_edges()
        assert all(e.source != "bob" and e.target != "bob" for e in edges)

    def test_remove_nonexistent_node_raises_error(self, graph):
        with pytest.raises(NodeNotFoundError):
            graph.remove_node("ghost")


# ======================================================================
#  엣지 CRUD
# ======================================================================


class TestEdgeCreate:
    def test_add_edge_returns_edge(self, graph):
        graph.add_node("alice", "Person")
        graph.add_node("bob", "Person")
        edge = graph.add_edge("alice", "bob", "KNOWS")
        assert isinstance(edge, Edge)
        assert edge.source == "alice"
        assert edge.target == "bob"
        assert edge.relation == "KNOWS"

    def test_add_edge_stores_properties(self, graph):
        graph.add_node("alice", "Person")
        graph.add_node("bob", "Person")
        graph.add_edge("alice", "bob", "KNOWS", since=2020, strength="strong")
        edges = graph.get_edges(source="alice")
        assert edges[0].properties["since"] == 2020
        assert edges[0].properties["strength"] == "strong"

    def test_add_edge_with_missing_source_raises_error(self, graph):
        graph.add_node("bob", "Person")
        with pytest.raises(NodeNotFoundError, match="alice"):
            graph.add_edge("alice", "bob", "KNOWS")

    def test_add_edge_with_missing_target_raises_error(self, graph):
        graph.add_node("alice", "Person")
        with pytest.raises(NodeNotFoundError, match="bob"):
            graph.add_edge("alice", "bob", "KNOWS")

    def test_can_add_self_loop(self, graph):
        graph.add_node("alice", "Person")
        edge = graph.add_edge("alice", "alice", "SELF_REF")
        assert edge.source == edge.target == "alice"


class TestEdgeRead:
    def test_get_edges_by_source(self, social_graph):
        edges = social_graph.get_edges(source="alice")
        assert len(edges) == 2
        assert all(e.source == "alice" for e in edges)

    def test_get_edges_by_target(self, social_graph):
        edges = social_graph.get_edges(target="carol")
        assert len(edges) == 2
        assert all(e.target == "carol" for e in edges)

    def test_get_edges_by_relation(self, social_graph):
        edges = social_graph.get_edges(relation="KNOWS")
        assert len(edges) == 3
        assert all(e.relation == "KNOWS" for e in edges)

    def test_get_edges_combined_filter(self, social_graph):
        edges = social_graph.get_edges(source="alice", relation="KNOWS")
        assert len(edges) == 2
        assert all(e.source == "alice" and e.relation == "KNOWS" for e in edges)

    def test_get_all_edges(self, social_graph):
        assert len(social_graph.get_edges()) == 5


class TestEdgeDelete:
    def test_remove_edge(self, social_graph):
        social_graph.remove_edge("alice", "bob", "KNOWS")
        edges = social_graph.get_edges(source="alice", target="bob")
        assert len(edges) == 0

    def test_remove_nonexistent_edge_raises_error(self, graph):
        graph.add_node("a", "Node")
        graph.add_node("b", "Node")
        with pytest.raises(EdgeNotFoundError):
            graph.remove_edge("a", "b", "FAKE")

    def test_other_edges_remain_after_remove(self, social_graph):
        social_graph.remove_edge("alice", "bob", "KNOWS")
        assert len(social_graph.get_edges(source="alice")) == 1  # carol과의 엣지는 남아있음


# ======================================================================
#  그래프 탐색
# ======================================================================


class TestNeighbors:
    def test_alice_knows_bob_and_carol(self, social_graph):
        neighbor_ids = {n.id for n in social_graph.neighbors("alice")}
        assert neighbor_ids == {"bob", "carol"}

    def test_neighbors_filtered_by_relation(self, social_graph):
        # bob의 KNOWS 관계 이웃만
        knows = social_graph.neighbors("bob", relation="KNOWS")
        assert len(knows) == 1
        assert knows[0].id == "carol"

    def test_neighbors_no_duplicate(self, graph):
        graph.add_node("a", "X")
        graph.add_node("b", "X")
        graph.add_edge("a", "b", "R1")
        graph.add_edge("a", "b", "R2")  # b로 가는 엣지 2개
        # b가 한 번만 나와야 함
        neighbors = graph.neighbors("a")
        assert len(neighbors) == 1
        assert neighbors[0].id == "b"

    def test_isolated_node_has_no_neighbors(self, graph):
        graph.add_node("alone", "Person")
        assert graph.neighbors("alone") == []


class TestFindPath:
    def test_direct_path(self, social_graph):
        path = social_graph.find_path("alice", "bob")
        assert path == ["alice", "bob"]

    def test_two_hop_path(self, social_graph):
        # alice → bob → google
        path = social_graph.find_path("alice", "google")
        assert path == ["alice", "bob", "google"]

    def test_three_hop_path(self, social_graph):
        # alice → bob → google → silicon_valley
        path = social_graph.find_path("alice", "silicon_valley")
        assert path == ["alice", "bob", "google", "silicon_valley"]

    def test_same_start_end_returns_single_node(self, social_graph):
        path = social_graph.find_path("alice", "alice")
        assert path == ["alice"]

    def test_no_path_returns_none(self, social_graph):
        # carol → alice 방향 엣지가 없으므로 경로 없음
        assert social_graph.find_path("carol", "google") is None

    def test_path_to_nonexistent_node_raises_error(self, social_graph):
        with pytest.raises(NodeNotFoundError):
            social_graph.find_path("alice", "mars")

    def test_bfs_finds_shortest_path(self, graph):
        """BFS가 최단 경로를 찾는지 확인합니다."""
        # a → b → d  (길이 2)
        # a → c → d  (길이 2)
        # a → d      (길이 1, 최단)
        for node_id in ["a", "b", "c", "d"]:
            graph.add_node(node_id, "X")
        graph.add_edge("a", "b", "R")
        graph.add_edge("b", "d", "R")
        graph.add_edge("a", "c", "R")
        graph.add_edge("c", "d", "R")
        graph.add_edge("a", "d", "R")
        path = graph.find_path("a", "d")
        assert path == ["a", "d"]  # 길이 1이 최단


class TestSubgraph:
    def test_subgraph_depth_1_includes_direct_neighbors(self, social_graph):
        sub = social_graph.subgraph("alice", depth=1)
        node_ids = {n.id for n in sub.all_nodes()}
        assert node_ids == {"alice", "bob", "carol"}

    def test_subgraph_depth_2_includes_two_hop_nodes(self, social_graph):
        sub = social_graph.subgraph("alice", depth=2)
        node_ids = {n.id for n in sub.all_nodes()}
        # alice(0) → bob(1), carol(1) → google(2), carol(1) (bob→carol은 1hop)
        assert "google" in node_ids

    def test_subgraph_only_includes_edges_within(self, social_graph):
        sub = social_graph.subgraph("alice", depth=1)
        # 서브그래프 내 노드 간의 엣지만 포함되어야 함
        node_ids = {n.id for n in sub.all_nodes()}
        for edge in sub.get_edges():
            assert edge.source in node_ids
            assert edge.target in node_ids

    def test_subgraph_depth_0_is_just_root(self, social_graph):
        sub = social_graph.subgraph("alice", depth=0)
        assert len(sub) == 1
        assert sub.get_node("alice").id == "alice"

    def test_subgraph_preserves_node_properties(self, social_graph):
        sub = social_graph.subgraph("alice", depth=1)
        assert sub.get_node("alice").properties["name"] == "Alice"


# ======================================================================
#  엣지 케이스 및 통합 시나리오
# ======================================================================


class TestIntegrationScenarios:
    def test_knowledge_chain(self, graph):
        """지식 체인: 한국 → 서울 → 강남 → 삼성역"""
        graph.add_node("korea", "Country", name="대한민국")
        graph.add_node("seoul", "City", name="서울")
        graph.add_node("gangnam", "District", name="강남구")
        graph.add_node("samsung_station", "Place", name="삼성역")

        graph.add_edge("korea", "seoul", "CONTAINS")
        graph.add_edge("seoul", "gangnam", "CONTAINS")
        graph.add_edge("gangnam", "samsung_station", "CONTAINS")

        path = graph.find_path("korea", "samsung_station")
        assert path == ["korea", "seoul", "gangnam", "samsung_station"]

    def test_repr_shows_node_and_edge_count(self, social_graph):
        r = repr(social_graph)
        assert "nodes=5" in r
        assert "edges=5" in r

    def test_empty_graph(self, graph):
        assert len(graph) == 0
        assert graph.all_nodes() == []
        assert graph.get_edges() == []
