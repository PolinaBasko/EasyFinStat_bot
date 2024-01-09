from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    stat_prompt = State()
    price_prompt = State()
    news_prompt = State()
    library = State()
    helpme = State()


