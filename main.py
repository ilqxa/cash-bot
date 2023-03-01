from bot.api_heandler import MessageHandler
from src.account import Accounter
from src.storage import InMemoryKeeper

if __name__ == '__main__':
    storage = InMemoryKeeper()
    accounter = Accounter(storage=storage)
    app = MessageHandler(accounter=accounter)

    app.start_long_pooling()