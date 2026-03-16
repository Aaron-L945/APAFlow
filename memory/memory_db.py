import sqlite3
import json

class APAFlowMemory:
    def __init__(self, db_path="apaflow_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    domain TEXT,
                    goal TEXT,
                    selector TEXT,
                    action TEXT,
                    value TEXT,
                    success_count INTEGER DEFAULT 1,
                    last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (domain, goal)
                )
            """)

    def save_experience(self, domain, goal, data):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO experiences (domain, goal, selector, action, value)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(domain, goal) DO UPDATE SET
                    selector=excluded.selector,
                    action=excluded.action,
                    value=excluded.value,
                    success_count=success_count + 1,
                    last_used=CURRENT_TIMESTAMP
            """, (domain, goal, data['selector'], data['action'], data.get('value', '')))

    def get_experience(self, domain, goal):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT selector, action, value FROM experiences WHERE domain = ? AND goal = ?",
                (domain, goal)
            )
            row = cursor.fetchone()
            return {"selector": row[0], "action": row[1], "value": row[2]} if row else None