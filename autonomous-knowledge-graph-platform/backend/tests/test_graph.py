from backend.models.graph_model import GraphSnapshot


def test_graph_snapshot_shape():
    snapshot = GraphSnapshot(nodes=[{"id": "1"}], edges=[], version=2)
    assert snapshot.to_dict()["version"] == 2
    assert len(snapshot.to_dict()["nodes"]) == 1
