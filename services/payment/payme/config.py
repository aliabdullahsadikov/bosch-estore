import os

config = None

PAYME_SETTINGS = {
    'DEBUG': True,  # True - test mode, False - production mode
    'ID': '',
    'SECRET_KEY': 'B@24m@bvvR0D64RxRJd@XHC2?PpmFAK%#SmY',
    "MERCHANT_USERNAME": os.getenv("PAYME_MERCHANT_USERNAME", "login"),
    "MERCHANT_PASSWORD": os.getenv("PAYME_MERCHANT_PASSWORD", "B@24m@bvvR0D64RxRJd@XHC2?PpmFAK%#SmY"),
    'ACCOUNTS': {
        'KEY_1': 'order_id',
        'KEY_2': '',
    },
    "ALLOWED_HOSTS": [
        '185.178.51.131',
        '185.178.51.132',
        '195.158.31.134',
        '195.158.31.10',
        '195.158.28.124',
        '195.158.5.82',
    ]

}