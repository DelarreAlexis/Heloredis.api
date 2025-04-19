import json
from aioredis import Redis
from pydantic import BaseModel
from typing import List, Annotated, Optional
from applications.dtos.stream_message_dto import StreamMessageDto, MessageDto
from fastapi import Query


class GetMessagesByKeyQuery(BaseModel):
    key: str
    page_size: int
    next_id: Optional[str]


async def handle_get_messages_by_key_query(
    query: GetMessagesByKeyQuery, redis_client: Redis
) -> StreamMessageDto:

    start_id = query.next_id if query.next_id else "+"
    messages = await redis_client.xrevrange(
        query.key, start_id, "-", query.page_size + 1
    )
    count = await redis_client.xlen(query.key)

    formatted_messages = []
    all_properties = []
    for message in messages:
        real_message = next(iter(message[1].values()))
        formatted_messages.append(MessageDto(id=message[0], data=real_message))

        data_json = json.loads(real_message)
        properties = list(data_json.keys())
        all_properties = list(set(all_properties) | set(properties))

    next_id = None
    if len(messages) > query.page_size:
        next_id = formatted_messages[-1].id
        formatted_messages = formatted_messages[: query.page_size]

    return StreamMessageDto(
        next_id=next_id,
        messages=formatted_messages,
        count=count,
        properties=sorted(all_properties),
    )
