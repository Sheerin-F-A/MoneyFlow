# MoneyFlow: Personal Finance Tracker

MoneyFlow is a simple, modern web application for tracking your personal expenses. Built with Flask, Bootstrap, SQLAlchemy, and Loguru, it helps you record, view, edit, and delete expenses, and provides a summary of your spending habits.

---

## Features

- 📊 **Dashboard:** View total expenses and breakdown by category  
- ➕ **Add Expenses:** Simple form to log new spending  
- ✏️ **Edit & Delete:** Update or remove existing expenses  
- 🔎 **Expense Table:** See all your expenses at a glance  
- 📝 **Logging:** All actions are logged using Loguru for easy debugging  
- 🎨 **Responsive UI:** Clean Bootstrap interface, works on desktop and mobile

---

## Screenshots

![alt text](image.png)
![alt text](image2.png)

---

## Getting Started

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

### 4. Run the Application

```bash
python app.py
```

Visit [http://127.0.0.1:5500](http://127.0.0.1:5500) in your browser.

---

## Project Structure

```
MONEYFLOW/
├── app.py
├── requirements.txt
├── README.md
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
│   │   └── edit_expense.html
│   └── static/
│       └── style.css
└── venv/
```

---

## Configuration

- **Database:** Uses SQLite (`expenses.db`) by default.
- **Logging:** All logs are written to the `logs/` directory.
- **Secret Key:** Set in `moneyflow/__init__.py` for session management and flash messages.

---

## Customization

- To change categories or UI, edit the HTML templates in `moneyflow/templates/`.
- To adjust logging behavior, modify Loguru settings in `moneyflow/__init__.py`.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Loguru](https://loguru.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

---

*Happy tracking!*

