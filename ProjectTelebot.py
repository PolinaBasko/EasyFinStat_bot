import telebot
import requests
from telebot import types
from constants import token
import logging


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

def run_EasyFin_bot(token: str) -> None:
    bot = telebot.TeleBot(token, parse_mode=None)

    data = []
    # initial commands handler. "Start" initiates the process and asks for company details, "help" explains the functionality
    @bot.message_handler(content_types=['text'])
    def get_company_name(message):
        if message.text == "/start":
            company = bot.send_message(message.from_user.id, "Hi! I'm EasyFinStat bot 🤖, trading and investment assistant. Let's check the latest finance statistics. Please, enter company stock ticker 📲 ")
            bot.register_next_step_handler(company, get_finstat)
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Hi! I'm EasyFinStat bot 🤖, trading and investment assistant. I can help you to obtain the latest finance statistics. Other than that, I can provide you with stock price change and show you the latest company news. In my reality you can use stock ticker instead of company name. Type /start to proceed.")
        else:
            bot.send_message(message.from_user.id, "Something went wrong. I don't get you 😔. Type /start or /help to proceed")

    # function gets type of statement from user, memorises company choice from previous step and sends these paramenters to the next step (send result)
    def get_finstat(message):
        company = message.text
        data.append(company)
        keyboard = types.InlineKeyboardMarkup()
        key_is = types.InlineKeyboardButton(text='📊 Income Statement', callback_data='income-statement/')
        keyboard.add(key_is, row_width=1)
        key_cf = types.InlineKeyboardButton(text='📈 Cash Flow', callback_data='cash-flow-statement/')
        keyboard.add(key_cf, row_width=1)
        key_bsh = types.InlineKeyboardButton(text='🧾 Balance Sheet', callback_data='balance-sheet-statement/')
        keyboard.add(key_bsh, row_width=1)
        bot.send_message(message.from_user.id, "Now please choose the Financial Statement", reply_markup=keyboard)

        # callback query handler works for 2 inline keyboards and sends to different steps depending from user choice
        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            print(data)
            print(call.data)
            #1st keyboard callback worker(type of financial statement)
            if call.data in ['income-statement/', 'cash-flow-statement/', 'balance-sheet-statement/']:
                statement = call.data
                data.append(statement)
                limit = bot.send_message(message.from_user.id, "Please limit number of statements")
                bot.register_next_step_handler(limit, send_result, data)
            #2nd keyboard callback worker (news, stock price change or finish)
            elif call.data == 'stock':
                company_new = bot.send_message(message.from_user.id, "Enter company name")
                bot.register_next_step_handler(company_new, send_stock_price, data)
                bot.register_next_step_handler(company_new, say_goodbye)
            elif call.data == 'news':
                company_new = bot.send_message(message.from_user.id, "Enter company name")
                bot.register_next_step_handler(company_new, send_news, data)
                bot.register_next_step_handler(company_new, say_goodbye)
            elif call.data == 'both':
                company_new = bot.send_message(message.from_user.id, "Enter company name")
                bot.register_next_step_handler(company_new, send_stock_price, data)
                bot.register_next_step_handler(company_new, send_news, data)
                bot.register_next_step_handler(company_new, say_goodbye)
            elif call.data == 'end':
                bot.send_message(message.from_user.id, "Thank you for this session! Stay tuned with us! To start again type /start ")

    #sending the finiancial statement outcome using sompany, limit and type of stat paremeters
    #function uses free API
    def send_result(message, data):
        try:
            limit = int(message.text)
            limit=int(message.text)
            print(limit)
            company = data[-2]
            statement = data[-1]
            starter = 'https://financialmodelingprep.com/api/v3/'
            closer = '?apikey=7dd2f065517ca2bb8ca040cf3303e50f'
            final = starter + statement + company + closer
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

            bot.send_message(message.from_user.id, "\n".join(result))

            #2nd inline keyboard - next step choice
            keyboard_next_step = types.InlineKeyboardMarkup()
            key_stock_ch = types.InlineKeyboardButton(text='📉 Overview stock price change', callback_data='stock')
            keyboard_next_step.add(key_stock_ch, row_width=1)
            key_news = types.InlineKeyboardButton(text='📨 Last company news', callback_data='news')
            keyboard_next_step.add(key_news, row_width=1)
            key_both = types.InlineKeyboardButton(text='📨 📉 Both options', callback_data='both')
            keyboard_next_step.add(key_both, row_width=1)
            key_end = types.InlineKeyboardButton(text='Nothing, thank you, I am done 👋', callback_data='end')
            keyboard_next_step.add(key_end, row_width=1)
            bot.send_message(message.from_user.id, "I can also provide you with stock price change and show you latest news. What would you like to get to know? ", reply_markup=keyboard_next_step)
        except ValueError:
            bot.send_message(message.from_user.id, "Please enter numeric value for limit next time. Type /start or /help to proceed")
        except IndexError:
            bot.send_message(message.from_user.id, "Ups.. Looks like this stock ticker is wrong or this company is discontinued from our database. Please doublecheck this next time. Type /start or /help to proceed")

    #sending the stock price change using company stock ticker
    #function uses free API
    def send_stock_price(message, data):
        try:
            company = message.text
            starter = 'https://financialmodelingprep.com/api/v3/stock-price-change/'
            closer = '?apikey=7dd2f065517ca2bb8ca040cf3303e50f'
            url = starter + company + closer
            response = requests.get(url)
            response = response.json()
            response = response[0]
            print(response)
            result=[]
            for key in response:
                a = str(key) + " : " + str(response[key])
                result.append(a)
            bot.send_message(message.from_user.id, "\n".join(result))
        except IndexError:
            bot.send_message(message.from_user.id,"Ups.. Looks like this stock ticker is wrong or this company is discontinued from our database. Please doublecheck this next time. Type /start or /help to proceed")

    # sending the latest news using company stock ticker
    # function uses free API
    def send_news(message, data):
        try:
            company = message.text
            url = "https://real-time-finance-data.p.rapidapi.com/stock-news"
            querystring = {"symbol": company, "language": "en"}
            headers = {
                "X-RapidAPI-Key": "58027c3fb0msh8062b42813f30cdp1d5c96jsn5df802fcae2a",
                "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            response = response.json()
            print(response)
            parcer1 = response['data']
            parcer2 = parcer1['news']
            parcer3 = parcer2[0]
            news = parcer3['article_title']
            link = parcer3['article_url']
            source = parcer3['source']
            time = parcer3['post_time_utc']
            bot.send_message(message.from_user.id, f'{news}, access article via link: {link}, source and time: {source}, {time} ')
        except IndexError:
            bot.send_message(message.from_user.id, "Ups.. Looks like this stock ticker is wrong or this company is discontinued from our database. Please doublecheck this next time. Type /start or /help to proceed")


    def say_goodbye(message):
        msg=message.text
        bot.send_message(message.from_user.id, "Thank you for this session! Stay tuned with us! To start again type /start ")



    bot.infinity_polling()


run_EasyFin_bot(token)

