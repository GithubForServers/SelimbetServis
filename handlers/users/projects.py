from loader import dp,db
from typing import Union

from aiogram import types
from aiogram.types import CallbackQuery, Message
from keyboards.inline.menu import categories_keyboard,subcategories_keyboard,menu_cd,items_keyboard,item_keyboard,buy_item


@dp.message_handler(text="🛒Mahsulotlar",state='*')
@dp.callback_query_handler(text="Mahsulotlar",state='*')
async def show_menu(message: types.Message):
    # Foydalanuvchilarga barcha kategoriyalarni qaytaramiz
    await list_categories(message)

async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    # Keyboardni chaqiramiz
    markup = await categories_keyboard(message.from_user.id)

    # Agar foydalanuvchidan Message kelsa Keyboardni yuboramiz
    if isinstance(message, Message):
        await message.answer("Bo'lim tanlang", reply_markup=markup)

    # Agar foydalanuvchidan Callback kelsa Callback natbibi o'zgartiramiz
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_reply_markup(markup)


# Ost-kategoriyalarni qaytaruvchi funksiya
async def list_subcategories(callback: CallbackQuery, category, **kwargs):
    markup = await subcategories_keyboard(category)

    # Xabar matnini o'zgartiramiz va keyboardni yuboramiz
    await callback.message.edit_reply_markup(markup)


async def list_items(callback: CallbackQuery, category, subcategory, **kwargs):
    markup = await items_keyboard(category, subcategory)

    await callback.message.edit_text(text="Mahsulot tanlang", reply_markup=markup)

async def show_item(callback: CallbackQuery, category, subcategory, item_id):
    markup = item_keyboard(category, subcategory, item_id)

    # Mahsulot haqida ma'lumotni bazadan olamiz
    item = await db.get_product(item_id)

    if item["photo"]:
        text = f"<a href=\"{item['photo']}\"> 🚘Mashina Nomi: {item['name']} </a>\n\n"
    else:
        text = f"{item['name']}\n\n"
    text += f"💸Narxi: {item['price']}$\n\n<b>Mashina Haqida👇</b>\n    {item['description']}\n\n"
    text += f"Mashina kodi:{item_id}\n"

    await callback.message.edit_text(text=text, reply_markup=markup)

@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):

    # Foydalanuvchi so'ragan Level (qavat)
    current_level = callback_data.get("level")

    # Foydalanuvchi so'ragan Kategoriya
    category = callback_data.get("category")

    # Ost-kategoriya (har doim ham bo'lavermaydi)
    subcategory = callback_data.get("subcategory")

    # Mahsulot ID raqami (har doim ham bo'lavermaydi)
    item_id = int(callback_data.get("item_id", 0))  # Retrieve item_id from callback_data, default to 0 if not found

    # Har bir Level (qavatga) mos funksiyalarni yozib chiqamiz
    levels = {
        "0": list_categories,      # Kategoriyalarni qaytaramiz
        "1": list_subcategories,   # Ost-kategoriyalarni qaytaramiz
        "2": list_items,           # Mahsulotlarni qaytaramiz
        "3": show_item,            # Mahsulotni ko'rsatamiz
    }

    # Foydalanuvchidan kelgan Level qiymatiga mos funksiyani chaqiramiz
    current_level_function = levels[current_level]

    # Tanlangan funksiyani chaqiramiz va kerakli parametrlarni uzatamiz
    await current_level_function(call, category=category, subcategory=subcategory, item_id=item_id)  # Pass item_id to show_item function
