from pydantic import BaseModel


class RedisConnectionDto(BaseModel):
    id: int
    name: str
    url: str
