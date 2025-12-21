from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("finance.db")

def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            amount REAL,
            category TEXT
        )
    """)
    db.commit()
    db.close()

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]

        cur.execute(
            "INSERT INTO expenses VALUES (NULL, ?, ?)",
            (amount, category)
        )
        db.commit()

    cur.execute("SELECT SUM(amount) FROM expenses")
    total = cur.fetchone()[0] or 0

    cur.execute("SELECT amount, category FROM expenses")
    expenses = cur.fetchall()


    db.close()
    return render_template("index.html", total=total, expenses=expenses)

init_db()

if __name__ == "__main__":
    app.run(debug=True)
