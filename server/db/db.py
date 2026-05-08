import sqlite3
import sqlite3
from contextlib import contextmanager

DB_PATH = "app.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()