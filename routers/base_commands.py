from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils import markdown
from keyboards import ButtonText, get_on_start_kb
from shared import logger

router = Router(name=__name__)

@router.message(CommandStart())
async def handle_start(message: Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        text=(
            f"Привет, {markdown.hbold(message.from_user.full_name)}!\n\n"
            "Я бот, который может создать раскраску из картинки, которую ты мне отправишь.\n"
            "Так что не стесняйся — просто пришли любое изображение!"
        ),
        reply_markup=get_on_start_kb(),
        parse_mode=ParseMode.HTML,
    )

@router.message(F.text == ButtonText.SEND_IMAGE)
@router.message(Command(ButtonText.SEND_IMAGE))
async def handle_send_image(message: Message):
    logger.info(f"User {message.from_user.id} requested to send image")
    await message.answer(
        text=(
            "Чтобы получить раскраску:\n"
            "1. Найди понравившуюся картинку в формате PNG, JPG, JPEG или WEBP.\n"
            "2. Отправь её сюда.\n"
            "3. Подтверди создание раскраски в появившемся меню.\n"
            "4. Немного подожди, пока нейросеть обработает изображение."
        )
    )

@router.message(F.text == ButtonText.ABOUT_SERVICE)
@router.message(Command(ButtonText.ABOUT_SERVICE))
async def handle_about_service(message: Message):
    logger.info(f"User {message.from_user.id} requested about service")
    await message.answer(
        text=(
            "Этот сервис создан студентами Донского государственного технического университета.\n\n"
            "Его цель — дать детям возможность раскрашивать изображения, которые им нравятся."
        )
    )

@router.message(F.text == ButtonText.HELP)
@router.message(Command(ButtonText.HELP))
async def handle_help(message: Message):
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer(
        text="Поддержка: @Kharamen"
    )

