from openai import OpenAI
from config.load_config import CONFIG

client = OpenAI(
    base_url=CONFIG.get("model_url", "llm_model"),
    api_key=CONFIG.get("api_keys", "llm_model")
)

class NemotronLLM:
    def __init__(self):
        self.client = client

    def invoke(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=CONFIG.get("models", "llm_model"),
            messages=[{"role": "system", "content": prompt}],
            temperature=0.6,
            top_p=0.95,
            max_tokens=4096,
        )
        return completion.choices[0].message.content