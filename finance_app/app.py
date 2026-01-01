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

    CATEGORIES = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Rent', 'Health', 'Other']

    def parse_date_or_none(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return None

    @app.route("/")
    def index():

        start_str = (request.args.get("start") or "").strip()
        end_str = (request.args.get("end") or "").strip()
        selected_category = request.args.get("category", "").strip()

        start_date = parse_date_or_none(start_str)
        end_date = parse_date_or_none(end_str)

        if start_date and end_date and end_date < start_date:
            flash("End date cannot be earlier than start date.", "error")
            start_date = end_date = None
            start_str = end_str = ""
            return redirect(url_for("index"))
        
        q = Expense.query
        if start_date:
            q = q.filter(Expense.date >= start_date)
        if end_date:
            q = q.filter(Expense.date <= end_date)

        if selected_category:
            q = q.filter(Expense.category == selected_category)

        expenses = q.order_by(Expense.date.desc(), Expense.id.desc()).all()
        total = sum(e.amount for e in expenses)


        cat_q = db.session.query(Expense.category, db.func.sum(Expense.amount))

        if start_date:
            cat_q = cat_q.filter(Expense.date >= start_date)
        if end_date:
            cat_q = cat_q.filter(Expense.date <= end_date)
        if selected_category:
            cat_q = cat_q.filter(Expense.category == selected_category)

        cat_row = cat_q.group_by((Expense.category)).all()
        cat_labels = [c for c, _ in cat_row]
        cat_values = [round(float(a or 0),2) for _, a in cat_row]


        day_q = db.session.query(Expense.date, db.func.sum(Expense.amount))

        if start_date:
            day_q = day_q.filter(Expense.date >= start_date)
        if end_date:
            day_q = day_q.filter(Expense.date <= end_date)
        if selected_category:
            day_q = day_q.filter(Expense.category == selected_category)

        day_row = day_q.group_by((Expense.date)).order_by(Expense.date).all()
        day_labels = [c.isoformat() for c, _ in day_row]
        day_values = [round(float(a or 0),2) for _, a in day_row]


        return render_template(

            "index.html", 
            expenses=expenses,
            total=total,
            categories=CATEGORIES,
            start_date=start_str,
            end_date=end_str,
            selected_category=selected_category,
            today=datetime.today().date(),
            notifications=1,
            cat_labels=cat_labels,
            cat_values=cat_values,
            day_labels=day_labels,
            day_values=day_values

        )


    @app.route("/add", methods=["POST"])
    def add():
        name = request.form["name"]
        amount = float(request.form["amount"])
        date_str = request.form["date"]
        category = request.form["category"]

        date = datetime.strptime(date_str, "%Y-%m-%d").date()

        new_expense = Expense(
            name=name,
            amount=amount,
            date=date,
            category=category
        )

        db.session.add(new_expense)
        db.session.commit()

        flash("Expense added successfully!", "success")
        return redirect(url_for("index"))

    @app.route("/delete/<int:expense_id>", methods=["POST"])
    def delete(expense_id):
        expense = Expense.query.get_or_404(expense_id)
        db.session.delete(expense)
        db.session.commit()
        flash("Expense deleted successfully!", "success")
        return redirect(url_for("index"))

   


if __name__ == "__main__":
    app.run(debug=True)
