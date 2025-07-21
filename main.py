import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import asyncio
from bot.handlers import handle_photo, start

async def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')

    bot = Bot(telegram_token)
    dp = Dispatcher(storage=MemoryStorage())

    # Start
    dp.message.register(start, Command("start"))

    # Photo
    dp.message.register(handle_photo, lambda msg: msg.photo)


    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())