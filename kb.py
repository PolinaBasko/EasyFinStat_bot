from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text=" 💵 Financial statements", callback_data="fin_stat"),
    InlineKeyboardButton(text=" 📉 Stock Price Δ", callback_data="st_price")],
    [InlineKeyboardButton(text=" 📨 Recent news", callback_data="st_news"),
    InlineKeyboardButton(text=" 📂 Ticker library", callback_data="ticker_libr")],
    [InlineKeyboardButton(text="🔎 Help", callback_data="help")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Main menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Main menu", callback_data="menu")]])

finstat_choice = [
    [InlineKeyboardButton(text="📊 Income Statement", callback_data="income statement")],
    [InlineKeyboardButton(text="📈 Cash Flow", callback_data="cash flow")],
    [InlineKeyboardButton(text="🧾 Balance Sheet", callback_data="balance sheet")]
]
finstat_choice = InlineKeyboardMarkup(inline_keyboard=finstat_choice)