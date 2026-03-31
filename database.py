from py2neo import Graph




graph = Graph(
    "neo4j+s://cb211a67.databases.neo4j.io",
    auth=("neo4j", "your_password")
)


def create_graph(entity1, entity2, relation):
    query = f"""
    MERGE (a:Entity {{name: "{entity1}"}})
    MERGE (b:Entity {{name: "{entity2}"}})
    MERGE (a)-[:{relation}]->(b)
    """
    graph.run(query)