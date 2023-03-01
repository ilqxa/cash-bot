import time

from src.storage import *


def test_base():
    keeper = InMemoryKeeper()
    tr1 = Transaction(
        id = 0,
        reporting_ts = int(time.time()),
        sender_id = 1,
        recipient_id = 2,
        amount = 10.,
    )
    keeper.write_transaction(tr1)
    assert len(keeper.transactions) == 1
    res = keeper.find_transactions(id = 0)
    assert len(res) == 1 and res[0] is tr1