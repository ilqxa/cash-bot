import time
from abc import ABC, abstractmethod

from pydantic import BaseModel


class Transaction(BaseModel):
    id: int
    created_ts: int = int(time.time())
    updated_ts: int = int(time.time())
    reporting_ts: int
    sender_id: int
    recipient_id: int
    amount: float
    comment: str | None


class Keeper(BaseModel, ABC):

    @abstractmethod
    def get_last_id(self) -> int:
        ...

    @abstractmethod
    def write_transaction(
        self,
        tr: Transaction,
    ) -> None:
        ...

    @abstractmethod
    def del_transaction(
        self,
        tr: Transaction,
    ) -> None:
        ...

    @abstractmethod
    def find_transactions(
        self,
        id: int | None = None,
        reporting_ts_from: int | None = None,
        reporting_ts_to: int | None = None,
        sender_id: int | None = None,
        recipient_id: int | None = None,
        amount_from: float | None = None,
        amount_to: float | None = None,
    ) -> list[Transaction]:
        ...


class InMemoryKeeper(Keeper):
    transactions: list[Transaction] = []

    def get_last_id(self) -> int:
        if len(self.transactions) == 0: return 0
        else: return max([t.id for t in self.transactions])

    def write_transaction(
        self,
        tr: Transaction,
    ) -> None:
        self.transactions.append(tr)

    def del_transaction(
        self,
        tr: Transaction,
    ) -> None:
        self.transactions.remove(tr)

    def find_transactions(
        self,
        id: int | None = None,
        reporting_ts_from: int | None = None,
        reporting_ts_to: int | None = None,
        sender_id: int | None = None,
        recipient_id: int | None = None,
        amount_from: float | None = None,
        amount_to: float | None = None,
    ) -> list[Transaction]:
        res = []
        for t in self.transactions:
            if (
                (id is None or t.id == id) and
                (reporting_ts_from is None or t.reporting_ts >= reporting_ts_from) and
                (reporting_ts_to is None or t.reporting_ts <= reporting_ts_to) and
                (sender_id is None or t.sender_id == sender_id) and
                (recipient_id is None or t.recipient_id == recipient_id) and
                (amount_from is None or t.amount >= amount_from) and
                (amount_to is None or t.amount <= amount_to)
            ): res.append(t)
        return res