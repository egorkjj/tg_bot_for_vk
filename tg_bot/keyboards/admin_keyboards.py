from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def links_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text = "Добавить ссылку", callback_data= "link_add"))
    kb.add(InlineKeyboardButton(text="Удалить ссылку", callback_data= "link_delete"))
    return kb

def users_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Удалить пользователей в статистике", callback_data= "user_delete"))
    return kb

def loop_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Удалить пользователь в статистике по времени", callback_data = "loop_delete"))
    return kb
