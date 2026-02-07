import asyncio
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from aiogram.filters import CommandStart
from aiogram.filters.state import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# ======================
# НАСТРОЙКИ
# ======================

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан! Вставь токен в переменные окружения Bothost")

REPORT_CHAT_ID = os.getenv("REPORT_CHAT_ID")
if not REPORT_CHAT_ID:
    raise RuntimeError("REPORT_CHAT_ID не задан! Вставь chat_id группы в переменные окружения Bothost")
REPORT_CHAT_ID = int(REPORT_CHAT_ID)  # для супергруппы

BARISTAS = {
    "barista_1": "Бариста 1",
    "barista_2": "Бариста 2",
    "barista_3": "Бариста 3",
}

# ======================
# СОСТОЯНИЯ
# ======================

class Checklist(StatesGroup):
    barista = State()
    dose = State()
    yield_espresso = State()
    time = State()
    acidity = State()
    bitterness = State()
    sweetness = State()
    balance = State()
    comment = State()
    espresso_photo = State()
    showcase_photo = State()

# ======================
# КЛАВИАТУРЫ
# ======================

def barista_keyboard():
    buttons = [[InlineKeyboardButton(text=name, callback_data=key)] for key, name in BARISTAS.items()]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def score_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 6)]]
    )

# ======================
# БОТ
# ======================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ----------------------
# DEBUG ХЭНДЛЕР
# ----------------------
@router.message()
async def debug(message: Message):
    await message.answer(f"Привет! Бот жив. Chat_id: {message.chat.id}")

# ======================
# ХЕНДЛЕРЫ FSM
# ======================

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("☀️ Открытие смены\n\nВыбери бариста:", reply_markup=barista_keyboard())
    await state.set_state(Checklist.barista)

@router.callback_query(StateFilter(Checklist.barista))
async def choose_barista(callback: CallbackQuery, state: FSMContext):
    barista_name = BARISTAS[callback.data]
    await state.update_data(barista=barista_name)
    await callback.message.answer("☕ Дозировка помола (г):")
    await state.set_state(Checklist.dose)
    await callback.answer()

@router.message(StateFilter(Checklist.dose))
async def dose(message: Message, state: FSMContext):
    await state.update_data(dose=message.text)
    await message.answer("☕ Выход эспрессо (г):")
    await state.set_state(Checklist.yield_espresso)

@router.message(StateFilter(Checklist.yield_espresso))
async def yield_espresso(message: Message, state: FSMContext):
    await state.update_data(yield_espresso=message.text)
    await message.answer("⏱ Время пролива (сек):")
    await state.set_state(Checklist.time)

@router.message(StateFilter(Checklist.time))
async def time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.answer("🍋 Кислотность (1–5):", reply_markup=score_keyboard())
    await state.set_state(Checklist.acidity)

@router.callback_query(StateFilter(Checklist.acidity))
async def acidity(callback: CallbackQuery, state: FSMContext):
    await state.update_data(acidity=callback.data)
    await callback.message.answer("🔥 Горечь (1–5):", reply_markup=score_keyboard())
    await state.set_state(Checklist.bitterness)
    await callback.answer()

@router.callback_query(StateFilter(Checklist.bitterness))
async def bitterness(callback: CallbackQuery, state: FSMContext):
    await state.update_data(bitterness=callback.data)
    await callback.message.answer("🍯 Сладость (1–5):", reply_markup=score_keyboard())
    await state.set_state(Checklist.sweetness)
    await callback.answer()

@router.callback_query(StateFilter(Checklist.sweetness))
async def sweetness(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sweetness=callback.data)
    await callback.message.answer("⚖️ Баланс (1–5):", reply_markup=score_keyboard())
    await state.set_state(Checklist.balance)
    await callback.answer()

@router.callback_query(StateFilter(Checklist.balance))
async def balance(callback: CallbackQuery, state: FSMContext):
    await state.update_data(balance=callback.data)
    await callback.message.answer("📝 Комментарий:")
    await state.set_state(Checklist.comment)
    await callback.answer()

@router.message(StateFilter(Checklist.comment))
async def comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await message.answer("📸 Прикрепи фото эспрессо:")
    await state.set_state(Checklist.espresso_photo)

@router.message(StateFilter(Checklist.espresso_photo), F.photo)
async def espresso_photo(message: Message, state: FSMContext):
    await state.update_data(espresso_photo=message.photo[-1].file_id)
    await message.answer("🧁 Прикрепи фото витрины:")
    await state.set_state(Checklist.showcase_photo)

@router.message(StateFilter(Checklist.showcase_photo), F.photo)
async def showcase_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    showcase_photo_id = message.photo[-1].file_id
    now = datetime.now()

    text = (
        "☀️ <b>Открытие смены</b>\n\n"
        f"👤 Бариста: {data['barista']}\n"
        f"📅 {now.strftime('%d.%m.%Y')}\n"
        f"⏰ {now.strftime('%H:%M')}\n\n"
        "☕ <b>Эспрессо:</b>\n"
        f"Доза: {data['dose']} г\n"
        f"Выход: {data['yield_espresso']} г\n"
        f"Время: {data['time']} сек\n\n"
        "⭐ <b>Вкус:</b>\n"
        f"Кислотность: {data['acidity']}/5\n"
        f"Горечь: {data['bitterness']}/5\n"
        f"Сладость: {data['sweetness']}/5\n"
        f"Баланс: {data['balance']}/5\n\n"
        "📝 <b>Комментарий:</b>\n"
        f"{data['comment']}"
    )

    await bot.send_media_group(
        chat_id=REPORT_CHAT_ID,
        media=[
            InputMediaPhoto(media=data["espresso_photo"], caption=text, parse_mode="HTML"),
            InputMediaPhoto(media=showcase_photo_id)
        ]
    )

    await message.answer("✅ Отчёт отправлен. Хорошей смены ☕️")
    await state.clear()

# ======================
# ЗАПУСК
# ======================

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())