import os
from aiogram import types
from aiogram.types import BufferedInputFile
from .photo_processor import PhotoProcessor
from service.watermark_photo import WatermarkPhoto


async def handle_photo(message: types.Message):
    # 1. Найти самое большое фото
    file_id = PhotoProcessor.get_largest_photo(message.photo)
    print(f"Found file ID: {file_id}")
    if not file_id:
        await message.answer("No photo found")
        return

    # 2. Скачать фото с Telegram
    telegram_bot = message.bot
    file = await telegram_bot.get_file(file_id)
    file_bytes = await telegram_bot.download_file(file.file_path)

    logo_path = os.getenv('LOGO_PATH', 'logo.png')
    watermark_photo = WatermarkPhoto(logo_path)
    watermarked = watermark_photo.add_watermark(file_bytes)

    # 3. Отправить обратно
    photo = BufferedInputFile(watermarked.getvalue(), filename="watermarked.jpg")
    await message.answer_photo(photo=photo)

async def start(message: types.Message):
    await message.answer("Hello! I'm a bot that can add a watermark to your photo.")