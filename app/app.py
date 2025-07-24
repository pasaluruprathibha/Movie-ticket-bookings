from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        seats INTEGER NOT NULL,
        show TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        seats = request.form['seats']
        show = request.form['show']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, seats, show) VALUES (?, ?, ?, ?)",
                  (name, email, seats, show))
        conn.commit()
        conn.close()

        return redirect('/bookings')

    return render_template('book.html')
@app.route('/bookings')
def bookings():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    data = c.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
