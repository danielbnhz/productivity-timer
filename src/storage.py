import sqlite3
import time
from pathlib import Path

DB_PATH = Path("productivity.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                start_ts INTEGER NOT NULL,
                end_ts INTEGER NOT NULL,
                duration INTEGER NOT NULL
            )
        """)
        conn.commit()


def log_session(session_id, start_ts, end_ts):
    duration = end_ts - start_ts

    if duration < 0:
        raise ValueError("End time must be after start time")

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO sessions (session_id, start_ts, end_ts, duration)
            VALUES (?, ?, ?, ?)
        """, (session_id, start_ts, end_ts, duration))
        conn.commit()


def get_all_sessions():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT session_id, start_ts, end_ts, duration
            FROM sessions
            ORDER BY start_ts DESC
        """)
        return cursor.fetchall()


def get_total_time():
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT SUM(duration) FROM sessions
        """)
        result = cursor.fetchone()[0]
        return result or 0
