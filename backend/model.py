import sqlite3
from pathlib import Path

DATABASE = Path(__file__).parent / "pomodoro.db"

def get_db():
    """
    FastAPI dependency that provides a database connection
    per request and ensures it is properly closed.
    """

    connection = sqlite3.connect(DATABASE, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
    finally:
        connection.commit()
        connection.close()