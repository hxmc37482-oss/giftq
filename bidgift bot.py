import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8808324194:AAGaYRJxEbCW01_GLnuv8cAIeWdqCUnL8x8"
CHANNEL_INVITE = "https://t.me/+rTIsSbfkngUwZGNi"
# Укажи username или ID канала (бот должен быть админом)
# Формат: @username или числовой ID (например -1001234567890)
CHANNEL_ID = "@bidgift_channel"  # ← ЗАМЕНИ НА РЕАЛЬНЫЙ USERNAME ИЛИ ID ТВОЕГО КАНАЛА

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Хранилище пользователей, подавших заявку (user_id -> True)
pending_users: dict[int, bool] = {}


def get_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📩 Подать заявку в канал", url=CHANNEL_INVITE)],
        [InlineKeyboardButton(text="✅ Проверить заявку", callback_data="check_request")]
    ])


def get_check_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Проверить заявку", callback_data="check_request")]
    ])


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет что бы получить мишку автоматически надо подать заявку в канал ниже.",
        reply_markup=get_start_keyboard()
    )


@dp.chat_join_request()
async def on_join_request(update: ChatJoinRequest):
    """Срабатывает когда кто-то подаёт заявку на вступление в канал."""
    user_id = update.from_user.id
    pending_users[user_id] = True
    logger.info(f"Новая заявка от пользователя {user_id} (@{update.from_user.username})")


@dp.callback_query(F.data == "check_request")
async def check_request(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if pending_users.get(user_id):
        # Заявка есть — сообщаем об ожидании
        await callback.message.edit_text(
            "Привет что бы получить мишку автоматически надо подать заявку в канал ниже.\n\n"
            "⏳ Ожидайте принятие заявки в канал, мишка будет отправлен после принятия.",
            reply_markup=get_check_keyboard()
        )
    else:
        # Заявки нет — предлагаем подать
        await callback.message.edit_text(
            "Привет что бы получить мишку автоматически надо подать заявку в канал ниже.\n\n"
            "❌ Заявка не найдена. Пожалуйста, подай заявку на вступление в канал и нажми кнопку снова.",
            reply_markup=get_start_keyboard()
        )

    await callback.answer()


async def main():
    logger.info("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
