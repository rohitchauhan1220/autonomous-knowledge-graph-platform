from neo4j import GraphDatabase
from config.settings import Config


class Neo4jConnector:
    def __init__(self):
        self.driver = None
        try:
            self.driver = GraphDatabase.driver(Config.NEO4J_URI, auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD))
        except Exception:
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def upsert_entity(self, name, label="Concept"):
        if not self.driver:
            return False
        with self.driver.session() as session:
            session.run("MERGE (e:Entity {name: $name}) SET e.label = $label", name=name, label=label)
        return True
