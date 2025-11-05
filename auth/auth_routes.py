from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from database.sql_provider import SQLProvider
import os
from auth.model_route_auth import auth_req, reg_exist_check, reg_new
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
sql_path = os.path.join(os.path.dirname(__file__), 'sql')
print("SQL folder path:", sql_path)
print("Files:", os.listdir(sql_path))

@auth_bp.route('/login', methods=['GET'])
def auth_index():
    if 'user_group' in session:
        session.clear()
    return render_template('static.html')


@auth_bp.route('/login', methods=['POST'])
def auth_main():
    user_data = request.form
    res_info = auth_req(current_app.config['db_config'], user_data, provider)
    print(res_info)
    if not res_info.status:
        return render_template('error_auth.html', message="Ошибка сервера")
    if not res_info.result:
        return render_template('error_auth.html', message="Такой пользователь не существует")

    session['user_group'] = res_info.result[0][3]
    session['user_id'] = res_info.result[0][0]
    session.permanent = True
    print('Выполнена аутентификация')
    return redirect(url_for('main_menu'))

@auth_bp.route('/registration', methods=['GET'])
def registration_index():
    return render_template('registration.html')

@auth_bp.route('/registration', methods=['POST'])
def registration_main():
    if 'user_group' in session:
        session.clear()
    user_data = request.form
    if user_data['password'] != user_data['password1']:
        return render_template('error_auth.html', message= "пароли не совпадает")
    if 'user_id' in session:
        return render_template('error_auth.html', message="Вы не вышли из учётной записи")

    res_info = reg_exist_check(current_app.config['db_config'], user_data, provider)
    print(res_info)
    if not res_info.status:
        return render_template('error_auth.html', message="Ошибка сервера")
    if res_info.result:
        return render_template('error_auth.html', message="Такой пользователь уже существует")

    res_info = reg_new(current_app.config['db_config'], user_data, provider)
    if not res_info.status:
        return render_template('error_auth.html', message="Ошибка сервера")

    print("Регистрация успешна")
