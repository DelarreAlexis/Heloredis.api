from aioredis import Redis
from pydantic import BaseModel


class GetCountMessagesByKeyQuery(BaseModel):
    key: str


async def handle_get_count_messages_by_key_query(
    query: GetCountMessagesByKeyQuery, redis_client: Redis
) -> int:
    key_type = await redis_client.type(query.key)
    return await redis_client.xlen(query.key)
