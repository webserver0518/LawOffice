from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from app.utils.user_managment import UserManager
import socket, platform, psutil

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users_managment', methods=['POST'])
def users_managment():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

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

@admin_bp.route('/load_users_management')
def load_users_management():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))
    
    users = UserManager.load_users()
    return render_template('admin_components/users_management.html', users=users)

@admin_bp.route('/load_users_statistics')
def load_users_statistics():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))

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

@admin_bp.route('/load_server_info')
def load_server_info():
    if not session.get('logged_in') or session.get('user') != 'admin':
        flash("⛔ אין הרשאה", "danger")
        return redirect(url_for('site.home'))



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
