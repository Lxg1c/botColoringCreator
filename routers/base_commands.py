from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils import markdown
from aiogram import F
from keyboards.replyKeyboard import ButtonText

from keyboards import get_on_start_kb

router = Router(name=__name__)

@router.message(CommandStart())
async def handle_start(message: Message):
    await message.answer(
        text=f"Привет, {markdown.hbold(message.from_user.full_name)}!\nЯ бот, который может делать раскраски "
             f"из картинок, которые ты мне покажешь.\nТак что не жди! Просто отправь мне любое фото",
        reply_markup=get_on_start_kb(),
        parse_mode=ParseMode.HTML,
    )


@router.message(F.text == ButtonText.SEND_IMAGE)
@router.message(Command(ButtonText.SEND_IMAGE))
async def handle_send_image(message: Message):
    await message.answer(
        text="Ну потом сюда инструкцию сделаем"
    )


@router.message(F.text == ButtonText.ABOUT_SERVICE)
@router.message(Command(ButtonText.ABOUT_SERVICE))
async def handle_send_image(message: Message):
    await message.answer(
        text="НУ ХУЛИ тут писать, ну типа анекдот"
    )


@router.message(F.text == ButtonText.HELP)
@router.message(Command(ButtonText.HELP))
async def handle_send_image(message: Message):
    await message.answer(
        text="Я это если чо. В рот геймдев ебал. Я собрал холодильник сам из "
             "материалов, тк у меня все розовое, а потом подумал что если я "
             "удалю папка откуда я взял ассет, а мой закину в префабы то он "
             "останется, но я так никогда не ошибался, сука"
    )
