from backend.services.reasoning_engine import ReasoningEngine


def reason_about(question, user_id=None):
    return ReasoningEngine().answer(question, user_id=user_id)
