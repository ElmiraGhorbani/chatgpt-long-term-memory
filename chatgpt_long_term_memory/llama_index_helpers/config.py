from pydantic import BaseModel, Field


class IndexConfig(BaseModel):
    root_path: str = Field(
        default="")
    knowledge_base: bool = Field(default=True)
    model_name: str = Field(default="gpt-3.5-turbo")
    temperature: int = Field(default=0)
    context_window: int = Field(default=4096)
    num_outputs: int = Field(default=700)
    max_chunk_overlap: float = Field(default=0.5)
    chunk_size_limit: int = Field(default=600)


class RetrieversConfig(BaseModel):
    top_k: int = Field(default=7)
    max_tokens: int = Field(default=1000)
