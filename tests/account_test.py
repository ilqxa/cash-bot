from datetime import date

from src.account import Accounter
from src.storage import InMemoryKeeper


def test_base():
    kp = InMemoryKeeper()
    ac = Accounter(storage=kp)

    ac.new_transaction(date(2023, 3, 1), 1, 2, 10)

    trs = ac.get_personal_balance_on_date(1, date(2023, 3, 2))
    rep = ac.make_personal_report(1, trs)
    assert rep['Сумма'].sum() == 10

    trs = ac.get_personal_balance_on_date(2, date(2023, 3, 2))
    rep = ac.make_personal_report(2, trs)
    assert rep['Сумма'].sum() == -10