import time
from abc import ABC, abstractmethod
from typing import Any

import aiohttp
import requests
from requests import Response
from aiohttp import ClientResponse
from pydantic import BaseModel

from bot.api_objects import ApiObject
from conf.api_telegram import TelegramBot


class Request(BaseModel):
    method: str
    obj: ApiObject | None = None
    conf = TelegramBot() # type: ignore
    completed: int | None = None
    result: ClientResponse | Response | None = None

    # async def __post_init_post_parse__(self) -> Any:
    #     async with aiohttp.ClientSession() as session:
    #         self.result = await session.post(self.conf.url + self.method, json=self.obj, headers=self.conf.headers)
    #     self.completed = int(time.time())

    def __post_init__(self) -> Any:
        with requests.Session() as session:
            self.result = session.post(self.conf.url + self.method, json=self.obj, headers=self.conf.headers)
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