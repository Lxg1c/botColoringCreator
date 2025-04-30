from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class ButtonText:
    CONFIRM="✅ Подтвердить"
    CHANGE="✏️ Изменить"
    CANCEL="❌ Отмена"

def get_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=ButtonText.CONFIRM, callback_data="confirm_image"),
            InlineKeyboardButton(text=ButtonText.CHANGE, callback_data="edit_image"),
            InlineKeyboardButton(text=ButtonText.CANCEL, callback_data="cancel_image"),
        ]
    ])
