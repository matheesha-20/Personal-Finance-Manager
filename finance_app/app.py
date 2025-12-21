from flask import Flask, render_template, request
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    # db = sqlite3.connect("finance.db")
    # cur = db.cursor()

    # if request.method == "POST":
    #     amount = request.form["amount"]
    #     category = request.form["category"]

    #     cur.execute(
    #         "INSERT INTO expenses VALUES (NULL, ?, ?)",
    #         (amount, category)
    #     )
    #     db.commit()

    # cur.execute("SELECT SUM(amount) FROM expenses")
    # total = cur.fetchone()[0] or 0

    # cur.execute("SELECT amount, category FROM expenses")
    # expenses = cur.fetchall()


    # db.close()
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
