from contextlib import asynccontextmanager
import aioredis
from fastapi import Header
from aioredis import Redis


async def get_redis_connection(redis_url: str) -> Redis:
    redis = await aioredis.from_url(redis_url)
    try:
        pong = await redis.ping()
        if pong:
            print("Connexion à Redis réussie !")
        else:
            print("Connexion à Redis échouée.")
        return redis
    except Exception as e:
        print(f"Erreur de connexion à Redis : {e}")


async def get_redis(x_redis_name: str = Header(...)):
    try:
        redis = await get_redis_connection(x_redis_name)
        yield redis
    finally:
        await redis.close()
