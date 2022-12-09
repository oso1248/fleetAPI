from .. config import settings
# psycopg2 connection
import psycopg2
from psycopg2.extras import RealDictCursor
import time
# sqlalchemy connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# psycopg2 connection
while True:
    try:
        conn = psycopg2.connect(host=settings.DATABASE_HOST,
                                database=settings.DATABASE_NAME,
                                user=settings.DATABASE_USERNAME,
                                password=settings.DATABASE_PASSWORD,
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print(f"Error: {error}")
        time.sleep(5)


# sqlalchemy connection
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()