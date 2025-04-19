from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session
from applications.commands.redisConnections.create_redis_connection_command import (
    CreateRedisConnectionCommand,
)
from applications.dtos.redis_connexion_dto import RedisConnectionDto
from applications.queries.redisConnexions.get_all_connections_query import (
    GetAllConnectionsQuery,
)
from core.database import SessionDep
from core.mediator import mediator


router = APIRouter(prefix="/redisConnection", tags=["redisConnection"])


@router.post("/")
async def create_redis_connection(
    session: Session = SessionDep,
    name: str = Body(None, description="Nom de la connexion Redis"),
    url: str = Body(None, description="Url de la connexion Redis"),
):
    command = CreateRedisConnectionCommand(
        name=name,
        url=url,
    )
    try:
        return await mediator.send(command, session=session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=List[RedisConnectionDto])
async def get_all_redis_connections(session: Session = SessionDep):
    query = GetAllConnectionsQuery()
    try:
        return await mediator.send(query, session=session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
