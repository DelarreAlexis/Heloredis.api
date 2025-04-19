from pydantic import BaseModel
from typing import Dict, List, Optional


class MessageDto(BaseModel):
    id: str
    data: str


class StreamMessageDto(BaseModel):
    next_id: Optional[str]
    count: int
    properties: List[str]
    messages: List[MessageDto]
