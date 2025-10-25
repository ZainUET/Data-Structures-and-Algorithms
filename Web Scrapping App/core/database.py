# core/database.py
import sqlite3
import os

class ProjectDatabase:
    def __init__(self, db_path="data/project.db"):
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables for storing entities with all required columns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Drop the table if it exists to recreate with new schema
        cursor.execute('DROP TABLE IF EXISTS books')
        
        # Main entities table with ALL required columns
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                isbn TEXT,
                publisher TEXT,
                publication_year INTEGER,
                category TEXT,
                price REAL,
                rating REAL,
                page_count INTEGER,
                language TEXT,
                description TEXT,
                stock_quantity INTEGER,
                format_type TEXT,
                scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_url TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully!")
    
    def get_all_entities(self):
        """Retrieve all entities from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books')
        entities = cursor.fetchall()
        
        conn.close()
        return entities
    
    def get_entity_count(self):
        """Get total number of entities"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM books')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count