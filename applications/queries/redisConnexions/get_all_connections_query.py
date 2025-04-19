from typing import List
from aioredis import Redis
from pydantic import BaseModel
from sqlmodel import Session, select

from applications.dtos.redis_connexion_dto import RedisConnectionDto
from domain.entities.redis_connection import RedisConnection


class GetAllConnectionsQuery(BaseModel):
    pass


async def handle_get_all_connections_query(
    query: GetAllConnectionsQuery, session: Session
) -> List[RedisConnectionDto]:
    statement = select(RedisConnection)
    results = session.exec(statement)
    redisConnections = results.all()

    redisConnectionDtos = []
    for redisConnection in redisConnections:
        redisConnectionDtos.append(
            RedisConnectionDto(
                id=redisConnection.id,
                name=redisConnection.name,
                url=redisConnection.url,
            )
        )
    return redisConnectionDtos
