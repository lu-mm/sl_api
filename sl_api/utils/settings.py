import os


# def get_database_uri(DATABASE):
#     db = DATABASE.get('db')
#     driver = DATABASE.get('driver')
#     user = DATABASE.get('user')
#     password = DATABASE.get('password')
#     host = DATABASE.get('host')
#     port = DATABASE.get('port')
#     name = DATABASE.get('name')
#
#     return '{}+{}://{}:{}@{}:{}/{}'.format(db, driver, user, password, host, port, name)






class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS=True
    access_key = ""
    access_secret = ""
    region_id=""


    # socket_message_queue='redis://10.211.55.7:6379/1'
    # CELERY_BROKER_URL='redis://10.211.55.7:6379/0'
    # CELERY_RESULT_BACKEND='redis://10.211.55.7:6379/0'
    # CELERY_TASK_SERIALIZER = 'json'
    # CELERY_TIMEZONE = 'Asia/Shanghai'
    # CELERY_ENABLE_UTC = True


class DevelopConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE = {
        'host': '',
        'port': 3306,
        'user': '',
        'password': '',
        'db': 'sl',
        'cursorclass':'pymysql.cursors.DictCursor'
    }
    logdir = "../logs"

    ansible_node_file="../file/ansible_cmdb_file/nodefile"
    ansible_host_file = "../file/ansible_cmdb_file/hosts"
    ansible_template= "../file/ansible_cmdb_file/sql.tpl"
    ansible_host_sql = "../file/ansible_cmdb_file/hosts.sql"
class ProdoctConfig(Config):
    DEBUG = False
    TESTING = False

    DATABASE = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'sl',
        'password': '123456',
        'db': 'sl',
        'charset' :'utf8mb4',
    }
    logdir = "../logs"
    ansible_node_file="../file/ansible_cmdb_file/nodefile"
    ansible_host_file = "../file/ansible_cmdb_file/hosts"
    ansible_template= "../file/ansible_cmdb_file/sql.tpl"
    ansible_host_sql = "../file/ansible_cmdb_file/hosts.sql"
    # SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)



envs = {
    "develop":DevelopConfig,
    "product":ProdoctConfig,
    "default":ProdoctConfig
}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
