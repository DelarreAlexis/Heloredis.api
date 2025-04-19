from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from core.mediator import mediator
from applications.queries.keys.get_count_all_keys_query import GetCountAllKeysQuery
from applications.queries.keys.get_all_keys_query import GetAllKeysQuery
from core.redis_client import get_redis

router = APIRouter(prefix="/keys", tags=["keys"])


@router.get("/count", response_model=int)
async def get_key_count():
    query = GetCountAllKeysQuery()
    try:
        return await mediator.send(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=List[str])
async def get_all_keys(redis_client: Redis = Depends(get_redis)):
    query = GetAllKeysQuery()
    try:
        return await mediator.send(query, redis_client=redis_client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
