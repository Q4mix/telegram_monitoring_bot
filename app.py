from flask import Flask, render_template, request, redirect, url_for, session, send_file
import json
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = 'maxfiy_kalit_123'

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "12ev38zs5Za0JcLccE"
LOG_FILE = "log.json"

@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template('login.html', error="Login yoki parol noto‘g‘ri")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except:
        logs = []

    total_logs = len(logs)
    sos_logs = [log for log in logs if 'sos' in log.get('message', '').lower()]
    sos_count = len(sos_logs)

    return render_template('dashboard.html', total_logs=total_logs, sos_count=sos_count)

@app.route('/logs')
def logs():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    query = request.args.get('q', '').lower()

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except:
        logs = []

    if query:
        filtered_logs = [log for log in logs if query in log.get('message', '').lower()]
    else:
        filtered_logs = logs

    return render_template('logs.html', logs=filtered_logs, query=query)

@app.route('/download')
def download():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    except:
        logs = []

    df = pd.DataFrame(logs)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Logs')
    output.seek(0)

    return send_file(output, attachment_filename="logs.xlsx", as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
