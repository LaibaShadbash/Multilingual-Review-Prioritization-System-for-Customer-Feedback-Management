import sqlite3

def add_reply_column():
    conn = sqlite3.connect('reviews.db')
    try:
        
        conn.execute("ALTER TABLE reviews ADD COLUMN reply_content TEXT")
        conn.commit()
        print("Success: 'reply_content' column added to reviews.db!")
    except sqlite3.OperationalError:
        print("Note: 'reply_content' column already exists.")
    finally:
        conn.close()

if __name__ == "__main__":
    add_reply_column()