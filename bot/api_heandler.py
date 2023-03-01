from time import sleep
from typing import Type

from pydantic import BaseModel

from bot.api_methods import getUpdates
from bot.api_objects import Update
from bot.events import Event, NewTransaction, Unrecognised
from src.account import Accounter
from src.storage import Keeper


class MessageHandler(BaseModel):
    accounter: Accounter
    events: list[Type[Event]] = [NewTransaction, Unrecognised] # type: ignore

    def start_long_pooling(self) -> None:
        while True:
            query = getUpdates()
            for u in query.result:
                self.update_handle(u)
            sleep(5)

    def set_webhook(self) -> None:
        pass

    def update_handle(self, u: Update) -> None:
        for e in self.events:
            if e.trying_by_template(u):
                event = e(update=u)
                continue