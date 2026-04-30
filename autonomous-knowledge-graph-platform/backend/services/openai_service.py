from config.settings import Config


class OpenAIService:
    def __init__(self):
        self.enabled = bool(Config.OPENAI_API_KEY)

    def extract_entities(self, text):
        if not self.enabled:
            return []
        from openai import OpenAI
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        prompt = "Extract enterprise entities as JSON list with name,label,attributes from: " + text[:4000]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        return response.choices[0].message.content

    def answer(self, question, context):
        if not self.enabled:
            return None
        from openai import OpenAI
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Answer with concise enterprise reasoning and cite source names."},
                {"role": "user", "content": f"Question: {question}\nContext: {context[:6000]}"},
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
