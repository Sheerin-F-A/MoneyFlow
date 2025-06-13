# MoneyFlow: Personal Finance Tracker

MoneyFlow is a modern, secure web application for tracking your personal expenses. Built with Flask, Bootstrap, SQLAlchemy, and Loguru, it lets you record, view, edit, and delete expenses, manage your account, and provides a summary of your spending habits.  
**Each user’s data is private and protected by authentication.**

---

## Features

- 🔐 **User Authentication:** Sign up, log in, log out, and update your password
- 📊 **Dashboard:** View total expenses and breakdown by category
- ➕ **Add Expenses:** Simple form to log new spending
- ✏️ **Edit & Delete:** Update or remove your own expenses
- 🔎 **Expense Table:** See all your expenses at a glance
- 📝 **Logging:** All actions are logged using Loguru for easy debugging
- 🎨 **Responsive UI:** Clean Bootstrap interface, works on desktop and mobile
- 🛡️ **Per-User Data:** Each user only sees and manages their own expenses
- 🔑 **Secure Configuration:** Secret key loaded from environment variable

---

## Screenshots

![Dashboard](./demo](./demo-images/image2.png](./demo-images/image3.png](./demo-images/image5.png](./demo-images/image6.png](./demo-images/image8.png Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/moneyflow.git
cd moneyflow
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in your project root:
```
SECRET_KEY=your-very-secret-key-here
```
*(Generate a secure key with `python -c "import secrets; print(secrets.token_hex(32))"`)*

### 5. Run the Application

```bash
python app.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## Project Structure

```
MONEYFLOW/
├── app.py
├── requirements.txt
├── README.md
├── .env
├── logs/
│   ├── moneyflow.log
│   └── errors.log
├── moneyflow/
│   ├── __init__.py
│   ├── models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── add_expense.html
│   │   ├── edit_expense.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   └── update_password.html
│   └── static/
│       └── style.css
└── venv/
```

---

## Configuration

- **Database:** Uses SQLite (`expenses.db`) by default.
- **Logging:** All logs are written to the `logs/` directory.
- **Secret Key:** Loaded from `.env` for session management and flash messages.
- **User Data:** Each user’s expenses are private and secure.

---

## Customization

- To change categories or UI, edit the HTML templates in `moneyflow/templates/`.
- To adjust logging behavior, modify Loguru settings in `moneyflow/__init__.py`.
- To use a different database (e.g., PostgreSQL), update the `SQLALCHEMY_DATABASE_URI` in your config.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Loguru](https://loguru.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/2.3.x/utils/)

---

*Happy tracking!*

---

**Tip:**  
If deploying to production (Heroku, Vercel, etc.), set your environment variables in the platform’s dashboard for security.  
For persistent data, use a managed database service instead of local SQLite.