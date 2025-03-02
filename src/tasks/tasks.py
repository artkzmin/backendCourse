import os
import asyncio
import logging
from PIL import Image

from time import sleep
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@celery_instance.task
def test_task():
    sleep(5)
    print("Task выполнен")


def resize_image_without_decorator(image_path: str):
    logging.debug(f"Вызывается функция с image_path={image_path}")
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"
    # Открываем изображение
    img = Image.open(image_path)
    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )
        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"
        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)
        # Сохраняем изображение
        img_resized.save(output_path)
    logging.info(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")


@celery_instance.task
def resize_image(image_path: str):
    resize_image_without_decorator(image_path)


async def get_bookings_with_today_checkin_helper():
    print("RUNNING")
    async with DBManager(async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        logging.debug(f"{bookings}=")


@celery_instance.task(name="booking_today_checkin")
def send_emails_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
