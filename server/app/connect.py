import os
import time
import psycopg2
from urllib.parse import urlparse
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv


def wait_for_db(db_url):
    result = urlparse(db_url)
    dbname = result.path[1:]
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            conn.close()
            return
        except psycopg2.OperationalError:
            print("Postgres is not ready yet. Waiting...")
            time.sleep(1)


load_dotenv()

DATABASE_URL = os.getenv("DOCKER_DATABASE_URL")
print(DATABASE_URL)

wait_for_db(DATABASE_URL)

engine = create_engine(DATABASE_URL)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
