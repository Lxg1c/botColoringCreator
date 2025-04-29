from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class ButtonText:
    SEND_IMAGE = "Отправить фото 🖼️"
    ABOUT_SERVICE = "О проекте 🤖"
    HELP = "Помощь 🆘"


def get_on_start_kb():
    send_image_btn = KeyboardButton(text=ButtonText.SEND_IMAGE)
    about_service_btn = KeyboardButton(text=ButtonText.ABOUT_SERVICE)
    help_btn = KeyboardButton(text=ButtonText.HELP)
    first_row = [send_image_btn]
    second_row = [about_service_btn, help_btn]
    markup = ReplyKeyboardMarkup(
        keyboard=[first_row, second_row],
        resize_keyboard=True,
    )

    return markup
