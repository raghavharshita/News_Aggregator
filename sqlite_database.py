import sqlite3

conn = sqlite3.connect('news_data.db')

cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS news_table(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    summary TEXT,
    category TEXT,
    publication_date TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
