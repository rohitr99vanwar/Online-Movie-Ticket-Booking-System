from flask import Flask, render_template, request, redirect, session, jsonify, send_file
import sqlite3
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "secret123"

# ---------- DB ----------
def init_db():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    print("Creating tables...")

    # USERS
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )''')

    # BOOKINGS (UPDATED WITH CUSTOMER)
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        customer TEXT,
        movie TEXT,
        seat TEXT,
        timing TEXT
    )''')

    # MOVIES
    c.execute('''CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )''')

    # DEFAULT MOVIES
    c.execute("SELECT * FROM movies")
    if not c.fetchall():
        c.executemany("INSERT INTO movies (name) VALUES (?)", [
            ("Avengers",),
            ("KGF",),
            ("Pushpa",),
            ("RRR",),
            ("Salaar",)
        ])

    conn.commit()
    conn.close()

# ---------- ROUTES ----------
@app.route('/')
def root():
    return redirect('/register')

# ---------- HOME ----------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute("SELECT name FROM movies")
    movies = [row[0] for row in c.fetchall()]

    conn.close()

    return render_template('index.html', user=session['user'], movies=movies)

# ---------- REGISTER ----------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        conn = sqlite3.connect('movies.db')
        c = conn.cursor()

        # CHECK USER EXISTS
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            conn.close()
            return render_template('register.html', error="User already exists")

        c.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].lower()
        password = request.form['password']

        conn = sqlite3.connect('movies.db')
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            return redirect('/home')

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

# ---------- ADD MOVIE ----------
@app.route('/add_movie', methods=['POST'])
def add_movie():
    if 'user' not in session:
        return redirect('/login')

    name = request.form['name'].strip().title()

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    # CHECK EXISTS
    c.execute("SELECT * FROM movies WHERE LOWER(name)=LOWER(?)", (name,))
    if c.fetchone():
        conn.close()
        return redirect('/home?msg=exists')

    c.execute("INSERT INTO movies (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

    return redirect('/home?msg=added')

# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ---------- BOOK ----------
@app.route('/book', methods=['POST'])
def book():
    data = request.json
    movie = data['movie']
    seat = data['seat']
    customer = data.get('customer')
    timing = data.get('timing')

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    # CHECK SEAT
    c.execute("SELECT * FROM bookings WHERE movie=? AND seat=?", (movie,seat))
    if c.fetchone():
        return jsonify({"status":"fail","message":"Seat already booked"})

    # INSERT
    c.execute("INSERT INTO bookings (username,customer,movie,seat,timing) VALUES (?,?,?,?,?)",
              (session['user'],customer,movie,seat,timing))

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})

# ---------- RECEIPT ----------
@app.route('/receipt')
def receipt():
    if 'user' not in session:
        return redirect('/login')

    movie = request.args.get('movie')
    seat = request.args.get('seat')
    customer = request.args.get('customer')
    timing = request.args.get('timing')

    if not movie or not seat:
        return redirect('/home')

    file_path = "ticket.pdf"

    c = canvas.Canvas(file_path)
    c.drawString(100,750,"🎬 Movie Ticket Receipt")
    c.drawString(100,700,f"Customer: {customer}")
    c.drawString(100,670,f"Movie: {movie}")
    c.drawString(100,640,f"Seat: {seat}")
    c.drawString(100,610,f"Timing: {timing}")
    c.save()

    return send_file(file_path, as_attachment=True)

# ---------- HISTORY ----------
@app.route('/history')
def history():
    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute("SELECT customer,movie,seat,timing FROM bookings WHERE username=?", (session['user'],))
    data = c.fetchall()
    conn.close()

    return render_template('history.html', bookings=data)

# ---------- GET BOOKED ----------
@app.route('/get_booked')
def get_booked():
    movie = request.args.get('movie')

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    c.execute("SELECT seat FROM bookings WHERE movie=?", (movie,))
    data = [row[0] for row in c.fetchall()]

    conn.close()
    return jsonify(data)

# ---------- RUN ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)