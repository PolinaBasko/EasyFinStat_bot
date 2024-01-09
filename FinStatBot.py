import telebot
import requests
from telebot import types

token = "6509565077:AAF-rK3rigB9kyBmXER-ocvy-bugck3aR8I"


def run_EasyFin_bot(token: str) -> None:
    bot = telebot.TeleBot(token, parse_mode=None)

    data=[]
    @bot.message_handler(content_types=['text'])
    def get_company_name(message):
        if message.text == "/start":
            company = bot.send_message(message.chat.id, "Enter company name")
            bot.register_next_step_handler(company, get_finstat)

    def get_finstat(message):
        company=message.text
        data.append(company)
        keyboard = types.InlineKeyboardMarkup()
        key_is = types.InlineKeyboardButton(text='Income Statement', callback_data='income-statement/')
        keyboard.add(key_is, row_width=1)
        key_cf = types.InlineKeyboardButton(text='Cash Flow', callback_data='cash-flow-statement/')
        keyboard.add(key_cf, row_width=1)
        key_bsh = types.InlineKeyboardButton(text='Balance Sheet', callback_data='balance-sheet-statement/')
        keyboard.add(key_bsh, row_width=1)
        bot.send_message(message.from_user.id, "Hi! Please choose Financial Statement below", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            statement = call.data
            data.append(statement)
            limit = bot.send_message(message.chat.id, "Enter limit")
            bot.register_next_step_handler(limit, send_result, data)

    def send_result(message, data):
        limit=message.text
        company = data[0]
        limit = data[2]
        statement = data[1]
        starter = 'https://financialmodelingprep.com/api/v3/'
        closer = '?apikey=7dd2f065517ca2bb8ca040cf3303e50f'
        final = starter + statement + company + closer
        # url = 'https://financialmodelingprep.com/api/v3/income-statement/AAPL?apikey=7dd2f065517ca2bb8ca040cf3303e50f'
        url = final
        response = requests.get(url)
        response = response.json()
        response = response[0]

        counter = 0
        result = []
        for key in response:
            a = str(key) + " : " + str(response[key])
            result.append(a)
            counter += 1
            if counter == limit:
                break

        bot.send_message(message.chat.id, "\n".join(result))

    bot.infinity_polling()

run_EasyFin_bot(token)



