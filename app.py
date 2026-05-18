from flask import Flask, render_template, request, redirect, url_for
from database import init_db, add_review
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Updated Customer Review Page with CSS link
HOME_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>The Urban Bean</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <h1>☕ The Urban Bean</h1>
        <form action="/submit" method="post">
            <label>How many stars?</label>
            <input type="number" name="stars" min="1" max="5" value="5">
            
            <label>Share your experience:</label>
            <textarea name="content" rows="4" required placeholder="The coffee was..."></textarea>
            
            <button type="submit">Submit Review</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return HOME_HTML

@app.route('/submit', methods=['POST'])
def submit():
    content = request.form['content']
    stars = int(request.form['stars'])
    add_review(content, stars, datetime.now().strftime("%Y-%m-%d %H:%M"))
    return f'''
    <link rel="stylesheet" href="/static/style.css">
    <div class="container status-msg">
        <h1>✨ Review Submitted!</h1>
        <p>Thank you for helping us grow.</p>
        <a href="/">← Go Back</a>
    </div>
    '''

@app.route('/admin/reply/<int:review_id>')
def admin_reply_page(review_id):
    conn = sqlite3.connect('reviews.db')
    conn.row_factory = sqlite3.Row
    review = conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
    conn.close()
    
    # We grab the 'suggested' text from the URL (sent by Streamlit)
    suggestion = request.args.get('suggested', '')

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Admin Portal</h1>
            <div class="review-box">
                <p><strong>Customer:</strong> {review['content']}</p>
            </div>
            <form action="/admin/submit_reply/{review_id}" method="post">
                <label>AI Suggested Reply:</label>
                <textarea name="reply_content" rows="5" required>{suggestion}</textarea>
                <button type="submit">Post Reply & Resolve</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/submit_reply/<int:review_id>', methods=['POST'])
def submit_admin_reply(review_id):
    reply = request.form['reply_content']
    conn = sqlite3.connect('reviews.db')
    conn.execute("UPDATE reviews SET status = 'Resolved', reply_content = ? WHERE id = ?", (reply, review_id))
    conn.commit()
    conn.close()
    return f'''
    <link rel="stylesheet" href="/static/style.css">
    <div class="container status-msg">
        <h1>✅ Reply Posted!</h1>
        <p>The review has been moved to resolved.</p>
        <a href="/">Back to Home</a>
    </div>
    '''

if __name__ == '__main__':
    init_db()
    app.run(port=5000, debug=True)