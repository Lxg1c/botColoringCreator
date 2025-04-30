import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.utils import markdown
from keyboards import ButtonText, get_on_start_kb, get_confirm_keyboard

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@router.message(F.photo | (F.document & F.document.mime_type.startswith("image/")))
async def handle_image(message: Message):
    logger.info(f"User {message.from_user.id} sent an image")
    # Определим объект фото/документа
    if message.photo:
        file_id = message.photo[-1].file_id
    else:
        file_id = message.document.file_id

    # Отправим изображение обратно с inline-клавиатурой
    await message.answer_photo(
        photo=file_id,
        caption="Это изображение подходит?",
        reply_markup=get_confirm_keyboard()
    )

@router.callback_query(F.data == "confirm_image")
async def handle_confirm(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} confirmed image")
    await callback.message.edit_caption(caption="✅ Изображение подтверждено!")
    await callback.answer("Изображение подтверждено")

@router.callback_query(F.data == "edit_image")
async def handle_edit(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} chose to edit image")
    await callback.message.edit_caption(caption="✏️ Хорошо, отправь новое изображение.")
    await callback.answer("Отправьте новое изображение")

@router.callback_query(F.data == "cancel_image")
async def handle_cancel(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} canceled image")
    await callback.message.edit_caption(caption="❌ Отменено.")
    await callback.answer("Действие отменено")