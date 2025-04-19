from aioredis import Redis
from pydantic import BaseModel


class GetCountAllKeysQuery(BaseModel):
    pass


async def handle_get_count_all_keys_query(
    query: GetCountAllKeysQuery, redis_client: Redis
) -> int:
    return await redis_client.dbsize()
