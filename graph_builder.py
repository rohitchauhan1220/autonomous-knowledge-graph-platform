from database import graph
from py2neo import Node, Relationship

def process_text(text):
    print("TEXT:", text)

    # HARD-CODED TEST (ignore AI for now)
    a = Node("Person", name="Elon Musk")
    b = Node("Company", name="SpaceX")

    rel = Relationship(a, "FOUNDED", b)

    graph.create(a)
    graph.create(b)
    graph.create(rel)

    print("DATA INSERTED")