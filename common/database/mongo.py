import pymongo

"""
MongoDB is used for a cart operations which located in directory 'services/cart'
"""

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

""" store db """
mdb = myclient["bosch-store"]
