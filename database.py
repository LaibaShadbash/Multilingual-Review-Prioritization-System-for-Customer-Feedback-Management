import sqlite3

def init_db():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    # status: 'Pending' or 'Resolved'
    # reply_content: Stores the business response
    c.execute('''CREATE TABLE IF NOT EXISTS reviews 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  content TEXT, stars INTEGER, date TEXT, 
                  reply_content TEXT, status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

def add_review(content, stars, date):
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute("INSERT INTO reviews (content, stars, date) VALUES (?, ?, ?)", 
              (content, stars, date))
    conn.commit()
    conn.close()