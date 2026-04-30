from backend.services.nlp_service import extract_entities


def test_rule_based_entity_extraction():
    entities = extract_entities("Atlas Logistics has 14% delay risk for Orion Cloud.")
    assert any(entity["label"] == "Risk" for entity in entities)
    assert any(entity["label"] == "Metric" for entity in entities)
