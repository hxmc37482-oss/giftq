import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8808324194:AAGaYRJxEbCW01_GLnuv8cAIeWdqCUnL8x8"
CHANNEL_INVITE = "https://t.me/+rTIsSbfkngUwZGNi"
CHANNEL_ID = -1003717805514

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# user_id тех, кто подал заявку
pending_users: set[int] = set()


def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📬 Подать заявку", url=CHANNEL_INVITE)],
        [InlineKeyboardButton(text="🔍 Проверить заявку", callback_data="check")]
    ])


def kb_check() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Проверить ещё раз", callback_data="check")]
    ])


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "🐻 <b>Привет!</b>\n\n"
        "Чтобы получить мишку автоматически — подай заявку на вступление в наш канал.\n\n"
        "👇 Нажми кнопку ниже и отправь заявку, затем вернись и нажми <b>«Проверить заявку»</b>.",
        reply_markup=kb_start(),
        parse_mode="HTML"
    )


@dp.chat_join_request()
async def on_join_request(update: ChatJoinRequest):
    """Срабатывает в реальном времени когда пользователь подаёт заявку в канал."""
    if update.chat.id == CHANNEL_ID:
        user_id = update.from_user.id
        pending_users.add(user_id)
        logger.info(f"✅ Заявка от {user_id} ({update.from_user.full_name})")


@dp.callback_query(F.data == "check")
async def check_request(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    if user_id in pending_users:
        await callback.message.edit_text(
            "🐻 <b>Заявка найдена!</b>\n\n"
            "⏳ Ожидайте принятия заявки в канал.\n"
            "Как только вас примут — мишка будет отправлен автоматически! 🎁",
            reply_markup=kb_check(),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            "🐻 <b>Привет!</b>\n\n"
            "Чтобы получить мишку автоматически — подай заявку на вступление в наш канал.\n\n"
            "❗️ Заявка пока не обнаружена.\n"
            "👇 Нажми <b>«Подать заявку»</b>, вступи в канал и вернись сюда.",
            reply_markup=kb_start(),
            parse_mode="HTML"
        )

    await callback.answer()


async def main():
    logger.info("🤖 BidGift бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
