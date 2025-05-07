from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards import get_confirm_keyboard
from ai import handle_prompt as generate_coloring
from shared import logger

router = Router(name=__name__)


# 💾 Состояния FSM
class GenStates(StatesGroup):
    waiting_for_input = State()


# 📷📝 Обработка фото или текста
@router.message(F.photo | (F.document & F.document.mime_type.startswith("image/")))
async def handle_image(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent an image")

    file_id = message.photo[-1].file_id if message.photo else message.document.file_id

    await state.set_state(GenStates.waiting_for_input)
    await state.update_data(file_id=file_id, input_type="image")

    await message.answer_photo(
        photo=file_id,
        caption="Это изображение подходит?",
        reply_markup=get_confirm_keyboard()
    )


@router.message(F.text)
async def handle_text(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent a prompt")

    await state.set_state(GenStates.waiting_for_input)
    await state.update_data(prompt=message.text, input_type="text")

    await message.answer(
        text=f"{message.text}\n\nСгенерировать раскраску с этим описанием?",
        reply_markup=get_confirm_keyboard()
    )


# ✅ Универсальный обработчик подтверждения
@router.callback_query(F.data == "confirm_image")
async def handle_confirm(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} confirmed input")

    await callback.answer("✅ Генерируем раскраску...")

    data = await state.get_data()
    input_type = data.get("input_type")

    if input_type == "text":
        prompt = data.get("prompt")
        if not prompt:
            await callback.message.answer("❌ Описание не найдено.")
            return

        photo = await generate_coloring(prompt)
        if isinstance(photo, str):
            await callback.message.answer(f"❌ {photo}")
        else:
            await callback.message.answer_photo(photo=photo, caption="🎨 Вот ваша раскраска!")

    elif input_type == "image":
        file_id = data.get("file_id")
        if not file_id:
            await callback.message.answer("❌ Изображение не найдено.")
            return

        await callback.message.answer("📷 Обработка изображения пока не реализована.")
        # Здесь можно вызвать обработку картинки, если нужно
        # await some_image_handler(file_id)

    await state.clear()


# ✏️ Редактирование ввода
@router.callback_query(F.data == "edit_image")
async def handle_edit(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} chose to edit")
    await state.clear()
    await callback.answer("✏️ Хорошо, отправь новое изображение или описание.")


# ❌ Отмена генерации
@router.callback_query(F.data == "cancel_image")
async def handle_cancel(callback: CallbackQuery, state: FSMContext):
    logger.info(f"User {callback.from_user.id} canceled input")
    await state.clear()
    await callback.answer("❌ Генерация отменена.")
