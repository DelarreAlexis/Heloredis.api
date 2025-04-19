from typing import List
from aioredis import Redis
from pydantic import BaseModel


class GetAllKeysQuery(BaseModel):
    pass


async def handle_get_count_all_keys_query(
    query: GetAllKeysQuery, redis_client: Redis
) -> List[str]:
    return sorted(await redis_client.keys())
