# moneyflow/__init__.py
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Expense, User
from datetime import datetime
from loguru import logger
import sys
import os
from dotenv import load_dotenv

load_dotenv() 

def create_app():

    # Determine the absolute path to the logs/ directory
    log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Remove default handler and add your own
    logger.remove()
    logger.add(sys.stdout, colorize=True, level="INFO")  # Console logs
    logger.add(os.path.join(log_dir, "moneyflow.log"), rotation="10 MB", retention="1 week", level="DEBUG")  # File logs
    logger.add(os.path.join(log_dir, "errors.log"), rotation="10 MB", level="ERROR")  # Only errors to a separate file

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    def login_required(f):
        from functools import wraps
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    @app.route('/')
    def home():
        user_id = session.get('user_id')
        expenses = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()
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
    @login_required
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
                    date=date,
                    user_id=session['user_id'] 
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
    @login_required
    def edit_expense(expense_id):
        expense = Expense.query.filter_by(id=expense_id, user_id=session['user_id']).first_or_404()
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
    @login_required
    def delete_expense(expense_id):
        try:
            logger.warning(f"Deleting expense {expense_id}")
            expense = Expense.query.filter_by(id=expense_id, user_id=session['user_id']).first_or_404()
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

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.', 'danger')
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
            else:
                hashed_pw = generate_password_hash(password)
                new_user = User(username=username, password=hashed_pw)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created! Please log in.', 'success')
                return redirect(url_for('login'))
        return render_template('signup.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash('Logged out.', 'info')
        return redirect(url_for('login'))
    
    @app.route('/update_password', methods=['GET', 'POST'])
    def update_password():
        if not session.get('user_id'):
            flash('Please log in to update your password.', 'warning')
            return redirect(url_for('login'))

        user = User.query.get(session['user_id'])

        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']

            if not check_password_hash(user.password, current_password):
                flash('Current password is incorrect.', 'danger')
            elif len(new_password) < 6:
                flash('New password should be at least 6 characters.', 'warning')
            else:
                user.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Password updated successfully!', 'success')
                return redirect(url_for('home'))

        return render_template('update_password.html')


    return app
