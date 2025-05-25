from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from kafka_settings.producer import send_prompt, send_image
from keyboards import get_confirm_keyboard
from shared import logger
import io


router = Router(name=__name__)


async def download_photo(bot, file_id: str) -> io.BytesIO:
    """Скачивает фото по file_id и возвращает BytesIO"""
    file = await bot.get_file(file_id)
    photo_bytes = await bot.download_file(file.file_path)
    return io.BytesIO(photo_bytes.read())


@router.message(F.photo | (F.document & F.document.mime_type.startswith("image/")))
async def handle_image(message: Message, state: FSMContext, bot):
    logger.info(f"User {message.from_user.id} sent an image")

    file_id = message.photo[-1].file_id if message.photo else message.document.file_id

    # Сохраняем file_id в FSMContext
    await state.update_data(file_id=file_id, input_type="image")

    photo_io = await download_photo(bot, file_id)
    photo_io.seek(0)
    image_data = photo_io.read()

    await message.answer_photo(
        photo=BufferedInputFile(image_data, filename="preview.jpg"),
        caption="Это изображение подходит?",
        reply_markup=get_confirm_keyboard()
    )


@router.message(F.text)
async def handle_text(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent a prompt")
    await state.update_data(prompt=message.text, input_type="text")
    await message.answer(
        text=f"{message.text}\n\nСгенерировать раскраску с этим описанием?",
        reply_markup=get_confirm_keyboard()
    )


@router.callback_query(F.data == "confirm_image")
async def handle_confirm(callback: CallbackQuery, state: FSMContext, bot):
    logger.info(f"User {callback.from_user.id} подтвердил генерацию")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("✅ Генерируем раскраску...")
    data = await state.get_data()
    input_type = data.get("input_type")

    try:
        logger.info("Определяем тип генерации")
        if input_type == "text":
            logger.info("Тип генерации: текст")
            prompt = data.get("prompt")
            if not prompt:
                await callback.message.answer("❌ Описание не найдено.")
                return
            await send_prompt(prompt, callback.from_user.id, callback.message.chat.id)
            logger.info(f"Промпт отправлен на обработку. Промпт: {prompt}")
        else:
            logger.info("Тип генерации: фото")
            logger.info(data)
            file_id = data.get("file_id")
            if not file_id:
                await callback.message.answer("❌ Изображение не найдено.")
                return
            photo_bytes = await download_photo(bot, file_id)
            await send_image(photo_bytes.getvalue(), callback.from_user.id, callback.message.chat.id)
            logger.info("Фото отправлено на обработку")
    except Exception as e:
        logger.error(f"Ошибка обработки: {e}")
        await callback.message.answer("❌ Произошла ошибка при обработке. Попробуйте позже.")
    finally:
        await state.clear()


@router.callback_query(F.data == "edit_image")
async def handle_edit(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} chose to edit")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("✏️ Хорошо, отправь новое изображение или описание.")


@router.callback_query(F.data == "cancel_image")
async def handle_cancel(callback: CallbackQuery):
    logger.info(f"User {callback.from_user.id} canceled input")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("❌ Генерация отменена.")