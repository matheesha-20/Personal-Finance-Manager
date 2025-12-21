from flask import Flask, render_template, request,url_for, redirect, make_response
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import flash

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my_secret_key'

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    category = db.Column(db.String(50), nullable=False)

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

@app.route("/add", methods=["POST"])
def add():
    
    name = request.form["name"]
    amount = request.form["amount"]
    date_str = request.form["date"]
    category = request.form["category"]


    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    new_expense = Expense(name=name, amount=amount, date=date, category=category)
    db.session.add(new_expense)
    db.session.commit()

   

    print(f"Added expense: {name}, {amount}, {date}, {category}")
    
    flash("Expense added successfully!", "success")

    return redirect(url_for("index"))

    @app.route("/")
    def index():
        expenses = Expense.query.order_by(Expense.date.desc()).all()
        total = sum(e.amount for e in expenses)
        return render_template("index.html", expenses=expenses, total=total)



if __name__ == "__main__":
    app.run(debug=True)
