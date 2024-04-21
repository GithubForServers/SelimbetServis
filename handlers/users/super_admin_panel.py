import time
import datetime
from utils.db_api.test import upload_instagram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filters import IsSuperAdmin
from keyboards.inline.main_menu_super_admin import main_menu_for_super_admin, back_to_main_menu
from loader import dp, db, bot
from states.admin_state import SuperAdminState
from middlewares.MediaGroup import AlbumMiddleware
from utils.db_api.test import photo_link



@dp.callback_query_handler(IsSuperAdmin(), text="add_admin", state="*")
async def add_admin(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Yangi adminni chat IDsini yuboring...\n"
                                 "🆔 Admin ID raqamini olish uchun @userinfobot ga /start bosishini ayting",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_ADMIN.set()

@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_ADMIN)
async def add_admin_method(message: types.Message, state: FSMContext):
    admin_id =message.text
    await state.update_data({"admin_id": admin_id})
    await message.answer("👨🏻‍💻 Yangi admin ismini yuborin",
                                 reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_ADD_FULLNAME.set()
#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_ADD_FULLNAME)
async def add_admin_method(message: types.Message,state: FSMContext):
    try:
        full_name = message.text
        await state.update_data({"full_name": full_name})
        malumot = await state.get_data()
        # Dasturchi @Mrgayratov kanla @Kingsofpy
        adminid = malumot.get("admin_id")
        full_name = malumot.get("full_name")
        try:
            # Convert user_id to integer before passing it to add_admin method
            await db.add_admin(user_id=int(adminid), full_name=full_name)
        except Exception as ex:
            print(ex)
        await bot.send_message(chat_id=adminid,text="tabriklaymiz siz botimizda adminlik huquqini qolgan kiritidingiz /start bosin")
        await message.answer("✅ Yangi admin muvaffaqiyatli qo'shildi!", reply_markup=main_menu_for_super_admin)
        await state.finish()
    except Exception as e:
        print(e)
        await message.answer("❌ Xatolik yuz berdi!", reply_markup=main_menu_for_super_admin)
        await state.finish()

@dp.callback_query_handler(IsSuperAdmin(), text="del_admin", state="*")
async def show_admins(call: types.CallbackQuery):

    await call.answer(cache_time=2)
    admins = await db.select_all_admins()
    buttons = InlineKeyboardMarkup(row_width=1)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[2]}", callback_data=f"admin:{admin[1]}"))
    # Dasturchi @Mrgayratov kanla @Kingsofpy
    buttons.add(InlineKeyboardButton(text="➕ Admin qo'shish", callback_data="add_admin"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text="👤 Adminlar", reply_markup=buttons)
    
#Dasturchi @Mrgayratov kanla @Kingsofpy
@dp.callback_query_handler(IsSuperAdmin(), text_contains="admin:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    admin = await db.select_all_admin(user_id=int(data[1]))
    for data in admin:
        text = f"Sizning ma'lumotlaringiz\n\n"
        text += f"<i>👤 Admin ismi :</i> <b>{data[2]}\n</b>"
        text += f"<i>🆔 Admin ID raqami :</i> <b>{data[1]}</b>"
        buttons = InlineKeyboardMarkup(row_width=1)

        buttons.insert(InlineKeyboardButton(text="❌ Admindan bo'shatish", callback_data=f"deladm:{data[1]}"))
        buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admins"))

        await call.message.edit_text(text=text, reply_markup=buttons)

@dp.callback_query_handler(IsSuperAdmin(), text_contains="deladm:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    delete_orders = await db.delete_admin(admin_id=int(data[1]))
    await bot.send_message(chat_id=data[1],
                           text="Sizdan adminlik huquqi olindi")

    await call.answer("🗑 Admin o'chirildi !",show_alert=True)
    await call.message.edit_text("✅ Admin muvaffaqiyatli o'chirildi!", reply_markup=main_menu_for_super_admin)


# ADMIN TAYORLASH VA CHIQARISH QISMI UCHUN

# MAJBURIY OBUNA SOZLASH UCHUN
@dp.callback_query_handler(text = "add_channel")
async def add_channel(call: types.CallbackQuery):
    await SuperAdminState.SUPER_ADMIN_ADD_CHANNEL.set()
    await call.message.edit_text(text="<i><b>📛 Kanal usernamesini yoki ID sini kiriting: </b></i>")
    await call.message.edit_reply_markup(reply_markup=back_to_main_menu)


@dp.message_handler(state=SuperAdminState.SUPER_ADMIN_ADD_CHANNEL)
async def add_channel(message: types.Message, state: FSMContext):
    matn = message.text
    if matn.isdigit() or matn.startswith("@") or matn.startswith("-"):
        try:
            if await db.check_channel(channel=message.text):
                await message.answer("<i>❌Bu kanal qo'shilgan! Boshqa kanal qo'shing!</i>", reply_markup=back_to_main_menu)
            else:
                try:
                    deeellll = await bot.send_message(chat_id=message.text, text=".")
                    await bot.delete_message(chat_id=message.text, message_id=deeellll.message_id)
                    try:
                        await db.add_channel(channel=message.text)
                    except:
                        pass
                    await message.answer("<i><b>Channel succesfully added ✅</b></i>")
                    await message.answer("<i>Siz admin panelidasiz. 🧑‍💻</i>", reply_markup=main_menu_for_super_admin)
                    await state.finish()
                except:
                    await message.reply("""<i><b>
Bu kanalda admin emasman!⚙️
Yoki siz kiritgan username ga ega kanal mavjud emas! ❌
Kanalga admin qilib qaytadan urinib ko'ring yoki to'g'ri username kiriting.🔁
                    </b></i>""", reply_markup=back_to_main_menu)
        except Exception as err:
            await message.answer(f"Xatolik ketdi: {err}")
            await state.finish()
    else:
        await message.answer("Xato kiritdingiz.", reply_markup=back_to_main_menu)

@dp.callback_query_handler(text="del_channel")
async def channel_list(call: types.CallbackQuery):
    royxat = await db.select_channels()
    text = "🔰 Kanallar ro'yxati:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[1]}\n💠 Username: {o[1]}\n\n"
    await call.message.edit_text(text=text)
    admins =await db.select_all_channels()
    buttons = InlineKeyboardMarkup(row_width=2)
    for admin in admins:
        buttons.insert(InlineKeyboardButton(text=f"{admin[1]}", callback_data=f"delchanel:{admin[1]}"))

    buttons.add(InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel"))
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)

@dp.callback_query_handler(IsSuperAdmin(), text_contains="delchanel:", state="*")
async def del_admin_method(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    data = call.data.rsplit(":")
    delete_orders = await db.delete_channel(channel=data[1])
    await call.answer("🗑 Channel o'chirildi !",show_alert=True)
    await call.message.edit_text("✅ Kanal muvaffaqiyatli o'chirildi!", reply_markup=main_menu_for_super_admin)
# MAJBURIY OBUNA SOZLASH UCHUN

# ADMINLARNI KORISH
@dp.callback_query_handler(text="admins")
async def channel_list(call: types.CallbackQuery):
    royxat = await db.select_admins()
    text = "🔰 Adminlar ro'yxati:\n\n"
    son = 0
    for o in royxat:
        son +=1
        text += f"{son}. {o[2]}\nID : {o[1]}💠 Ismi: {o[2]}\n\n"
    await call.message.edit_text(text=text)

    buttons = InlineKeyboardMarkup(row_width=1)
    buttons.insert(InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back_to_main_menu"))
    await call.message.edit_text(text=text, reply_markup=buttons)
# ADMINLARNI KORISH

# STATISKA KORISH UCHUN
@dp.callback_query_handler(text="statistics")
async def stat(call : types.CallbackQuery):
    stat = await db.stat()
    stat = str(stat)
    for x in stat:
        dta = x
        datas = datetime.datetime.now()
        yil_oy_kun = (datetime.datetime.date(datetime.datetime.now()))
        soat_minut_sekund = f"{datas.hour}:{datas.minute}:{datas.second}"
        await call.message.delete()
        await call.message.answer(f"<b>👥 Bot foydalanuvchilari soni: {(x)} nafar\n</b>"
                                  f"<b>⏰ Soat: {soat_minut_sekund}\n</b>"
                                  f"<b>📆 Sana: {yil_oy_kun}</b>",reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("◀️ Orqaga",callback_data="back_to_main_menu")))


# ADMINGA SEND FUNC
@dp.callback_query_handler(IsSuperAdmin(), text="send_message_to_admins", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Reklamani yuboring...\n"
                                 "Yoki bekor qilish tugmasini bosing", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS.set()


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS,content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    users = await db.stat_admins()
    users = str(users)
    for x in users:
        await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
                             f"📊 Adminlar soni: {x} ta\n"
                             f"🕒 Kuting...\n")
        user = await db.select_all_admins()

        for i in user:
            user_id= i['user_id']
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                       message_id=message.message_id,reply_markup=message.reply_markup, parse_mode=types.ParseMode.HTML)

                time.sleep(0.5)
            except Exception as e:
                print(e)


        await message.answer("✅ Reklama muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
        await state.finish()
# ADMINGA SEND FUNC TUGADI

# ====================Foydalanuvchliar uchun SEND SUNC  ============================
@dp.callback_query_handler(IsSuperAdmin(), text="send_advertisement", state="*")
async def send_advertisement(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    await call.message.edit_text("Reklamani yuboring...\n"
                                 "Yoki bekor qilish tugmasini bosing", reply_markup=back_to_main_menu)
    await SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT.set()


@dp.message_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_STATE_GET_ADVERTISEMENT,
                    content_types=types.ContentTypes.ANY)
async def send_advertisement_to_user(message: types.Message,state: FSMContext):
    users =  await db.stat()
    admin_id = message.from_user.id
    users = str(users)
    for x in users:
        await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
                             f"📊 Foydalanuvchilar soni: {x} ta\n"
                             f"🕒 Kuting...\n")
        user = await db.select_all_users()
        for i in user:
            user_id= i['user_id']
            try:
                await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                       message_id=message.message_id, reply_markup=message.reply_markup, parse_mode=types.ParseMode.HTML)

                time.sleep(0.5)
            except Exception as e:
                await bot.send_message(admin_id,e)


        await message.answer("✅ Reklama muvaffaqiyatli yuborildi!", reply_markup=main_menu_for_super_admin)
        await state.finish()
# ========================================================================================= #
# ========================================================================================= #
# ***************************************************************************************** # 
#                    MAHSULOTNI BAZAGA QO'SHISH UCHUN HANDLER YOZAMIZ                       #
# ========================================================================================= #
# ***************************************************************************************** #
# ========================================================================================= #

@dp.callback_query_handler(IsSuperAdmin(), text="add_mahsulot", state="*")
async def add_item(call: types.CallbackQuery):
    await call.answer(cache_time=1)
    categories = InlineKeyboardMarkup(row_width=2)
    categorys = await db.select_all_category()
    for category in categorys:
        categories.insert(InlineKeyboardButton(text=category['name'],callback_data=category['id']))
    categories.add(InlineKeyboardButton(text="➕Categoriya qo'shish",callback_data='add_category'))
    categories.add(InlineKeyboardButton(text="⬅️ Orqaga",callback_data='back_to_main_menu'))
    await call.message.edit_text("Mahsulot qo'shish uchun ,Mahsulot categoriyasini tanlang!", reply_markup=categories)
    
    await SuperAdminState.SUPER_ADMIN_SELECT_CATEGORY.set()

# =================================DAVOMI======================================================== #

@dp.callback_query_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_SELECT_CATEGORY)
async def add_category(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    if call.data.isdigit():
        category_id = call.data
        await state.update_data({"category_id": category_id})
        subcategories = InlineKeyboardMarkup(row_width=2)
        subcategorys = await db.select_subcategory(call.data) 
        for subcategory in subcategorys:

            subcategories.insert(InlineKeyboardButton(text=subcategory['name'],callback_data=subcategory['id']))
        subcategories.add(InlineKeyboardButton(text="➕Subcategoriya qo'shish",callback_data='add_subcategory'))
        # subcategories.add(InlineKeyboardButton(text="⬅️ Orqaga",callback_data='back_to_category_menu'))
        select_category = await call.message.edit_text("Subcategoriyalarni tanglang!", reply_markup=subcategories)
        await SuperAdminState.SUPER_ADMIN_SELECT_SUBCATEGORY.set()

    elif call.data == 'back_to_main_menu':
        await call.answer(cache_time=1)
        await call.message.edit_text(text="👨‍💻 Bosh menyu", reply_markup=main_menu_for_super_admin)
        await state.finish()
    elif call.data =='add_category':
        text = await call.message.answer('Categoriya nomini kiriting:')
        message_id= text.message_id
        await SuperAdminState.SUPER_ADMIN_ADD_CATEGORY.set()
    else:
        await state.finish()
    
# GET PRODUCTS INFORMATIONS
@dp.callback_query_handler(IsSuperAdmin(), state=SuperAdminState.SUPER_ADMIN_SELECT_SUBCATEGORY)
async def get_info(call: types.CallbackQuery,state: FSMContext):
    
    await call.answer(cache_time=1)
    data = await state.get_data()
    if call.data.isdigit():
        await call.message.edit_reply_markup()
        await call.message.edit_text("📛Mahsulot nomini yuboring.")
        await state.update_data({"subcategory_id": call.data})

        await SuperAdminState.SUPER_ADMIN_NAME.set()
    elif call.data=='add_subcategory':
        await call.answer(cache_time=1)
        await call.message.answer('Sub Categoriya nomini yuboring!')
        await SuperAdminState.SUPER_ADMIN_ADD_SUBCATEGORY.set()    
    else:
        await state.finish()
 
@dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_NAME)
async def name_state(message: types.Message,state:FSMContext):
    item_name = message.text
    print(item_name)
    await state.update_data({"item_name": item_name})
    await message.answer(f"💸Iltimos <b>{item_name}</b>ning narxini kiriting:")
    await SuperAdminState.SUPER_ADMIN_PRICE.set()

@dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_PRICE)
async def price_state(message: types.Message,state: FSMContext):
    if message.text.isdigit():
        print(message.text)
        price = message.text
        await state.update_data({"price": price})
        await message.answer(f"🖼Iltimos mahsulot rasmni yuboring.")
        await SuperAdminState.SUPER_ADMIN_PHOTO.set()
@dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_PHOTO,
                    content_types=types.ContentType.PHOTO)
async def photo_state(message: types.Message,state:FSMContext):
    photo = message.photo[-1]
    link = await photo_link(photo)
    await state.update_data({"photo": link})
    await message.answer("📃Iltimos Mahsulot haqida qisqacha malumot yuboring!")
    await SuperAdminState.SUPER_ADMIN_DESCTIPTION.set()

@dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_DESCTIPTION)
async def description_state(message: types.Message,state: FSMContext):
    description = message.text
    await state.update_data({"desctiption": {description}})
    data = await state.get_data()
    category_id = data.get('category_id')
    subcategory_id = data.get('subcategory_id')
    name = data.get('item_name')
    price = data.get('price')
    photo = data.get('photo')

    await db.add_product(name=name,description=description,price=price,category_id=int(category_id),subcategory_id=int(subcategory_id),photo=str(photo))
    await message.answer('Malumotlaringiz qabul qilindi.Endi ular baza ga va ijtimoiy tarmoqlarga qoyiliyapdi')
    
    await state.finish()







# SUBCATEGORIYA QO'SHISH UCHUN HANDLER YOZAMIZ/

@dp.message_handler(IsSuperAdmin(), state = SuperAdminState.SUPER_ADMIN_ADD_SUBCATEGORY)
async def add_subcategory(message: types.Message,state: FSMContext):
    category_name = message.text
    data = await state.get_data()
    category_id = data.get('category_id')
    # print(data)
    print(category_id)
    await db.add_subcategory(name=category_name,category_id=int(category_id))
    await message.answer('✅SubCategoriya muvaffaqiyatli qo\'shildi')
    subcategories = InlineKeyboardMarkup(row_width=2)
    subcategorys = await db.select_subcategory(category_id) 
    for subcategory in subcategorys:
        print(subcategory)
        subcategories.insert(InlineKeyboardButton(text=subcategory['name'],callback_data=subcategory['id']))
    subcategories.add(InlineKeyboardButton(text="⬅️ Orqaga",callback_data='back_to_category_menu'))
    subcategories.add(InlineKeyboardButton(text="➕Subcategoriya qo'shish",callback_data='add_subcategory'))
    select_category = await message.edit_text("Subcategoriyalarni tanglang!", reply_markup=subcategories)
    await SuperAdminState.SUPER_ADMIN_SELECT_CATEGORY.set()

