from bot.api_methods import getUpdates


def test_base():
    res = getUpdates()
    assert res.completed is not None