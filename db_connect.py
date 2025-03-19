import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker

load_dotenv()

def connect_unix_socket() -> sqlalchemy.engine.base.Engine:
    """Initializes a Unix socket connection pool for a Cloud SQL instance of MySQL."""
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]

    if os.name !="nt":
        unix_socket_path = "/cloudsql/{}".format(os.environ["INSTANCE_CONNECTION_NAME"])
        pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username=db_user,
                password=db_pass,
                database=db_name,
                query={"unix_socket": unix_socket_path},
            ),
        )
    else :
        db_host = os.environ.get("DB_HOST","127.0.0.1")
        pool = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username=db_user,
                password=db_pass,
                host=db_host,
                port=3060,
                database=db_name,
            )
        )
    return pool

# Create the engine and session factory
engine = connect_unix_socket()
Session = sessionmaker(bind=engine)
session = Session()