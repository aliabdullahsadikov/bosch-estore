import os

from services.payment.payme.config import PAYME_SETTINGS


def config(env: str = None):
    if env == "prod":
        return PRODACTION_CONFIGS

    return DEVELOPMENT_CONFIGS


def collect_allowed_hosts():
    """
    It intended to gather all allowed hosts
    including from the environment as app-allowed hosts and Payme service.
    :return:
    """
    if os.getenv("ALLOWED_HOSTS") and isinstance(os.getenv("ALLOWED_HOSTS"), list):
        return PAYME_SETTINGS["ALLOWED_HOSTS"] + os.getenv("ALLOWED_HOSTS")

    return PAYME_SETTINGS["ALLOWED_HOSTS"]


DEVELOPMENT_CONFIGS = {
    "DATABASE_URL_POSTGRES": "postgresql://ali:131313ali@localhost:5432/shop-bosch-2",
    "DATABASE_URL_POSTGRES_FOR_TESTING": "postgresql://ali:131313ali@localhost:5432/shop-bosch-test_db",
    "ALLOWED_HOSTS": collect_allowed_hosts(),


    "image_conf": {
        "default_path": "common/static/photo",
        "image_type": {
            "category": "/category",
            "product": "/product"
        },
        "image_prefix": {
            "product": "prod:",
            "category": "cat:"
        },
        "default_images": {
            "common": {
                "sm": "default_img_sm.jpg",
                "md": "default_img_md.jpg",
                "lg": "default_img_lg.jpg",
            },
            "category": {
                "sm": "category_default_img_sm.jpg",
                "md": "category_default_img_md.jpg"
            },
            "product": {
                "sm": "product_default_img_sm.jpg",
                "md": "product_default_img_md.jpg",
                "lg": "product_default_img_lg.jpg",
            }
        }
    }
}


PRODACTION_CONFIGS = {
    "DATABASE_URL_POSTGRES": os.getenv("DATABASE_URL", "not defined"),
    "ALLOWED_HOSTS": collect_allowed_hosts()
}

config = config(os.getenv("ENV", "dev"))

USER_STATUS = {
    "new": 0,
    "active": 1,
    "deactivated": -1,
    "deleted": -2
}
