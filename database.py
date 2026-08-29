import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "tasks.db"


class Database:
    """Handles SQLite database operations."""

    def __init__(self, db_path=DB_PATH):
        self.db_path = str(db_path)
        self.initialize()

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        try:
            yield conn
            conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    def initialize(self):
        with self.connection() as conn:

            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    title TEXT NOT NULL,

                    description TEXT DEFAULT '',

                    category TEXT DEFAULT 'General',

                    priority TEXT NOT NULL DEFAULT 'Medium',

                    deadline TEXT NOT NULL,

                    status TEXT NOT NULL DEFAULT 'Pending',

                    created_at TEXT NOT NULL,

                    completed_at TEXT
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_deadline
                ON tasks(deadline)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_status
                ON tasks(status)
            """)

    def add_task(self, task):

        with self.connection() as conn:

            cursor = conn.execute("""
                INSERT INTO tasks
                (
                    title,
                    description,
                    category,
                    priority,
                    deadline,
                    status,
                    created_at
                )

                VALUES (?, ?, ?, ?, ?, 'Pending', ?)
            """, (

                task["title"],
                task["description"],
                task["category"],
                task["priority"],
                task["deadline"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ))

            return cursor.lastrowid

    def update_task(self, task_id, task):

        with self.connection() as conn:

            conn.execute("""
                UPDATE tasks

                SET
                    title=?,
                    description=?,
                    category=?,
                    priority=?,
                    deadline=?

                WHERE id=?
            """, (

                task["title"],
                task["description"],
                task["category"],
                task["priority"],
                task["deadline"],
                task_id

            ))

    def delete_task(self, task_id):

        with self.connection() as conn:

            conn.execute(
                "DELETE FROM tasks WHERE id=?",
                (task_id,)
            )

    def set_status(self, task_id, completed):

        with self.connection() as conn:

            if completed:

                conn.execute("""
                    UPDATE tasks

                    SET
                        status='Completed',
                        completed_at=?

                    WHERE id=?
                """, (

                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    task_id

                ))

            else:

                conn.execute("""
                    UPDATE tasks

                    SET
                        status='Pending',
                        completed_at=NULL

                    WHERE id=?
                """, (task_id,))

    def get_task(self, task_id):

        with self.connection() as conn:

            return conn.execute(
                "SELECT * FROM tasks WHERE id=?",
                (task_id,)
            ).fetchone()

    def get_tasks(
        self,
        search="",
        status="All",
        priority="All",
        category="All"
    ):

        query = """
            SELECT *
            FROM tasks
            WHERE 1=1
        """

        params = []

        if search:

            query += """
                AND (
                    title LIKE ?
                    OR description LIKE ?
                    OR category LIKE ?
                )
            """

            value = f"%{search}%"

            params.extend([
                value,
                value,
                value
            ])

        if status != "All":

            query += " AND status=?"

            params.append(status)

        if priority != "All":

            query += " AND priority=?"

            params.append(priority)

        if category != "All":

            query += " AND category=?"

            params.append(category)

        query += """
            ORDER BY

            CASE priority

                WHEN 'High' THEN 1

                WHEN 'Medium' THEN 2

                ELSE 3

            END,

            deadline ASC
        """

        with self.connection() as conn:

            return conn.execute(
                query,
                params
            ).fetchall()

    def get_categories(self):

        with self.connection() as conn:

            rows = conn.execute("""
                SELECT DISTINCT category
                FROM tasks
                ORDER BY category
            """).fetchall()

            return [
                row["category"]
                for row in rows
            ]

    def get_statistics(self):

        with self.connection() as conn:

            total = conn.execute("""
                SELECT COUNT(*) AS count
                FROM tasks
            """).fetchone()["count"]

            completed = conn.execute("""
                SELECT COUNT(*) AS count
                FROM tasks

                WHERE status='Completed'
            """).fetchone()["count"]

            pending = conn.execute("""
                SELECT COUNT(*) AS count
                FROM tasks

                WHERE status='Pending'
            """).fetchone()["count"]

            today = datetime.now().strftime(
                "%Y-%m-%d"
            )

            overdue = conn.execute("""
                SELECT COUNT(*) AS count
                FROM tasks

                WHERE
                    status='Pending'
                    AND deadline < ?
            """, (today,)).fetchone()["count"]

            high = conn.execute("""
                SELECT COUNT(*) AS count
                FROM tasks

                WHERE
                    status='Pending'
                    AND priority='High'
            """).fetchone()["count"]

            completion_rate = (
                completed / total * 100
                if total
                else 0
            )

            return {

                "total": total,

                "completed": completed,

                "pending": pending,

                "overdue": overdue,

                "high": high,

                "rate": completion_rate

            }