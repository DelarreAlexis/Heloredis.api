from sqlmodel import SQLModel, Field


class RedisConnection(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    url: str = Field(index=True)
