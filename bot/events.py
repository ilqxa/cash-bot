from abc import ABC, abstractmethod

from pydantic import BaseModel

from bot.api_objects import Update
from bot.api_methods import sendMessage


class Event(ABC, BaseModel):
    update: Update

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.react()

    @classmethod
    @abstractmethod
    def trying_by_template(cls, u: Update) -> bool:
        ...

    @abstractmethod
    def react(self) -> None:
        ...


class Unrecognised(Event):
    @classmethod
    def trying_by_template(cls, u: Update) -> bool:
        if u.message is not None: return True
        else: return False
    
    def react(self) -> None:
        if self.update.message is None: return
        r = sendMessage(
            chat_id = self.update.message.chat.id,
            text = 'Неизвестный запрос',
            reply_to_message_id = self.update.message.message_id,
        )


class NewTransaction(Event):
    @classmethod
    def trying_by_template(cls, u: Update) -> bool:
        if u.message is None or u.message.entities is None or u.message.text is None: return False
        for e in u.message.entities:
            if e.type == 'hashtag' and u.message.text[e.offset:e.offset+e.length] in ['#отправить', '#получить']:
                return True
        return False


class RequestBalance(Event):
    ...