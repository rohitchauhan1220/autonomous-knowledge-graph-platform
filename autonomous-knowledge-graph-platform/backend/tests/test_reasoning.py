from backend.services.reasoning_engine import ReasoningEngine


def test_offline_answer_no_docs():
    answer = ReasoningEngine()._offline_answer("missing", [])
    assert "No direct source matched" in answer
