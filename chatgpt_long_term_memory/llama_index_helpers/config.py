from pydantic import BaseModel


class IndexConfig(BaseModel):
    root_path: str = ""
    knowledge_base: bool = True
    model_name: str = "gpt-3.5-turbo"
    temperature: int = 0
    context_window: int = 4096
    num_outputs: int = 700
    max_chunk_overlap: float = 0.5
    chunk_size_limit: int = 600


class RetrieversConfig(BaseModel):
    top_k: int = 3
    similarity_threshold: float = 0.7
