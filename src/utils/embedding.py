from config.load_config import CONFIG
from src.models.nv_embed_v1 import NvidiaEmbedding

def get_embedding_instance():
    return NvidiaEmbedding()