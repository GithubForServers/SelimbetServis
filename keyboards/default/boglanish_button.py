from aiogram import types
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton
from loader import dp

boglanish = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="🛒Mahsulotlar")
    ],],
    resize_keyboard=True
)

check = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅Ha"),
            KeyboardButton(text="❌Yo'q")
        ],
    ],
    resize_keyboard=True
)
