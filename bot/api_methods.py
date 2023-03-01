import time
from abc import ABC, abstractmethod
from typing import Any
import json

import requests
from requests import Response
from pydantic import BaseModel

from bot.api_objects import ApiObject, Update
from conf.api_telegram import TelegramBot


class Request(BaseModel):
    method: str
    obj: ApiObject | None = None
    conf = TelegramBot() # type: ignore
    completed: int | None = None
    response: Response | None = None

    def __init__(self, **data) -> None:
        super().__init__(**data)
        with requests.Session() as session:
            self.response = session.post(self.conf.url + self.method, json=self.obj, headers=self.conf.headers)
        self.completed = int(time.time())

    class Config:
        arbitrary_types_allowed = True
        post_init_call = 'after_validatiton'


class getUpdates(Request):
    method: str = '/getUpdates'
    offset: int | None = None
    limit: int = 100
    timeout: int = 0
    allowed_updates: list | str = 'chat_member'

    @property
    def result(self) -> list[Update]:
        res: list[Update] = []
        if self.response is None or self.response.status_code != 200: return res
        updates: list = json.loads(self.response.content.decode('utf-8'))['result']
        for u in updates:
            res.append(Update(**u))
        return res