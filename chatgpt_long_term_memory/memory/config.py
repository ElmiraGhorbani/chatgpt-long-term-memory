from pydantic import BaseModel, Field


class ChatMemoryConfig(BaseModel):
    redis_host: str = Field(default="172.16.0.2")
    redis_port: int = Field(default=6379)
