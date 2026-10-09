
import sqlite3
import secrets
import string
from collections import OrderedDict
from pathlib import Path

DB_PATH = Path(__file__).with_name("smarturl.db")


class LRUCache:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


class URLShortener:
    def __init__(self):
        self.cache = LRUCache(100)
        self.initialize_database()

    def connect(self):
        return sqlite3.connect(DB_PATH)

    def initialize_database(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    short_code TEXT PRIMARY KEY,
                    original_url TEXT NOT NULL,
                    clicks INTEGER DEFAULT 0
                )
            """)

    def shorten_url(self, original_url):
        characters = string.ascii_letters + string.digits

        with self.connect() as conn:
            while True:
                code = "".join(
                    secrets.choice(characters) for _ in range(6)
                )

                exists = conn.execute(
                    "SELECT 1 FROM urls WHERE short_code = ?",
                    (code,)
                ).fetchone()

                if not exists:
                    break

            conn.execute(
                "INSERT INTO urls (short_code, original_url) VALUES (?, ?)",
                (code, original_url)
            )

        self.cache.put(code, original_url)
        return code

    def get_original_url(self, code):
        original_url = self.cache.get(code)

        if original_url is not None:
            return original_url

        with self.connect() as conn:
            row = conn.execute(
                "SELECT original_url FROM urls WHERE short_code = ?",
                (code,)
            ).fetchone()

        if row:
            self.cache.put(code, row[0])
            return row[0]

        return None

    def record_click(self, code):
        with self.connect() as conn:
            conn.execute(
                "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
                (code,)
            )

    def get_stats(self, code):
        with self.connect() as conn:
            row = conn.execute(
                "SELECT original_url, clicks FROM urls WHERE short_code = ?",
                (code,)
            ).fetchone()

        if row:
            return {
                "original_url": row[0],
                "clicks": row[1]
            }

        return None