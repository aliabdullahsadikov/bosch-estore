from common.database.mongo import mdb


""" define cart collection """
Cart = mdb["cart"]

"""

default schema of cart collection:

{
    "user_id": 1133,
    "total": 13000,
    "ordered": True/False,
    "status": 0/1/2
    "created_at": date-time,
    "items": [
        {
            "product_id": 13
            "product_name": "Mixer",
            "article": 12345,
            "price": 1000,
            "amount": 2,
            "total_price": 2000
            
        },
        {
            ...
        }
    ]
}

"""