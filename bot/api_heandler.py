from time import sleep

from pydantic import BaseModel

from bot.api_methods import getUpdates
from bot.api_objects import Update
from bot.events import Event, Unrecognised
from src.account import Accounter
from src.storage import Keeper


class MessageHandler(BaseModel):
    accounter: Accounter

    def start_long_pooling(self) -> None:
        while True:
            query = getUpdates()
            for u in query.result:
                self.update_handle(u)
            sleep(5)

    def set_webhook(self) -> None:
        pass

    def update_handle(self, u: Update) -> None:
        event = self.parse_event(u)

    def parse_event(self, u: Update) -> Event:
        return Unrecognised()