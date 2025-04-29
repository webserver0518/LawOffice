from flask import Flask, render_template, redirect, url_for, session, flash, request, send_file, g
from legal_case_classes import GreetingHelper, Config

from user_managment import UserManager
from data_managment import DataManager

from datetime import datetime
from collections import Counter
import uuid


app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0          # Flask לא ישים max-age

@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"]        = "no-cache"
    response.headers["Expires"]       = "0"
    return response


# site functions

@app.route('/')
def base_site():
    return render_template('base_site.html')

@app.route('/home')
def home():
    return render_template('base_site.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = ''
    if request.method == 'POST':
        username = request.form['username'].strip()
        pwd = request.form['password'].strip()
        local_time = request.form.get('local_time')

        result = UserManager.authenticate(username, pwd)

        if result == "success":
            session['logged_in'] = True
            session['user'] = username
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            session['user_type'] = 'admin' if username == 'admin' else 'client'

            UserManager.record_login(username, session_id)

            return redirect(url_for('base_dashboard'))

        elif result == "wrong_password":
            flash("הסיסמה שגויה", "danger")

        elif result == "user_not_found":
            flash("שם המשתמש לא קיים במערכת", "danger")

    return redirect(url_for('base_site'))

@app.route('/logout')
def logout():
    session.clear()
    flash("התנתקת בהצלחה", "info")
    return redirect(url_for('base_site'))

# site loaders

@app.route('/load_login')
def load_login():
    return render_template('site_components/login.html')

@app.route('/load_about')
def load_about():
    return render_template('site_components/about.html')

@app.route('/load_home')
def load_home():
    return render_template('site_components/home.html')

# admin functions

@app.route('/users_managment', methods=['POST'])
def users_managment():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))

    action = request.form.get('action')
    username = request.form.get('username')
    password = request.form.get('password')

    if action == 'add':
        success = UserManager.add_user(username, password)
        if not success:
            return 'Conflict', 409  # user exists
    elif action == 'update':
        UserManager.update_password(username, password)
    elif action == 'delete':
        UserManager.delete_user(username)

    return '', 204  # No content

# admin loaders

@app.route('/load_users_management')
def load_users_management():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    users = UserManager.load_users()
    return render_template('admin_components/users_management.html', users=users)

@app.route('/load_users_statistics')
def load_users_statistics():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))

    logins = UserManager.load_logins()

    from collections import Counter
    from datetime import datetime

    all_times = []
    user_counts = {}
    user_durations = {}

    for user, sessions in logins.items():
        if user == "admin":
            continue

        total_duration = 0
        for entry in sessions:
            if isinstance(entry, dict) and "login" in entry:
                login_time = datetime.strptime(entry["login"], "%Y-%m-%d %H:%M")
                logout_time = datetime.strptime(entry["logout"], "%Y-%m-%d %H:%M") if entry.get("logout") else datetime.now()
                duration = (logout_time - login_time).total_seconds() / 60
                total_duration += duration
                all_times.append(login_time.hour)

        user_counts[user] = len(sessions)
        user_durations[user] = round(total_duration, 1)

    hour_distribution = Counter(all_times).most_common()
    total_logins = sum(user_counts.values())
    most_active_user = max(user_counts.items(), key=lambda x: x[1])[0] if user_counts else None

    return render_template('admin_components/users_statistics.html',
                           total_logins=total_logins,
                           most_active_user=most_active_user,
                           hour_distribution=hour_distribution,
                           user_durations=user_durations)

@app.route('/load_server_info')
def load_server_info():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))

    import platform
    import socket
    import psutil

    def bytes_to_gb(b):
        return round(b / (1024 ** 3), 2)
    
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)

    info = {
        "hostname": socket.gethostname(),
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "os": platform.system() + " " + platform.release(),
        "python_version": platform.python_version(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,
        "memory_percent": mem.percent,
        "memory_used": bytes_to_gb(mem.used),
        "memory_total": bytes_to_gb(mem.total),
        "disk_percent": disk.percent,
        "disk_used": bytes_to_gb(disk.used),
        "disk_total": bytes_to_gb(disk.total)
    }

    return render_template('admin_components/server_info.html', info=info)

# dashboard functions

@app.route('/base_dashboard')
def base_dashboard():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))

    return render_template('base_dashboard.html',
                           greeting=GreetingHelper.get_greeting(),
                           current_time=GreetingHelper.get_current_time(),
                           user=session.get('user'))

@app.route('/client_create', methods=['POST'])
def client_create():
    username = session.get("user", "anonymous")
    if not username:
        username = "anonymous"

    case_data = {
        "client_name": request.form.get("client_name"),
        "client_phone": request.form.get("client_phone"),
        "client_email": request.form.get("client_email"),
        "client_address": request.form.get("client_address"),
        "case_title": request.form.get("case_title"),
        "category": request.form.get("category"),
        "case_facts": request.form.get("case_facts"),
        "timestamp": datetime.now().isoformat(timespec='seconds')
    }

    print("📄 case_data:", case_data)
    print("👤 username:", username)

    DataManager.save_user_case(username, case_data)

    flash('התיק נוסף בהצלחה', 'success')
    return render_template("base_dashboard.html", page='view_case')


# dashboard loaders

@app.route('/load_birds_view')
def load_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/birds_view.html')


@app.route('/load_cases_birds_view')
def load_cases_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/cases_birds_view.html')

@app.route('/load_active_cases')
def load_active_cases():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/active_cases.html')

@app.route('/load_add_case')
def load_add_case():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/add_case.html')

@app.route('/load_view_case')
def load_view_case():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))

    return render_template("client_components/view_case.html")


    # Flask route – דוגמה

@app.route('/load_archived_cases')
def load_archived_cases():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/archived_cases.html')



@app.route('/load_clients_birds_view')
def load_clients_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/clients_birds_view.html')

@app.route('/load_active_clients')
def load_active_clients():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/active_clients.html')

@app.route('/load_add_client')
def load_add_client():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/add_client.html')

@app.route('/load_view_client')
def load_view_client():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))

    return render_template("client_components/view_client.html")



@app.route('/load_attendency_birds_view')
def load_attendency_birds_view():
    if not session.get('logged_in'):
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('home'))
    
    return render_template('client_components/attendency_birds_view.html')







if __name__ == '__main__':
    app.run(debug=True, port=5000)
