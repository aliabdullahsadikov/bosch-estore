import datetime
import os.path
from abc import ABC, abstractmethod, abstractproperty
from fastapi import UploadFile

from common.config import DEVELOPMENT_CONFIGS

img_conf = DEVELOPMENT_CONFIGS["image_conf"]


class ImgManagerAbc(ABC):

    def __init__(
        self,
        app_photo_path: str = img_conf["default_path"],
        img_type: str = None,
        prefix: str = None,
        default_img: dict = img_conf["default_images"]["common"]
    ):
        self.app_photo_path = app_photo_path
        self.img_type = img_type
        self.prefix = prefix
        self.default_img = default_img
        self.file_name = "/" + self.prefix + str(datetime.datetime.now()) + ".jpg"

    @property
    def full_path(self):
        return os.path.abspath(self.app_photo_path)+self.img_type

    def generate_file_name(self, addition=""):
        return "/" + self.prefix + str(datetime.datetime.now()) + addition + ".jpg"

    # @property
    # def full_path_name(self):
    #     return self.full_path + self.file_name

    @property
    def file_path_for_db(self):
        if self.img_type:
            return self.img_type+self.file_name
        return self.default_img

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def reject(self):
        pass

    @abstractmethod
    def delete(self):
        pass


