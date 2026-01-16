import sqlite3
import time
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path("productivity.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    """Initialize the database with sessions and categories tables."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                start_ts INTEGER NOT NULL,
                end_ts INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        conn.commit()

def get_or_create_category(conn, category_name):
    """Return the category ID, creating it if it doesn't exist."""
    cursor = conn.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    row = cursor.fetchone()
    if row:
        return row[0]

    conn.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
    conn.commit()
    return conn.execute("SELECT id FROM categories WHERE name = ?", (category_name,)).fetchone()[0]


def log_session(session_id, start_ts, end_ts, category_name="uncategorized"):
    """Log a session with optional category. Stores created_at automatically."""
    duration = end_ts - start_ts
    if duration < 0:
        raise ValueError("End time must be after start time")

    with get_connection() as conn:
        category_id = get_or_create_category(conn, category_name)
        conn.execute("""
            INSERT INTO sessions (session_id, start_ts, end_ts, duration, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (session_id, start_ts, end_ts, duration, category_id))
        conn.commit()


def get_all_sessions():
    """Return all sessions with category names and creation timestamp."""
    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT s.session_id, s.start_ts, s.end_ts, s.duration, c.name as category, s.created_at
            FROM sessions s
            JOIN categories c ON s.category_id = c.id
            ORDER BY s.start_ts DESC
        """)
        return cursor.fetchall()



def get_total_time_last_24h():
    """
    Return total time for each category in the past 24 hours,
    including 'Total Productivity'.
    Durations are returned as 'Hh Mm' strings for readability.
    """
    now = datetime.utcnow()
    past_24h_ts = int((now - timedelta(hours=24)).timestamp())  # UNIX timestamp for comparison

    with get_connection() as conn:
        cursor = conn.execute("""
            SELECT c.name as category, SUM(s.duration) as total_duration
            FROM sessions s
            JOIN categories c ON s.category_id = c.id
            WHERE s.created_at >= ?
            GROUP BY c.name
        """, (past_24h_ts,))
        
        result = {}
        total_seconds = 0

        for row in cursor.fetchall():
            category, duration_seconds = row
            if not duration_seconds:
                continue

            # Convert string to int if needed
            duration_seconds = int(duration_seconds)
            total_seconds += duration_seconds

            hours, remainder = divmod(duration_seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            result[category] = f"{hours}h {minutes}m"

        # Add total productivity
        total_hours, remainder = divmod(total_seconds, 3600)
        total_minutes, _ = divmod(remainder, 60)
        result['Total Productivity'] = f"{total_hours}h {total_minutes}m"

        return result