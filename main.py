from fastapi import Depends, FastAPI
import uvicorn
from applications.commands.redisConnections.create_redis_connection_command import (
    CreateRedisConnectionCommand,
    handle_create_redis_connection_command,
)
from applications.queries.redisConnexions.get_all_connections_query import (
    GetAllConnectionsQuery,
    handle_get_all_connections_query,
)
from core.database import create_db_and_tables
from core.mediator import mediator
from contextlib import asynccontextmanager
from applications.queries.keys.get_count_all_keys_query import (
    GetCountAllKeysQuery,
    handle_get_count_all_keys_query,
)
from applications.queries.keys.get_all_keys_query import (
    GetAllKeysQuery,
    handle_get_count_all_keys_query,
)
from applications.queries.messages.get_count_messages_by_key_query import (
    GetCountMessagesByKeyQuery,
    handle_get_count_messages_by_key_query,
)
from applications.queries.messages.get_messages_by_key_query import (
    GetMessagesByKeyQuery,
    handle_get_messages_by_key_query,
)
from fastapi.middleware.cors import CORSMiddleware

from routers import key, redis_connection
from routers import message


async def lifespan(app: FastAPI):
    create_db_and_tables()

    mediator.register_handler(
        CreateRedisConnectionCommand, handle_create_redis_connection_command
    )
    mediator.register_handler(GetAllConnectionsQuery, handle_get_all_connections_query)

    mediator.register_handler(GetCountAllKeysQuery, handle_get_count_all_keys_query)
    mediator.register_handler(GetAllKeysQuery, handle_get_count_all_keys_query)

    mediator.register_handler(
        GetCountMessagesByKeyQuery, handle_get_count_messages_by_key_query
    )
    mediator.register_handler(GetMessagesByKeyQuery, handle_get_messages_by_key_query)

    yield


app = FastAPI(lifespan=lifespan, title="HeloRedis", version="0.0.1")

origins = ["http://localhost:5173", "https://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(key.router)
app.include_router(message.router)
app.include_router(redis_connection.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
