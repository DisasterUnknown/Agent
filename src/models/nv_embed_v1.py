from openai import OpenAI
from config.load_config import CONFIG

client = OpenAI(
    api_key=CONFIG.get("api_keys", "embedding_model"),
    base_url=CONFIG.get("model_url", "embedding_model")
)

class NvidiaEmbedding:
    def __init__(self):
        self.client = client

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            input=texts,
            model=CONFIG.get("models", "embedding_model"),
            encoding_format="float",
            extra_body={"input_type": "passage", "truncate": "NONE"}
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            input=[text],
            model=CONFIG.get("models", "embedding_model"),
            encoding_format="float",
            extra_body={"input_type": "query", "truncate": "NONE"}
        )
        return [item.embedding for item in response.data][0]