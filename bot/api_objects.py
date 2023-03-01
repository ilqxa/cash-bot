from __future__ import annotations

from abc import ABC

from pydantic import BaseModel


class ApiObject(BaseModel, ABC):
    ...

class Update(ApiObject):
    update_id: int
    message: Message | None


class Message(ApiObject):
    message_id: int
    chat: Chat
    text: str | None


class Chat(ApiObject):
    id: int


Update.update_forward_refs()
Message.update_forward_refs()
Chat.update_forward_refs()