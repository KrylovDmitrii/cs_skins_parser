import os
import sys
import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from finder_utils import finder_main
from collect_skin_info import fetch_and_save_data
from constants import BASE_URL

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

    try:
        with open('data/skins_data/sent_skins.json', 'r', encoding='utf-8') as file:
            sent_skins = json.load(file)
    except FileNotFoundError:
        sent_skins = {}

    new_skins = {}
    for category, skins in skin_to_send.items():
        if not skins:
            continue

        new_skins[category] = []
        for skin, description in skins:
            skin_id = skin.get('Ссылка на товар', '')
            if skin_id not in sent_skins:
                new_skins[category].append((skin, description))
                sent_skins[skin_id] = True

    with open('data/skins_data/sent_skins.json', 'w', encoding='utf-8') as file:
        json.dump(sent_skins, file, ensure_ascii=False, indent=4)

    for category, skins in new_skins.items():
        if not skins:
            continue

        message_text = f"Категория: {category}\n"
        for skin, description in skins:
            message_text += f"Скин: {skin}\nПричина: {description}\n\n"

        await bot.send_message(CHAT_ID, message_text)


async def periodic_update() -> None:
    while True:
        await fetch_and_save_data(base_url=BASE_URL, sorted_by_hot=True, pages=3)
        await send_skin_notifications()
        await asyncio.sleep(120)


async def main() -> None:
    task1 = dp.start_polling(bot)
    task2 = periodic_update()
    await asyncio.gather(task1, task2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
