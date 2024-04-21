from data.config import ADMINS
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove
from loader import dp,bot,db
from aiogram import types
from keyboards.inline.menu import buy_item
from aiogram.types import CallbackQuery
from states.buy_cars import PersonalData
from aiogram.dispatcher import FSMContext
from keyboards.inline.menu import item_keyboard
from keyboards.default.boglanish_button import boglanish

@dp.callback_query_handler(buy_item.filter(),state=None)
async def buy(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    data = callback_data['item_id']
    await state.update_data(
        {"item_id": data}
    )
    fullname_msg = await call.message.answer(f"👤Ism Familiyangiz yuboring!")
    await PersonalData.fullName.set()
    

# Foydanuvchini Ism va Familiyasi olamiz
@dp.message_handler(state=PersonalData.fullName)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(
        {"name": fullname}
    )
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_button = KeyboardButton(text="☎️ Yuborish", request_contact=True)
    keyboard.add(phone_button)

    await message.answer("📞Telefon raqamingizni yuboring.",reply_markup=keyboard)

    await PersonalData.phoneNum.set()

async def show_item(item_id):

    item = await db.get_product(item_id)

    if item["photo"]:
        text = f"<a href=\"{item['photo']}\"> 🚘Mashina Nomi: {item['name']} </a>\n"
    else:
        text = f"{item['name']}\n\n"
    text += f"💸Narxi: {item['price']}$\n\n<b>Mashina Haqida👇</b>\n<i>    {item['description']}</i>\n"

    return text

@dp.message_handler(content_types=types.ContentType.CONTACT,state=PersonalData.phoneNum)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username
    await state.update_data(
        {"phone": phone,
         'username': username,
         'user_id': user_id}
    )
    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")
    item_id = data.get('item_id')  
    ariza = "<b>📩Foydalanuvchidan Kelgan Ariza Mavjud!</b>\n\n"
    ariza += f"👤Ism Familiya: {name}\n"
    ariza += f"📞Telefon raqam: {phone}\n"
    ariza += f"✅Username: @{username}\n"
    ariza += f"🆔Telegram_id:{user_id}\n\n"
    ariza += f"<b>🔰Moshina haqida Malumot.</b>\n\n"
    ariza += await show_item(item_id)

    await bot.send_message(ADMINS[-1],ariza)
    msg = "✅Malumotlaringiz Qabul Qilindi Adminlarimiz tez orada siz bilan bo'g'lanishadi."

    await message.answer(msg,reply_markup=boglanish)
    await state.finish()
