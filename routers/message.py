from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, Query
from core.mediator import mediator
from typing import List, Optional, Annotated
from applications.queries.messages.get_count_messages_by_key_query import (
    GetCountMessagesByKeyQuery,
)
from applications.queries.messages.get_messages_by_key_query import (
    GetMessagesByKeyQuery,
)
from applications.dtos.stream_message_dto import StreamMessageDto
from core.redis_client import get_redis

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/{redis_key}/count", response_model=int)
async def get_message_count(redis_key: str, redis_client: Redis = Depends(get_redis)):
    query = GetCountMessagesByKeyQuery(key=redis_key)
    try:
        return await mediator.send(query, redis_client=redis_client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{redis_key}", response_model=StreamMessageDto)
async def get_message(
    redis_key: str,
    page_size: Annotated[
        int, Query(ge=1, le=100, description="Nombre de messages par page (max 100)")
    ] = 10,
    next_id: Optional[str] = Query(
        None, description="ID du prochain message de la page suivante"
    ),
    redis_client: Redis = Depends(get_redis),
):
    query = GetMessagesByKeyQuery(
        key=redis_key, page_size=page_size, next_id=next_id, redis_client=redis_client
    )
    try:
        return await mediator.send(query, redis_client=redis_client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
