from abc import ABC, abstractmethod

from pydantic import BaseModel


class Event(BaseModel):
    ...


class Unrecognised(Event):
    ...


class NewTransaction(Event):
    ...


class RequestBalance(Event):
    ...