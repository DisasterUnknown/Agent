from openai import OpenAI
from config.load_config import CONFIG

client = OpenAI(
    base_url=CONFIG.get("model_url", "chat_model"),
    api_key=CONFIG.get("api_keys", "chat_model")
)

class QwenChatLLM:
    def __init__(self):
        self.client = client

    def invoke(self, prompt: str) -> str:
        completion = self.client.chat.completions.create(
            model=CONFIG.get("models", "chat_model"),
            messages=[{"role": "system", "content": prompt}],
            temperature=CONFIG.get("hyperparameters", "temperature"),
            top_p=CONFIG.get("hyperparameters", "top_p"),
            max_tokens=CONFIG.get("hyperparameters", "max_tokens"),
        )
        return completion.choices[0].message.content