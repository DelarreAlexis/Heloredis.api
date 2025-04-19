from pydantic import BaseModel
from sqlmodel import Session

from applications.dtos.redis_connexion_dto import RedisConnectionDto
from domain.entities.redis_connection import RedisConnection


class CreateRedisConnectionCommand(BaseModel):
    name: str
    url: str


async def handle_create_redis_connection_command(
    command: CreateRedisConnectionCommand, session: Session
) -> RedisConnectionDto:
    redisConnection = RedisConnection(name=command.name, url=command.url)
    session.add(redisConnection)
    session.commit()
    session.refresh(redisConnection)
    return RedisConnectionDto(
        id=redisConnection.id, name=redisConnection.name, url=redisConnection.url
    )
