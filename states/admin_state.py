from aiogram.dispatcher.filters.state import State, StatesGroup


class SuperAdminState(StatesGroup):
    SUPER_ADMIN_STATE_MAIN = State()
    SUPER_ADMIN_STATE_GET_ADVERTISEMENT = State()
    SUPER_ADMIN_SEND_MESSAGE_TO_ADMINS = State()
    SUPER_ADMIN_ADD_ADMIN = State()
    SUPER_ADMIN_ADD_FULLNAME = State()
    SUPER_ADMIN_ADD_CHANNEL = State()
    SUPER_ADMIN_SELECT_CATEGORY = State()
    SUPER_ADMIN_ADD_CATEGORY = State()
    SUPER_ADMIN_SELECT_SUBCATEGORY = State()
    SUPER_ADMIN_SELECT_SUBCATEGORY_GET_INFO = State()
    SUPER_ADMIN_ADD_SUBCATEGORY = State()
    
    SUPER_ADMIN_ADD_POST = State()
    SUPER_ADMIN_UPDATE_CAPTION = State()
    SUPER_ADMIN_UPDATE_PHOTO = State()

    SUPER_ADMIN_NAME = State()
    SUPER_ADMIN_PRICE = State()
    SUPER_ADMIN_PHOTO = State()
    SUPER_ADMIN_DESCTIPTION = State()
