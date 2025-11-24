"""app.py: render and route to webpages"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from db.query import get_all, insert, get_user_by_email
from db.server import init_database
from db.schema import Users
import bcrypt
import logging

# load environment variables from .env
load_dotenv()

# database connection - values set in .env
db_name = os.getenv('db_name')
db_owner = os.getenv('db_owner')
db_pass = os.getenv('db_pass')
db_url = f"postgresql://{db_owner}:{db_pass}@localhost/{db_name}"

# logging config
logging.basicConfig(
    filename = "logs/logs.txt", level=logging.INFO, filemode="a", format="%(asctime)s [%(levelname)s%] %(message)s"
)

logger = logging.getLogger(__name__)

def create_app():
    """Create Flask application and connect to your DB"""
    # create flask app
    app = Flask(__name__,
                template_folder=os.path.join(os.getcwd(), 'templates'),
                static_folder=os.path.join(os.getcwd(), 'static'))

    # connect to db
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    # Initialize database
    with app.app_context():
        if not init_database():
            print("Failed to initialize database. Exiting.")
            exit(1)

    # ===============================================================
    # routes
    # ===============================================================

    # create a webpage based off of the html in templates/index.html
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """Sign up page: enables users to sign up"""
        # TODO: implement sign up logic here
        error: str = None
        is_valid: bool = False
        if request.method == 'POST':
            fname = request.form["FirstName"].strip()
            lname = request.form["LastName"].strip()
            email = request.form["Email"].strip()
            phone = request.form["PhoneNumber"].strip()
            password = request.form["Password"].strip()

            is_valid = fname.isalpha() and lname.isalpha() and len(phone) == 10 and phone.isdigit()
            if not is_valid:
                flash("Invalid input.")
            else:
                try:
                    # create user objects using information from the form
                    hashedPass = bcrypt.hashpw(
                        password.encode('utf-8'), bcrypt.gensalt()
                    )
                    decodePass = hashedPass.decode('utf-8')
                    user = Users(
                        FirstName=fname,
                        LastName=lname,
                        Email=email,
                        PhoneNumber=phone,
                        Password=decodePass
                    )
                    
                    insert(user)

                except Exception as e:
                    flash("Exception:", e)
                    error = "Failed to create user."
                    logger.error(f"Error creating user: {e}")
                    # log the error message
                    flash("Error:", error)

                finally:
                    return redirect(url_for('index'))

        return render_template('signup.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Log in page: enables users to log in"""
        # TODO: implement login logic here
        if request.method == 'POST':
            email = request.form["Email"].strip()
            password = request.form["Password"].strip()
            try:
                user = get_user_by_email(Users, email)
                valid_pass = False
                valid_email = False
                if user:
                    valid_email = True
                    if bcrypt.checkpw(password.encode('utf-8'), user.Password.encode('utf-8')):
                        valid_pass = True
                if not (valid_email and valid_pass):
                    raise Exception("Incorrect Credentials")
            except Exception as e:
                print("Exception:", e)
            finally:
                if valid_email and valid_pass:
                    return redirect(url_for('success'))
                else:
                    return redirect(url_for('login'))
        return render_template('login.html')

    @app.route('/users')
    def users():
        """Users page: displays all users in the Users table"""
        all_users = get_all(Users)

        return render_template('users.html', users=all_users)

    @app.route('/success')
    def success():
        """Success page: displayed upon successful login"""

        return render_template('success.html')

    return app


if __name__ == "__main__":
    app = create_app()
    # debug refreshes your application with your new changes every time you save
    app.run(debug=True)
