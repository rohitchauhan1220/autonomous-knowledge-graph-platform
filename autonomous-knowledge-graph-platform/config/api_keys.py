from config.settings import Config


def ai_keys_configured():
    return {
        "openai": bool(Config.OPENAI_API_KEY),
        "gemini": bool(Config.GEMINI_API_KEY),
        "neo4j": bool(Config.NEO4J_PASSWORD),
    }
