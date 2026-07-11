import json
import sqlite3
import os
from data.migrations import MIGRATIONS
from entity.creature import Creature
from datetime import datetime

DB_PATH = './data/creature.db'


# connects to db or creates it if it doesn't exist
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()

    current_version = cursor.execute("PRAGMA user_version").fetchone()[0]
    target_version = len(MIGRATIONS)
    # create table if it doesn't exist, uses only 1d 1 because there will only ever be 1 creature
    while current_version < target_version:
        MIGRATIONS[current_version](cursor)
        current_version += 1
        cursor.execute(f"PRAGMA user_version = {current_version}")
    
    
    conn.commit()
    conn.close()

def save_creature(creature):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO creature (id, name, species, age, energy, fullness, happiness, memory_json, known_tricks_json, created_at, last_interaction, last_decay_check)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        creature.name,
        creature.species,
        creature.age,
        creature.energy,
        creature.fullness,
        creature.happiness,
        json.dumps(creature.memory),
        json.dumps(creature.known_tricks),
        creature.created_at.isoformat(),
        creature.last_interaction.isoformat(),
        creature.last_decay_check.isoformat()
    ))
    conn.commit()
    conn.close()

def load_creature():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name, species, age, energy, fullness, happiness, memory_json, known_tricks_json, created_at, last_interaction, last_decay_check FROM creature WHERE id = 1')
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                'name': row[0],
                'species': row[1],
                'age': row[2],
                'energy': row[3],
                'fullness': row[4],
                'happiness': row[5],
                'memory': json.loads(row[6]),
                'known_tricks': json.loads(row[7]),
                'created_at': row[8],
                'last_interaction': row[9],
                'last_decay_check': row[10]
            }
        else:
            return None
    except sqlite3.DatabaseError as e:
        handle_corrupted_db()
        raise RuntimeError("Database was corrupted and has been reset. Please restart the application to create a new creature.") from e
    
def handle_corrupted_db():
    os.remove('./data/creature.db')
    initialize_db()

def row_to_creature(row):
    return Creature(
        name=row['name'],
        species=row['species'],
        age=row['age'],
        energy=row['energy'],
        fullness=row['fullness'],
        happiness=row['happiness'],
        memory=row['memory'],
        known_tricks=row['known_tricks'],
        created_at=datetime.fromisoformat(row['created_at']),
        last_interaction=datetime.fromisoformat(row['last_interaction']),
        last_decay_check=datetime.fromisoformat(row['last_decay_check'])
    )

def delete_creature():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM creature WHERE id = 1')
    conn.commit()
    conn.close()