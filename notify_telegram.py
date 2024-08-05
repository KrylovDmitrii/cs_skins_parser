import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from finder_utils import finder_main

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if API_TOKEN is None or CHAT_ID is None:
    raise ValueError("API_TOKEN или TELEGRAM_CHAT_ID отсутсвуют в окружении")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! "
                         f"Я бот для мониторинга скинов на сайте lis-skins")


async def send_skin_notifications() -> None:
    skin_to_send = finder_main()
    if not skin_to_send:
        return

    for category, skins in skin_to_send.items():
        if not skins:
            continue

        message_text = f"Категория: {category}\n"
        for skin, description in skins:
            message_text += f"Скин: {skin}\nПричина: {description}\n\n"

        await bot.send_message(CHAT_ID, message_text)


async def periodic_update() -> None:
    while True:
        await send_skin_notifications()
        await asyncio.sleep(60)


async def main() -> None:
    task1 = dp.start_polling(bot)
    task2 = periodic_update()
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
