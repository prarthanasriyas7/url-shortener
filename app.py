from flask import Flask, request, jsonify, redirect
import sqlite3
import random
import string
from datetime import datetime, date

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE,
            long_url TEXT UNIQUE,
            click_count INTEGER DEFAULT 0,
            click_limit INTEGER DEFAULT NULL,
            expiry_date TEXT DEFAULT NULL,
            created_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generate_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=6))
    number = str(random.randint(100, 999))
    return code + number

def is_url_expired(click_count, click_limit, expiry_date):
    """Returns True if expired by date OR click limit reached"""
    if expiry_date:
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
        if date.today() > expiry:
            return True
    if click_limit is not None:
        if click_count >= click_limit:
            return True
    return False



# API 1 — POST /shorten — Create short URL

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({"error": "Please provide a URL"}), 400

    long_url = data['url']
    click_limit = data.get('click_limit', None)
    expiry_date = data.get('expiry_date', None)

    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT short_code, click_count, click_limit, expiry_date FROM urls WHERE long_url = ?',
        (long_url,)
    )
    existing = cursor.fetchone()

    if existing:
        old_code, old_click_count, old_click_limit, old_expiry_date = existing
        expired = is_url_expired(old_click_count, old_click_limit, old_expiry_date)

        if not expired:
            # Still active -> return SAME code
            conn.close()
            short_url = f"http://localhost:5000/{old_code}"
            return jsonify({
                "short_url": short_url,
                "code": old_code,
                "message": "URL already exists and is still active!"
            }), 200
        else:
            # Expired -> generate NEW code, use NEW click_limit/expiry_date from this request
            new_code = generate_code()
            new_created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                '''UPDATE urls 
                SET short_code = ?, click_count = 0, click_limit = ?, 
                    expiry_date = ?, created_date = ?
                WHERE long_url = ?''',
                (new_code, click_limit, expiry_date, new_created_date, long_url)
            )
            conn.commit()
            conn.close()

            short_url = f"http://localhost:5000/{new_code}"
            return jsonify({
                "short_url": short_url,
                "code": new_code,
                "click_limit": click_limit,
                "expiry_date": expiry_date,
                "created_date": new_created_date,
                "message": "Old URL was expired. New short URL created!"
            }), 201

    # URL never existed before -> create fresh
    short_code = generate_code()
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        '''INSERT INTO urls 
        (short_code, long_url, click_limit, expiry_date, created_date) 
        VALUES (?, ?, ?, ?, ?)''',
        (short_code, long_url, click_limit, expiry_date, created_date)
    )
    conn.commit()
    conn.close()

    short_url = f"http://localhost:5000/{short_code}"
    return jsonify({
        "short_url": short_url,
        "code": short_code,
        "click_limit": click_limit,
        "expiry_date": expiry_date,
        "created_date": created_date,
        "message": "New short URL created!"
    }), 201



# API 2 — GET /url/<short_code> — Returns ONLY original_url

@app.route('/url/<short_code>', methods=['GET'])
def get_original_url(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT long_url FROM urls WHERE short_code = ?',
        (short_code,)
    )
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({"original_url": result[0]}), 200



# API 3 — GET /<short_code> — Redirect + track clicks + check expiry/limit

@app.route('/<short_code>')
def redirect_url(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT long_url, click_count, click_limit, expiry_date 
        FROM urls WHERE short_code = ?''',
        (short_code,)
    )
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return jsonify({"error": "Short URL not found"}), 404

    long_url, click_count, click_limit, expiry_date = result

    if is_url_expired(click_count, click_limit, expiry_date):
        conn.close()
        return jsonify({"error": "This URL has expired!"}), 410

    cursor.execute(
        'UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?',
        (short_code,)
    )
    conn.commit()
    conn.close()

    return redirect(long_url)

# API 4 — GET /stats/<short_code> — Returns ALL statistics

@app.route('/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT long_url, click_count, click_limit, 
        expiry_date, created_date FROM urls WHERE short_code = ?''',
        (short_code,)
    )
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "long_url": result[0],
        "click_count": result[1],
        "click_limit": result[2],
        "expiry_date": result[3],
        "created_date": result[4],
        "short_url": f"http://localhost:5000/{short_code}"
    }), 200


if __name__ == '__main__':
    init_db()
    app.run(debug=True)