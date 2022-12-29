import datetime
import os
from typing import Union

from fastapi import UploadFile, File

PHOTO_TYPE = {
    "category": "/category",
    "product": "/product"
}

PHOTO_PREFIX = {
    "product": "prod:",
    "category": "cat:"
}


def save_photo(path: str, mode: str, file: UploadFile) -> str:
    path_file, file_name = get_full_file_path(path, mode)

    with open(path_file, "wb+") as new_file:
        new_file.write(file.file.read())

    return mode+f"/{PHOTO_PREFIX['category']}" + file_name


def delete_photo(path: str, filenames: list) -> bool:
    for filename in filenames:
        file = os.path.abspath(path) + filename
        if os.path.exists(file):
            os.remove(file)

        #  should add logging
    return True


def get_full_file_path(path, mode):
    # file_extension = file.filename[file.filename.rfind("."):]
    # file_name = f"category:{self.payload['name']}_{datetime.datetime.now()}{file_extension}"

    file_name = str(datetime.datetime.now()) + ".jpg"
    _path = os.path.abspath(path)
    path_file = _path + mode + f"/{PHOTO_PREFIX['category']}" + file_name

    return path_file, file_name


def reject_photo(path: str, mode: str, filename: str = "") -> bool:
    if os.path.exists(path+mode+filename):
        os.remove(path+mode+filename)
    else:
        return False  # Photo has not exists!

    return True
