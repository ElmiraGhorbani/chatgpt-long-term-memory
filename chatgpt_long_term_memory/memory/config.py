from pydantic import BaseModel


class ChatMemoryConfig(BaseModel):
    redis_host: str = "172.16.0.2"
    redis_port: int = 6379
