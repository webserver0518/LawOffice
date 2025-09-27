from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.utils.user_managment import UserManager
import uuid


site_bp = Blueprint('site', __name__)

@site_bp.route('/')
@site_bp.route('/home')
def home():
    return render_template('base_site.html')

@site_bp.route('/about')
def about():
    return render_template('about.html')

@site_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        flash("כבר מחובר", "danger")
    else:
        username = ''
        if request.method == 'POST':
            username = request.form['username'].strip()
            password = request.form['password'].strip()

            result = UserManager.authenticate(username, password)

            if result == "success":
                session['logged_in'] = True
                session['office_name'] = UserManager.get_office_name(username)
                session['username'] = username
                session_id = str(uuid.uuid4())
                session['session_id'] = session_id
                session['user_type'] = 'admin' if username == 'admin' else 'client'

                UserManager.record_login(username, session_id)

                return redirect(url_for('client.base_dashboard'))

            elif result == "wrong_password":
                flash("הסיסמה שגויה", "danger")

            elif result == "user_not_found":
                flash("שם המשתמש לא קיים במערכת", "danger")

    return redirect(url_for('site.home'))

@site_bp.route('/logout')
def logout():
    session.clear()
    flash("התנתקת בהצלחה", "info")
    return redirect(url_for('site.home'))



@site_bp.route('/load_login')
def load_login():
    return render_template('site_components/login.html')

@site_bp.route('/load_about')
def load_about():
    return render_template('site_components/about.html')

@site_bp.route('/load_home')
def load_home():
    return render_template('site_components/home.html')




