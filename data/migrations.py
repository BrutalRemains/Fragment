# migrations are handled explicitly through functions, as little db management is actually needed for this project

def migration_001_create_creature_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS creature (
            id INTEGER PRIMARY KEY CHECK (id = 1), 
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            age INTEGER NOT NULL DEFAULT 0,
            energy INTEGER NOT NULL DEFAULT 100,
            fullness INTEGER NOT NULL DEFAULT 100,
            happiness INTEGER NOT NULL DEFAULT 100,
            memory_json TEXT NOT NULL DEFAULT '[]',
            known_tricks_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL,
            last_interaction TEXT NOT NULL,
            last_decay_check TEXT NOT NULL
        )
    ''')

def migration_002_create_creature_events_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS creature_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creature_id INTEGER NOT NULL,
            action_type TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_creature_events_created_at
        ON creature_events(created_at)
    """)


MIGRATIONS = [
    migration_001_create_creature_table,
    migration_002_create_creature_events_table
]