# CATEGORIYA QO'SHISH UCHUN HANDLER YOZAMIZ/
@dp.message_handler(IsSuperAdmin(), state = SuperAdminState.SUPER_ADMIN_ADD_CATEGORY)
async def add_category(message: types.Message,state: FSMContext):
    category_name = message.text
    await db.add_category(message.text)
    await message.answer('✅Categoriya muvaffaqiyatli qo\'shildi')
    categories = InlineKeyboardMarkup(row_width=2)
    categorys = await db.select_all_category()
    for category in categorys:
        categories.insert(InlineKeyboardButton(text=category['name'],callback_data=category['id']))
    categories.add(InlineKeyboardButton(text="➕Categoriya qo'shish",callback_data='add_category'))
    categories.add(InlineKeyboardButton(text="⬅️ Orqaga",callback_data='back_to_main_menu'))
    await message.answer("Mahsulot qo'shish uchun ,Mahsulot categoriyasini tanlang!", reply_markup=categories)
    await SuperAdminState.SUPER_ADMIN_SELECT_CATEGORY.set()
# ========================================================================================= #
# ========================================================================================= #
# ***************************************************************************************** # 
#                    MAHSULOT QO'SHIB UNI TARQATISH UCHUN HANDLER YOZAMIZ                   #
# ========================================================================================= #
# ***************************************************************************************** #
# ========================================================================================= #



