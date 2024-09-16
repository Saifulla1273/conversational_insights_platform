import sqlite3

def init_db():
    conn = sqlite3.connect('db/insights.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS insights (
                    id INTEGER PRIMARY KEY,
                    file_name TEXT,
                    transcription TEXT,
                    topics TEXT,
                    sentiment TEXT,
                    insights TEXT
                )''')
    conn.commit()
    conn.close()

def save_insights(file_name, transcription, topics, sentiment, insights):
    conn = sqlite3.connect('db/insights.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO insights (file_name, transcription, topics, sentiment, insights)
                   VALUES (?, ?, ?, ?, ?)''', 
                   (file_name, transcription, topics, sentiment, insights))
    conn.commit()
    conn.close()
