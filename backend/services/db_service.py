import sqlite3
import json
from datetime import datetime

DB_NAME = "cache.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS url_cache (
        url TEXT PRIMARY KEY,
        response TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def get_cached_result(url):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("SELECT response FROM url_cache WHERE url = ?", (url,))
        row = c.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
    except:
        pass

    return None


def save_result(url, result):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""
        INSERT OR REPLACE INTO url_cache (url, response, created_at)
        VALUES (?, ?, ?)
        """, (url, json.dumps(result), datetime.now().isoformat()))

        conn.commit()
        conn.close()
    except:
        pass