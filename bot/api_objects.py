from __future__ import annotations

from pydantic import BaseModel


class Update(BaseModel):
    update_id: int
    message: Message | None


class Message(BaseModel):
    message_id: int
    chat: Chat
    text: str | None


class Chat(BaseModel):
    id: int


Update.update_forward_refs()
Message.update_forward_refs()
Chat.update_forward_refs()