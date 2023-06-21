from flask import Blueprint, render_template, request, flash, Flask
import sqlite3

auth = Blueprint('auth', __name__)
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('home.html', users=users)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")
    
@auth.route('/logout')
def logout():
    return render_template("logout.html")
    
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    data =request.form
    print(data)
    if request.method == 'POST':
        agency_name = request.form.get('agencyName')
        email = request.form.get('email')
        contact = request.form.get('contact')        
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if len(agency_name) < 2:
            flash('Agency name must be greater than 1 characters.', category='error')
        elif len(email) < 11:
            flash('Agency email must be greater than 10 characters.', category='error')
        elif len(contact) < 9:
            flash('Phone number must be greater than 8 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO users (name, email, contact, password) VALUES (?, ?, ?, ?)',
                         (agency_name, email, contact, password1))
            conn.commit()
            conn.close()
            flash('Account created successfully!', category='success')
    return render_template("sign_up.html")