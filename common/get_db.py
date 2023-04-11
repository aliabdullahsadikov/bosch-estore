from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker

@contextmanager
def get_db():
    from common.database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
