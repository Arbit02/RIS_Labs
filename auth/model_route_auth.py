from dataclasses import dataclass
from database.select import select_string
from database.insert import insert_one
from database.sql_provider import SQLProvider
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class ProductInfoResponse:
    result: tuple
    error_message: str
    status: bool

def auth_req(db_config, user_input_data, sql_provider):
    _sql = sql_provider.get('user.sql', input_login=user_input_data['login'])
    result, schema = select_string(db_config, _sql)
    if not result:
        return ProductInfoResponse(tuple(), error_message="Пользователь не найден", status=False)

    stored_hash = result[0][2]
    if check_password_hash(stored_hash, user_input_data['password']):
        return ProductInfoResponse(result, error_message='', status=True)
    else:
        return ProductInfoResponse(tuple(), error_message="Неверный пароль", status=False)



def reg_exist_check(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('user_check.sql', input_login=user_input_data['login'])
    result, schema = select_string(db_config, _sql)
    if result:
        return ProductInfoResponse(result, error_message=error_message, status=True)
    return ProductInfoResponse(tuple(), error_message=error_message, status=False)


def reg_new(db_config, user_input_data, sql_provider):
    error_message = ''
    hashed_password = generate_password_hash(user_input_data['password'])
    _sql = sql_provider.get('user_new.sql',
                            input_login=user_input_data['login'],
                            input_password=hashed_password,
                            input_group='user')
    result = insert_one(db_config, _sql)
    if result:
        return ProductInfoResponse(tuple(), error_message=error_message, status=True)
    return ProductInfoResponse(tuple(), error_message=error_message, status=False)
