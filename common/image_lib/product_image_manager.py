import os
import copy
from abc import abstractmethod
from PIL import Image

from fastapi import UploadFile
from common.image_lib.image_manager import ImgManagerAbc
from common.config import DEVELOPMENT_CONFIGS


img_conf = DEVELOPMENT_CONFIGS["image_conf"]

PHOTO_SIZE = {
        "sm": (100, 80),
        "md": (600, 400),
        "lg": (1024, 768)
    }


class ProductImgManager(ImgManagerAbc):

    def __init__(self, file_obj: UploadFile, size: tuple):
        self.file_obj = copy.deepcopy(file_obj)
        self.size = size
        super(ProductImgManager, self).__init__(
            img_type=img_conf["image_type"]["product"],
            prefix=img_conf["image_prefix"]["product"]
        )

    def save(self):
        new_name = self.generate_file_name(f"{self.size[0]}")

        with open(self.full_path+new_name, "wb+") as new_file:
            new_file.write(self.file_obj.file.read())

        image = Image.open(self.full_path+new_name)
        new = image.resize(self.size)
        new.save(self.full_path+new_name)

        return self.img_type+new_name

    def reject(self):
        if os.path.exists(self.full_path + self.file_name):
            os.remove(self.full_path + self.file_name)
        else:
            return False  # Photo has not exists!

        return True  # Deleted

    def delete(self):
        pass

