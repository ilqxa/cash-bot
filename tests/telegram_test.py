from bot.api_methods import getUpdates, sendMessage
from bot.api_objects import Update, Message, User, Chat
from bot.events import Unrecognised


def test_base():
    res = getUpdates()
    assert res.completed is not None


def test_send():
    msg = sendMessage(
        chat_id = -959684362,
        text = 'Тестовое сообщение от бота во время отладки'
    )
    assert True


def test_reactions():
    u = Update.parse_obj({'update_id': 843277026, 'message': {'message_id': 24, 'from': {'id': 101232786, 'is_bot': False, 'first_name': 'Ilia', 'last_name': 'Maystrenko', 'language_code': 'en'}, 'chat': {'id': -959684362, 'title': 'Тест', 'type': 'group', 'all_members_are_administrators': True}, 'date': 1677698202, 'text': 'Дашик #отправить 1337$RUB', 'entities': [{'offset': 6, 'length': 10, 'type': 'hashtag'}]}})
    for e in [Unrecognised]:
        if e.trying_by_template(u):
            event = e(update=u)
    assert True