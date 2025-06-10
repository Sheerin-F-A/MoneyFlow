# moneyflow/__init__.py
from flask import Flask, render_template, redirect, url_for, request, flash
from .models import db, Expense
from datetime import datetime
from loguru import logger
import sys
import os

def create_app():

    # Determine the absolute path to the logs/ directory
    log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Remove default handler and add your own
    logger.remove()
    logger.add(sys.stdout, colorize=True, level="INFO")  # Console logs
    logger.add("moneyflow.log", rotation="10 MB", retention="1 week", level="DEBUG")  # File logs
    logger.add("errors.log", rotation="10 MB", level="ERROR")  # Only errors to a separate file

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-very-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def home():
        expenses = Expense.query.order_by(Expense.date.desc()).all()
        # Calculate total expenses
        total_expense = sum(exp.amount for exp in expenses)
        # Calculate expenses by category
        expenses_by_category = {}
        for exp in expenses:
            expenses_by_category[exp.category] = expenses_by_category.get(exp.category, 0) + exp.amount
        return render_template(
            'home.html',
            expenses=expenses,
            total_expense=total_expense,
            expenses_by_category=expenses_by_category
        )
    
    # CREATE
    @app.route('/add', methods=['GET', 'POST'])
    def add_expense():
        if request.method == 'POST':
            try:
                amount = request.form['amount']
                category = request.form['category']
                description = request.form['description']
                date_str = request.form['date']

                # Convert date string to datetime object, or use now if empty
                if date_str:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                else:
                    date = datetime.utcnow()
                logger.info(f"Adding expense: {amount} {category} {description} {date}")
                # Create and save the expense
                new_expense = Expense(
                    amount=float(amount),
                    category=category,
                    description=description,
                    date=date
                )
                db.session.add(new_expense)
                db.session.commit()
                logger.success("Expense added successfully.")
                flash('Expense added successfully!', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                logger.error(f"Failed to add expense: {e}")
                flash('Error adding expense', 'danger')
                return redirect(url_for('home'))
        return render_template('add_expense.html')
    
    # UPDATE
    @app.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
    def edit_expense(expense_id):
        expense = Expense.query.get_or_404(expense_id)
        if request.method == 'POST':
            try:
                logger.info(f"Editing expense {expense_id}")
                expense.amount = float(request.form['amount'])
                expense.category = request.form['category']
                expense.description = request.form['description']
                date_str = request.form['date']
                expense.date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else expense.date
                db.session.commit()
                logger.success("Expense updated successfully.")
                flash('Expense updated!', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                logger.error(f"Failed to update expense: {e}")
                flash('Error editing expense', 'danger')
                return redirect(url_for('home'))
        return render_template('edit_expense.html', expense=expense)

    # DELETE
    @app.route('/delete/<int:expense_id>', methods=['POST'])
    def delete_expense(expense_id):
        try:
            logger.warning(f"Deleting expense {expense_id}")
            expense = Expense.query.get_or_404(expense_id)
            db.session.delete(expense)
            db.session.commit()
            logger.success("Expense deleted successfully.")
            flash('Expense deleted!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            logger.error(f"Failed to delete expense: {e}")
            flash('Error deleting expense', 'danger')
            return redirect(url_for('home'))

    @app.errorhandler(Exception)
    def handle_exception(e):
        logger.exception(f"Unhandled exception: {e}")
        flash('An unexpected error occurred.', 'danger')
        return render_template('home.html'), 500

    return app
