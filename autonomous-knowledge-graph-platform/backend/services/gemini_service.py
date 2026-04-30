from config.settings import Config


class GeminiService:
    def __init__(self):
        self.enabled = bool(Config.GEMINI_API_KEY)

    def generate_insight(self, question, context):
        if not self.enabled:
            return None
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Generate context-aware enterprise insight.\nQuestion: {question}\nContext: {context[:6000]}"
        )
        return response.text
