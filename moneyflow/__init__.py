# moneyflow/__init__.py
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
<<<<<<< HEAD
from .models import db, Expense, User
from datetime import datetime
from loguru import logger
import sys
import os
=======
from datetime import datetime, date
from loguru import logger
import sys
import os
import random
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
<<<<<<< HEAD

load_dotenv() 
mail = Mail()

def create_app():

=======
from flask_migrate import Migrate       
from .extensions import db, migrate 

load_dotenv() 
mail = Mail() 

QUOTES = [
    "Every penny saved is a penny earned.",
    "Small steps every day lead to big results.",
    "Your budget is a reflection of your goals.",
    "Save money, and money will save you.",
    "Don’t watch the clock; do what it does. Keep going.",
    "Dream big, save bigger!",
    "Financial freedom is a journey, not a destination.",
    "A goal without a plan is just a wish.",
    "The best time to start was yesterday. The next best is now.",
    "Discipline is the bridge between goals and accomplishment.",
]

def create_app():
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile
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
<<<<<<< HEAD
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
=======
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("MYSQL_URI")
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'moneyflow', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = '78cf082ad41558'
    app.config['MAIL_PASSWORD'] = '1e2111c11c2383'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail.init_app(app)
    db.init_app(app)
<<<<<<< HEAD
=======
    migrate.init_app(app, db)    

    from . import models   
    from .models import Expense, User
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile

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
<<<<<<< HEAD
=======
        today = date.today().toordinal()
        quote_of_the_day = QUOTES[today % len(QUOTES)]    
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile
        return render_template(
            'home.html',
            expenses=expenses,
            total_expense=total_expense,
<<<<<<< HEAD
            expenses_by_category=expenses_by_category
=======
            expenses_by_category=expenses_by_category,
            quote_of_the_day=quote_of_the_day
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile
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
                logger.info(f"Login success: user_id={user.id}, username={user.username}, ip={request.remote_addr}")
                flash('Logged in successfully!', 'success')
                return redirect(url_for('home'))
            else:
                logger.warning(f"Login failed: username={username}, ip={request.remote_addr}")
                flash('Invalid username or password.', 'danger')
        return render_template('login.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if User.query.filter_by(username=username).first():
                logger.warning(f"Signup failed: username exists ({username}), ip={request.remote_addr}")
                flash('Username already exists.', 'danger')
            else:
                hashed_pw = generate_password_hash(password)
                new_user = User(username=username, password=hashed_pw)
                db.session.add(new_user)
                db.session.commit()
                logger.info(f"Signup success: user_id={new_user.id}, username={username}, ip={request.remote_addr}")
                flash('Account created! Please log in.', 'success')
                return redirect(url_for('login'))
        return render_template('signup.html')

    @app.route('/logout')
    def logout():
        user_id = session.get('user_id')
        logger.info(f"Logout: user_id={user_id}, ip={request.remote_addr}")
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

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @app.route('/profile', methods=['GET', 'POST'])
    @login_required
    def profile():
        user = User.query.get(session['user_id'])
        if request.method == 'POST':
            email = request.form.get('email')
            preferences = request.form.get('preferences')
            file = request.files.get('profile_picture')
            logger.info(f"Profile updated: user_id={user.id}, ip={request.remote_addr}")
            if email:
                user.email = email
            if preferences:
                user.preferences = preferences
            if file and allowed_file(file.filename):
                logger.info(f"Profile picture uploaded: user_id={user.id}, filename={file.filename}, ip={request.remote_addr}")
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_picture = filename
            db.session.commit()
            flash('Profile updated!', 'success')
            return redirect(url_for('profile'))
        return render_template('profile.html', user=user)
    

    # helper to generate tokens

    def generate_reset_token(user_id, expires_sec=3600):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': user_id}, salt='password-reset-salt')

    def verify_reset_token(token, expires_sec=3600):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=expires_sec)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)
    
    # forgot PASSWORD route

    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        if request.method == 'POST':
            email = request.form['email']
            user = User.query.filter_by(email=email).first()
            if user:
                logger.info(f"Password reset requested: user_id={user.id}, email={email}, ip={request.remote_addr}")
                token = generate_reset_token(user.id)
                reset_url = url_for('reset_password', token=token, _external=True)
                msg = Message('Password Reset Request',
                            sender=app.config['MAIL_USERNAME'],
                            recipients=[user.email])
                msg.body = f'Reset your password: {reset_url}'
                mail.send(msg)
                flash('A password reset link has been sent to your email.', 'info')
            else:
                logger.warning(f"Password reset requested for non-existent email: {email}, ip={request.remote_addr}")
                flash('No user found with that email.', 'danger')
        return render_template('forgot_password.html')
    
    # reset password route:

    @app.route('/reset/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        user = verify_reset_token(token)
        if not user:
            logger.warning(f"Invalid/expired reset token used, ip={request.remote_addr}")
            flash('Invalid or expired token.', 'danger')
            return redirect(url_for('login'))
        if request.method == 'POST':
            new_password = request.form['new_password']
            user.password = generate_password_hash(new_password)
            db.session.commit()
            logger.info(f"Password reset successful: user_id={user.id}, ip={request.remote_addr}")
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        return render_template('reset_password.html')



    return app
