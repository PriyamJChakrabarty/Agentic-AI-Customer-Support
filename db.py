from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("TIDB_HOST")
PORT = int(os.getenv("TIDB_PORT", 4000))
USER = os.getenv("TIDB_USER")
PASSWORD = os.getenv("TIDB_PASSWORD")
DB_NAME = os.getenv("TIDB_DB_NAME")
CA_PATH = os.getenv("CA_PATH")

connect_args = {
    "ssl": {
        "ca": CA_PATH,
        "check_hostname": True,
    }
}

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?charset=utf8mb4",
    connect_args=connect_args,
    pool_pre_ping=True,
    future=True,
)

if __name__ == "__main__":
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()")).scalar()
        print("Connected to TiDB Cloud, server time:", result)
