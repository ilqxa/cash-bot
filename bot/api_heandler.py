from time import sleep

from pydantic import BaseModel

from bot.api_methods import getUpdates
from bot.api_objects import Update
from src.account import Accounter
from src.storage import Keeper


class LongPooling(BaseModel):
    accounter: Accounter

    def run(self) -> None:
        while True:
            query = getUpdates()
            for u in query.result:
                self.handle(u)
            sleep(5)

    def handle(self, u: Update) -> None:
        pass


class WebHook(BaseModel):
    ...