from flask import Blueprint, render_template, request, flash, redirect, url_for
import sqlite3
from .views import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? LIMIT 1', (email,))
        if user is None:
            flash('User does not exist.', category='error')
        else:
            row = user.fetchone()
            result_dict = dict(zip(row.keys(), row))
            print(result_dict)
 
            if check_password_hash(result_dict['password'], password):
                flash('Logged in successfully!', category='success')
            else:
                flash('Incorrect password, try again.', category='error')
        conn.close()
            
    return render_template("login.html")
    
@auth.route('/logout')
def logout():
    return redirect(url_for('views.home'))
    
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

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? LIMIT 1', (email,))
        conn.close()
        if user:
            flash('Email already exists.', category='error')
        elif len(agency_name) < 2:
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
            password = generate_password_hash(password1, method='sha256')
            conn = get_db_connection()
            conn.execute('CREATE TABLE IF NOT EXISTS users ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'name STRING(150) UNIQUE,'
                'email STRING(150) UNIQUE,'
                'contact INTEGER UNIQUE,'
                'password STRING(150)'
                ');'
            )
            conn.commit()
            conn.execute('INSERT INTO users (name, email, contact, password) VALUES (?, ?, ?, ?)',
                         (agency_name, email, contact, password))
            conn.commit()
            conn.close()
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))
    return render_template("sign_up.html")