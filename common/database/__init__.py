
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from common.config import config

DATABASE_URL = config["DATABASE_URL_POSTGRES"]

engine = sqlalchemy.create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



"""
Importing models from whole modules in order to explore database.
common.models file is role as gateway for all models as well as all models in the services gathered into this file.
"""
from common import models


# Create the tables in the database
Base.metadata.create_all(engine)









#
# database = databases.Database(DATABASE_URL)
#
# metadata = sqlalchemy.MetaData()


#
# engine = sqlalchemy.create_engine(DATABASE_URL)
# metadata.create_all(engine)




