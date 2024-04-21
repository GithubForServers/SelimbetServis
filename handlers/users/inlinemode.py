from loader import dp,bot,db
from aiogram import types 
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup

from handlers.users.buy import show_item
@dp.inline_handler()
async def query_car_by_id(query: types.InlineQuery):
    
    query_text = query.query.strip()
    if query_text.isdigit():  
        car_id = int(query_text)
        car = await db.get_product(car_id)
        if car:
            forward = InlineKeyboardMarkup(row_width=1)
            forward.insert(InlineKeyboardButton(text="Ulashish↗️", switch_inline_query=car_id))
            caption_text = await show_item(car_id)
            await query.answer(
                results=[
                    types.InlineQueryResultPhoto(
                        id=str(car_id),
                        photo_url=car['photo'],
                        thumb_url=car['photo'],
                        caption=caption_text,
                        reply_markup=forward
                    )
                ],
                cache_time=1
            )
            return
    await query.answer(results=[], cache_time=1)