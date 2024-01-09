from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import flags
from aiogram.fsm.context import FSMContext
import utils
from states import Gen
import tickers_library

import kb
import text

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)

@router.message(F.text == "Menu")
@router.message(F.text == "Main menu")
@router.message(F.text == "◀️ Main menu")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "fin_stat")
async def input_company_ticker_fs(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Choose the financial statement", reply_markup=kb.finstat_choice)


@router.callback_query(F.data == "income statement")
async def ingest_stat_is(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text.gen_ticker_fs)
    await state.set_state(Gen.stat_prompt)
    await state.update_data(statement="income-statement/")
    await callback_query.message.answer(text.gen_exit_itermediate, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "cash flow")
async def ingest_stat_cf(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text.gen_ticker_fs)
    await state.set_state(Gen.stat_prompt)
    await state.update_data(statement="cash-flow-statement/")
    await callback_query.message.answer(text.gen_exit_itermediate, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "balance sheet")
async def ingest_stat_bsh(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(text.gen_ticker_fs)
    await state.set_state(Gen.stat_prompt)
    await state.update_data(statement="balance-sheet-statement/")
    await callback_query.message.answer(text.gen_exit_itermediate, reply_markup=kb.exit_kb)


@router.message(Gen.stat_prompt)
@flags.chat_action("typing")
async def get_statement(msg: Message, state: FSMContext):
    mesg = await msg.answer(text.gen_wait)
    try:
        company = msg.text
        statement = (await state.get_data())['statement']
        print(statement)
        starter = 'https://financialmodelingprep.com/api/v3/'
        closer = '?apikey=7dd2f065517ca2bb8ca040cf3303e50f'
        final = starter + statement + company + closer
        api_url = final
        res = await utils.get_statement_func(api_url)
        res = res[0]
        counter = 0
        result = []
        for key in res:
            a = str(key) + " : " + str(res[key])
            result.append(a)
            counter += 1
        await mesg.answer("\n".join(result))
        await mesg.answer(text.gen_exit, reply_markup=kb.exit_kb)
    except Exception:
        return await mesg.answer(text.gen_error, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "st_price")
async def input_company_ticker_stp(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Gen.price_prompt)
    await callback_query.message.edit_text(text.gen_ticker_stp)
    await callback_query.message.answer(text.gen_exit_itermediate, reply_markup=kb.exit_kb)

@router.message(Gen.price_prompt)
@flags.chat_action("typing")
async def get_stock_price(msg: Message, state: FSMContext):
    mesg = await msg.answer(text.gen_wait)
    try:
        company = msg.text
        starter = 'https://financialmodelingprep.com/api/v3/stock-price-change/'
        closer = '?apikey=7dd2f065517ca2bb8ca040cf3303e50f'
        url = starter + company + closer
        res = await utils.get_stock_price_func(url)
        res = res[0]
        result = []
        for key in res:
            a = str(key) + " : " + str(res[key])
            result.append(a)
        await mesg.answer("\n".join(result))
        await mesg.answer(text.gen_exit, reply_markup=kb.exit_kb)
    except Exception:
        return await mesg.answer(text.gen_error, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "st_news")
async def input_company_ticker_news(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Gen.news_prompt)
    await callback_query.message.edit_text(text.gen_ticker_news)
    await callback_query.message.answer(text.gen_exit_itermediate, reply_markup=kb.exit_kb)

@router.message(Gen.news_prompt)
@flags.chat_action("typing")
async def send_news(msg: Message, state: FSMContext):
    mesg = await msg.answer(text.gen_wait)
    try:
        company = msg.text
        url = "https://real-time-finance-data.p.rapidapi.com/stock-news"
        res = await utils.send_news_func(url, company)
        parcer1 = res['data']
        parcer2 = parcer1['news']
        parcer3 = parcer2[0]
        news = parcer3['article_title']
        link = parcer3['article_url']
        source = parcer3['source']
        time = parcer3['post_time_utc']
        await mesg.answer(f'{news}, access article via link: {link}, source and time: {source}, {time} ')
        await mesg.answer(text.gen_exit, reply_markup=kb.exit_kb)
    except Exception:
        return await mesg.answer(text.gen_error, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "ticker_libr")
async def tickers_provide(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Gen.library)
    await callback_query.message.answer(tickers_library.library, reply_markup=kb.exit_kb)


@router.callback_query(F.data == "help")
async def helper(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Gen.helpme)
    await callback_query.message.answer(text.help, reply_markup=kb.exit_kb)