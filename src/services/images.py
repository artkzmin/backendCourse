import shutil
from fastapi import UploadFile, BackgroundTasks
from src.services.base import BaseService
from src.tasks.tasks import resize_image_without_decorator


class ImageService(BaseService):
    def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks):
        image_path = f"src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)
        background_tasks.add_task(resize_image_without_decorator, image_path)
