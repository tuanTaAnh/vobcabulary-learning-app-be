import sqlite3
from pathlib import Path

DB_PATH = Path("/app/data/vocab.db")


def column_exists(cursor, table_name: str, column_name: str) -> bool:
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return any(column[1] == column_name for column in columns)


def table_exists(cursor, table_name: str) -> bool:
    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = ?
        """,
        (table_name,),
    )
    return cursor.fetchone() is not None


def main():
    if not DB_PATH.exists():
        print(f"Database not found at {DB_PATH}")
        print("Nothing to migrate.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO collections (name, description, created_at)
        SELECT
            'General',
            'Default collection for existing words',
            CURRENT_TIMESTAMP
        WHERE NOT EXISTS (
            SELECT 1 FROM collections WHERE name = 'General'
        )
        """
    )

    if not table_exists(cursor, "vocab"):
        print("Table vocab does not exist yet.")
        conn.commit()
        conn.close()
        return

    if not column_exists(cursor, "vocab", "collection_id"):
        print("Adding column vocab.collection_id ...")
        cursor.execute("ALTER TABLE vocab ADD COLUMN collection_id INTEGER")
    else:
        print("Column vocab.collection_id already exists.")

    cursor.execute("SELECT id FROM collections WHERE name = 'General'")
    default_collection = cursor.fetchone()

    if default_collection:
        default_collection_id = default_collection[0]

        cursor.execute(
            """
            UPDATE vocab
            SET collection_id = ?
            WHERE collection_id IS NULL
            """,
            (default_collection_id,),
        )

    conn.commit()
    conn.close()

    print("Collections migration completed.")


if __name__ == "__main__":
    main()