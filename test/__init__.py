from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api_gateway import app
from common.database import Base, get_db
from common.config import config

engine = create_engine(
    config["DATABASE_URL_POSTGRES_FOR_TESTING"]
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """ Get session function for testing """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

test = TestClient(app)
""" Now ready to testing with the test db not an original """



