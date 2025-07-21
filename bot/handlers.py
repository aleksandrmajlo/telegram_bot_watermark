import os
from aiogram import types
from aiogram.types import BufferedInputFile
from .photo_processor import PhotoProcessor
from service.watermark_photo import WatermarkPhoto
from service.watermark_video import WatermarkKVideo

async def handle_photo(message: types.Message):
    # 1. Найти самое большое фото
    file_id = PhotoProcessor.get_largest_photo(message.photo)
    if not file_id:
        await message.answer("No photo found")
        return

    # 2. Скачать фото с Telegram
    telegram_bot = message.bot
    file = await telegram_bot.get_file(file_id)
    file_bytes = await telegram_bot.download_file(file.file_path)

    logo_path = os.getenv('LOGO_PATH', 'watermark/logo.png')
    watermark_photo = WatermarkPhoto(logo_path)
    watermarked = watermark_photo.add_watermark(file_bytes)

    # 3. Отправить обратно
    photo = BufferedInputFile(watermarked.getvalue(), filename="watermarked.jpg")
    await message.answer_photo(photo=photo)

async def handle_video(message: types.Message): 
    file_id = message.video.file_id

    if not file_id:
        await message.answer("No video found")
        return
    if message.video.file_size > 49 * 1024 * 1024:
        await message.answer("⚠️ Donvald Bot: ваше видео слишком большое (больше 50MB). Пожалуйста, отправьте файл меньшего размера.")
        return    
    # 2. Скачать видео с Telegram
    telegram_bot = message.bot
    file = await telegram_bot.get_file(file_id)
    file_bytes = await telegram_bot.download_file(file.file_path)

    logo_path = os.getenv('LOGO_VIDEO_PATH', 'watermark/logo_video.png')
    watermark_video = WatermarkKVideo(logo_path)
    watermarked = watermark_video.add_watermark(file_bytes)
    # 3. Отправить обратно
    video = BufferedInputFile(watermarked.getvalue(), filename="watermarked.mp4")
    await message.answer_video(video=video)  

async def start(message: types.Message):
    await message.answer("Hello! I'm a bot that can add a watermark to your photo or video.")