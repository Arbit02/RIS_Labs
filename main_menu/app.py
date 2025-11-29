import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, render_template, session, json, redirect,url_for
from query_bp.route import query_bp
from reports_bp.reports_routes import report_bp
from auth.auth_routes import auth_bp
from access import login_required, group_required
from flask_assets import Environment, Bundle
app = Flask(__name__)
assets_env = Environment(app)
app.config['ASSETS_DEBUG'] = False
assets_env.init_app(app)


with open("../data/db_config.json") as f:
    app.config['db_config'] = json.load(f)

with open("../data/db_auth_check.json") as f:
    app.config['db_access'] = json.load(f)


app.secret_key = 'You will never guess'

app.register_blueprint(query_bp, url_prefix='/query')

app.register_blueprint(auth_bp, url_prefix='/auth')

app.register_blueprint(report_bp, url_prefix='/report')

@app.route('/')
@login_required
def main_menu():
    return render_template('/pages/index.html')

@app.route('/exit')
@group_required
def exit_func():
    if 'user_group' in session:
        session.clear()
        return render_template('logout.html')
    return redirect(url_for('main_menu'))

@app.route('/error')
def error_message():
    return render_template("error.html", message="Какая-то ошибка :(")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)