import sqlite3


class ChatDatabase:

    def __init__(self, db_name="chat_history.db"):
        self.conn = sqlite3.connect(
            db_name,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT
            )
        """)

        self.conn.commit()

    def save_message(self, role, message):
        self.cursor.execute(
            "INSERT INTO chat_history(role, message) VALUES(?, ?)",
            (role, message)
        )

        self.conn.commit()

    def get_messages(self):

        self.cursor.execute(
            "SELECT role, message FROM chat_history ORDER BY id"
        )

        return self.cursor.fetchall()

    def clear_history(self):

        self.cursor.execute(
            "DELETE FROM chat_history"
        )

        self.conn.commit()


db = ChatDatabase()