from typing import List, Union
@dp.message_handler(IsSuperAdmin(),state=SuperAdminState.SUPER_ADMIN_ADD_POST,
                    content_types=types.ContentTypes.ANY)
async def add_post_to_social(message: types.Message,state: FSMContext):
    # ADD PRODUCT ON DATABASE
    
    # ENG TO ADD PRODUCT ON DATABASE
    file = message.content_type
    users =  await db.stat()
    admin_id = message.from_user.id

    print()
    caption_entities = message.caption_entities
    urls = []

    for caption_entry in caption_entities:
        if caption_entry.type == 'text_link':
            urls.append(caption_entry.url)
    users = str(users)
    for x in users:
        user = await db.select_all_users()
        for i in user:
            user_id = i['user_id']
            try:
                await bot.copy_message(
                    chat_id=user_id,
                    from_chat_id=message.from_user.id,
                    message_id=message.message_id,
                    reply_markup=message.reply_markup
                )

                time.sleep(0.5)
            except Exception as e:
                await bot.send_message(admin_id, e)

    
    channels = await db.channel_stat()
    channels = str(channels)

    for y in channels:

        await message.answer(f"📢 Reklama jo'natish boshlandi...\n"
                             f"📊 Foydalanuvchilar soni: {x} ta\n"
                             f"📌 Kanallar soni: {y} ta\n"
                             f"🕒 Kuting...\n")
        channels = await db.select_all_channels()
        for i in channels:
            channel=i['channel']
            channel_info = await bot.get_chat(channel)
            channel = channel_info.id
            try:
                await bot.copy_message(chat_id=channel, from_chat_id=admin_id,
                                       message_id= message.message_id,reply_markup=message.reply_markup, parse_mode=types.ParseMode.HTML)
                
                
                time.sleep(0.5)
            except Exception as e:
                await bot.send_message(admin_id,e)
# =================== ADD POST ON INSTAGRAM =================================
        file_type = message.content_type
        if file_type=='photo':
            photo = message.photo[-1]
            file_id = photo.file_id
            caption = f"\n{message.caption}\n"
            rasm = await upload_instagram(content_type=file_type,file_id=file_id,photo=photo,caption=caption)

        await message.answer("✅ Contentlaringiz Telegram kanal va Instagram sahifangizga muvaffaqiyatli joylandi!", reply_markup=main_menu_for_super_admin)


    await state.finish()


#Media group uchun handler yozdim
async def handle_albums(message: types.Message, album: List[types.Message]):
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()

    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")

    await message.answer_media_group(media_group)




# Bosh menu
@dp.callback_query_handler(IsSuperAdmin(), text="back_to_main_menu", state="*")
async def back_to_main_menu_method(call: types.CallbackQuery,state: FSMContext):
    await call.answer(cache_time=1)
    await call.message.edit_text(text="👨‍💻 Bosh menyu", reply_markup=main_menu_for_super_admin)
    await state.finish()

from typing import List
