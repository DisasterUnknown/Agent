import re
import math
from openai import OpenAI
from config.load_config import CONFIG

client = OpenAI(
    api_key=CONFIG.get("api_keys", "reward_model"),
    base_url=CONFIG.get("model_url", "reward_model")
)

class NemotronRewardModel:
    def __init__(self):
        self.client = client

    def score(self, prompt: str) -> float:
        completion = self.client.chat.completions.create(
            model=CONFIG.get("models", "reward_model"    ),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10,
        )

        raw = completion.choices[0].message.content.strip().lower()
        match = re.search(r"-?\d+\.?\d*", raw)

        if not match:
            return 0.0

        reward = float(match.group())
        normalized = 1 / (1 + math.exp(-reward / 5))

        return normalized