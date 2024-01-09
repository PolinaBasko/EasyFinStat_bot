import requests
import aiohttp
import config


async def get_statement_func(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def get_stock_price_func(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def send_news_func(url, company):
    querystring = {"symbol": company, "language": "en"}
    headers = {
        "X-RapidAPI-Key": config.NEWS_API_TOKEN,
        "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            return await response.json()

