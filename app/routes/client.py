from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.utils.data_managment import DataManager
from app.utils.legal_case_classes import GreetingHelper
from datetime import datetime

import os
from werkzeug.utils import secure_filename
import uuid


client_bp = Blueprint('client', __name__)


@client_bp.route('/base_dashboard')
def base_dashboard():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

    return render_template('base_dashboard.html',
                           greeting=GreetingHelper.get_greeting(),
                           current_time=GreetingHelper.get_current_time(),
                           user=session.get('user'))

@client_bp.route('/client_create', methods=['POST'])
def client_create():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

    username = session.get("username", "anonymous")

    case_data = request.form.to_dict()

    #DataManager.save_case_with_sequence(username, case_data)
    flash(str(DataManager.my(username, case_data)), 'success')

    #flash('התיק נוסף בהצלחה', 'success')
    return render_template("base_dashboard.html", page='view_case')


# dashboard loaders

@client_bp.route('/load_birds_view')
def load_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/birds_view.html')


@client_bp.route('/load_cases_birds_view')
def load_cases_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/cases_birds_view.html')

@client_bp.route('/load_active_cases')
def load_active_cases():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/active_cases.html')

@client_bp.route('/load_add_case')
def load_add_case():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/add_case.html')

@client_bp.route('/load_view_case')
def load_view_case():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

    return render_template("client_components/view_case.html")


    # Flask route – דוגמה

@client_bp.route('/load_archived_cases')
def load_archived_cases():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/archived_cases.html')



@client_bp.route('/load_clients_birds_view')
def load_clients_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/clients_birds_view.html')

@client_bp.route('/load_active_clients')
def load_active_clients():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/active_clients.html')

@client_bp.route('/load_add_client')
def load_add_client():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/add_client.html')

@client_bp.route('/load_view_client')
def load_view_client():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

    return render_template("client_components/view_client.html")



@client_bp.route('/load_attendency_birds_view')
def load_attendency_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/attendency_birds_view.html')

