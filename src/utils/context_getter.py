import os
from langchain_chroma import Chroma
from src.utils.embedding import get_embedding_instance
from config.load_config import CONFIG

def get_context(user_prompt: str):
    embedding_func = get_embedding_instance()
    db = Chroma(persist_directory=CONFIG.get("paths", "db_dir"), embedding_function=embedding_func)

    results = db.similarity_search_with_score(user_prompt, k=8)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    return context_text, results