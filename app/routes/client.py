from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from app.utils.data_managment import DataManager
from app.utils.legal_case_classes import GreetingHelper
from app.utils.s3_managment import S3Manager


client_bp = Blueprint('client', __name__)


@client_bp.route('/base_dashboard')
def base_dashboard():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

    return render_template('base_dashboard.html',
                           greeting=GreetingHelper.get_greeting(),
                           current_time=GreetingHelper.get_current_time(),
                           user=session.get('username'))


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

@client_bp.route("/get_clients")
def get_clients():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

    clients = DataManager.load_json_from_data("clients") or []
    return jsonify(clients)

@client_bp.route('/client_create', methods=['POST'])
def client_create():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

    username = session.get("username")

    case_data = request.form.to_dict()

    index_uploads_name = "index"
    index_uploads_file = DataManager.load_json_from_data_indexs(index_uploads_name)
    index_uploads_file['num_of_cases'] += 1
    case_serial_number = index_uploads_file['num_of_cases']
    DataManager.save_json_to_data_indexs(index_uploads_name, index_uploads_file)


    index_username_name = "index-" + username

    index_username_file = DataManager.load_json_from_data_indexs(index_username_name)
    index_username_file[case_serial_number] = case_data['case_title']
    DataManager.save_json_to_data_indexs(index_username_name, index_username_file)

    print(case_data)

    files = [fs for fs in request.files.getlist('files') if fs.filename]
    print('len(files): ' + str(len(files)))

    for fs in files:
        if not fs or fs.filename == '':
            continue
        dest_key = f"{username}/{case_serial_number}/{fs.filename}"
        print(dest_key)
        S3Manager.upload(fs, dest_key)  

    flash('התיק נוסף בהצלחה', 'success')
    return render_template("base_dashboard.html", page='view_case')


@client_bp.route('/load_attendency_birds_view')
def load_attendency_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    return render_template('client_components/attendency_birds_view.html')




