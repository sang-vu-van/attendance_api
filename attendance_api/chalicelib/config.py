import os


def get_db_url() -> str:
    return os.getenv(
        "DB_URL",
        "mysql+pymysql://attendance_user:attendance@127.0.0.1:3306/attendance_db?charset=utf8mb4",
    )
