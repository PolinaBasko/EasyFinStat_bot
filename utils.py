import requests
import aiohttp


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
        "X-RapidAPI-Key": "58027c3fb0msh8062b42813f30cdp1d5c96jsn5df802fcae2a",
        "X-RapidAPI-Host": "real-time-finance-data.p.rapidapi.com"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            return await response.json()

