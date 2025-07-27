# app.py
from moneyflow import create_app
<<<<<<< HEAD
from moneyflow.models import db
=======
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile

app = create_app()

if __name__ == '__main__':
<<<<<<< HEAD
    with app.app_context():
        db.create_all()
=======
>>>>>>> feature/initial-deliverable-with-user-auth-and-profile
    app.run(host='0.0.0.0', port= 5500, debug=True)
