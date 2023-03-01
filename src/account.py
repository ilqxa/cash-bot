import time
from datetime import date, datetime

import pandas as pd
from pydantic import BaseModel

from src.storage import Keeper, Transaction


class Accounter(BaseModel):
    storage: Keeper

    def new_transaction(
        self,
        reporting_date: date | datetime,
        sender_id: int,
        recipient_id: int,
        amount: float,
        comment: str | None = None,
    ) -> None:
        id_new = self.storage.get_last_id() + 1
        reporting_ts = int(time.mktime(reporting_date.timetuple()))
        tr = Transaction(
            id = id_new,
            reporting_ts = reporting_ts,
            sender_id = sender_id,
            recipient_id = recipient_id,
            amount = amount,
            comment = comment,
        )
        self.storage.write_transaction(tr)

    def get_personal_balance_on_date(
        self,
        person_id: int,
        reporting_date: date,
    ) -> None:
        ts_to = int(time.mktime(reporting_date.timetuple())) - 1
        debts = self.storage.find_transactions(sender_id=person_id, reporting_ts_to=ts_to)
        creds = self.storage.find_transactions(recipient_id=person_id, reporting_ts_to=ts_to)
        return debts + creds

    def get_personal_transactions_by_period(
        self,
        person_id: int,
        date_from: date,
        date_to: date,
    ) -> list[Transaction]:
        ts_from = int(time.mktime(date_from.timetuple()))
        ts_to = int(time.mktime(date_to.timetuple())) + 24*60*60 - 1
        debts = self.storage.find_transactions(sender_id=person_id, reporting_ts_from=ts_from, reporting_ts_to=ts_to)
        creds = self.storage.find_transactions(recipient_id=person_id, reporting_ts_from=ts_from, reporting_ts_to=ts_to)
        return debts + creds
    
    def make_personal_report(
        self,
        person_id: int,
        trs: list[Transaction],
    ) -> pd.DataFrame:
        res = pd.DataFrame([t.dict() for t in trs])
        res = res[(res['sender_id'] == person_id) | (res['recipient_id'] == person_id)]
        res['reporting_date'] = pd.to_datetime(res['reporting_ts'], unit='s', utc=True).dt.tz_convert('Europe/Moscow').dt.date
        res['amount'] = res.apply(lambda s: s['amount'] if s['sender_id'] == person_id else -s['amount'], axis=1)
        res['partner_id'] = res.apply(lambda s: s['recipient_id'] if s['sender_id'] == person_id else s['recipient_id'], axis=1)
        res = res.sort_values(by='reporting_ts')
        # res = res.drop(columns=['id', 'created_ts', 'updated_ts', 'reporting_ts', 'sender_id', 'recipient_id'])
        res = res[['partner_id', 'reporting_date', 'amount', 'comment']]
        res = res.rename(columns={
            'reporting_date': 'Дата операции',
            'partner_id': 'Партнер',
            'amount': 'Сумма',
            'comment': 'Примечание',
        })
        return res