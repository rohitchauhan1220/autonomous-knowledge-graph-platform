class GraphSnapshot:
    def __init__(self, nodes=None, edges=None, version=1):
        self.nodes = nodes or []
        self.edges = edges or []
        self.version = version

    def to_dict(self):
        return {"version": self.version, "nodes": self.nodes, "edges": self.edges}
