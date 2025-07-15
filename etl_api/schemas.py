# schemas.py

from pydantic import BaseModel
from datetime import date
from typing import List


class TopProduct(BaseModel):
    object_class: str
    mentions: int


class ChannelActivityItem(BaseModel):
    date: date
    message_count: int


class MessageResult(BaseModel):
    message_id: int
    channel_title: str
    message_text: str
    date: date
