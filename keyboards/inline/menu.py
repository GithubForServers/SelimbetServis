from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from loader import db
from aiogram.utils.callback_data import CallbackData

menu_cd = CallbackData("show_menu", "level", "category", "subcategory", "item_id")
buy_item = CallbackData("buy", "item_id")

def make_callback_data(level, category="0", subcategory="0", item_id="0"):
    return menu_cd.new(
        level=level, category=category, subcategory=subcategory, item_id=item_id
    )
from data.config import ADMINS
async def categories_keyboard(tgid):
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=1)
    categories = await db.select_all_category()

    for category in categories:
        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1, category=category["id"]
        )
        button_text = category['name']
        # Tugmani keyboardga qo'shamiz
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

        # Keyboardni qaytaramiz
    admin=ADMINS[-1]

    if tgid==int(admin):
        markup.row(
            InlineKeyboardButton(
                text="⬅️Ortga", callback_data='back_to_main_menu'
            )
        )
        return markup

    else:
        
        return markup



# Berilgan kategoriya ostidagi kategoriyalarni qaytaruvchi keyboard
async def subcategories_keyboard(category_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)

    # Kategoriya ostidagi kategoriyalarni bazadan olamiz
    subcategories = await db.select_subcategory(category_id)
    for subcategory in subcategories:
        button_text = f"{subcategory['name']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category_id,
            subcategory=subcategory["id"],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasini yasaymiz (yuoqri qavatga qaytamiz)
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga", callback_data=make_callback_data(level=CURRENT_LEVEL - 1)
        )
    )
    return markup


# Ostkategoriyaga tegishli mahsulotlar uchun keyboard yasaymiz
async def items_keyboard(category, subcategory):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=1)

    # Ost-kategorioyaga tegishli barcha mahsulotlarni olamiz
    items = await db.get_products(category,subcategory)
    for item in items:
        # Tugma matnini yasaymiz
        button_text = f"{item['name']} - ${item['price']}"

        # Tugma bosganda qaytuvchi callbackni yasaymiz: Keyingi bosqich +1 va kategoriyalar
        callback_data = make_callback_data(
            level=CURRENT_LEVEL + 1,
            category=category,
            subcategory=subcategory,
            item_id=item["id"],
        )
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    # Ortga qaytish tugmasi
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category
            ),
        )
    )
    return markup

def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(
        InlineKeyboardButton(text=f"🛒 Xarid qilish", callback_data=buy_item.new(item_id=item_id))
    )
    markup.row(
        InlineKeyboardButton(text="✉️Ulashish", switch_inline_query=item_id),
    )
    markup.row(
        InlineKeyboardButton(
            text="⬅️Ortga",
            callback_data=make_callback_data(
                level=CURRENT_LEVEL - 1, category=category, subcategory=subcategory
            ),
        )
    )
    return markup