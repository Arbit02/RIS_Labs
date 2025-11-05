from database.DBcm import DBContextManager
from pymysql.err import OperationalError


def select_list(db_config: dict, _sql: str, params=None):
    result = ()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql, params)
                result = cursor.fetchall()
            except OperationalError as error:
                print("error: ", error.args)
                return result, schema
            else:
                print("Cursor no errors")

            schema = [item[0] for item in cursor.description]

    return result, schema

def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict


def select_string(db_config: dict, _sql: str):
    result = dict()
    schema = list()
    print(_sql)

    with DBContextManager(db_config) as cursor:

        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
                result = cursor.fetchall()
            except OperationalError as error:
                print("error: ", error)
                return result
            else:
                print("Cursor no errors")

            schema = [item[0] for item in cursor.description]

    return result, schema