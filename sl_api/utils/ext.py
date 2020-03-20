import os

import pymysql
from celery import Celery
from flask_migrate import Migrate
from flask_restful import Api
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

from utils.pymysql import SQLManager
from utils.settings import envs
from utils.web_log import _LogFactory


env = os.environ.get("FLASK_ENV") or "default"
config = envs.get(env)

migrate = Migrate()
api=Api()
# socketio = SocketIO()
db = SQLManager()





def mylog():
    if config.DEBUG==True:
        logger=_LogFactory.get_logger('CONSOLE')
    else:
        logger=_LogFactory.get_logger('LOGGER')
    return logger

# celery = Celery(__name__, broker=config.CELERY_BROKER_URL)
# celery.conf.ONCE = {
#   'backend': 'celery_once.backends.Redis',
#   'settings': {
#     'url': 'redis://10.211.55.7:6379/0',
#     'default_timeout': 60 * 60
#   }
# }

swagger_template = {
  "swagger": "2.0",
  "info": {
    "title": "Al API",
    "description": "API for my data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "shijingjing@lushangyouwo.com",
      "url": "www.sl.com",
    },
    "termsOfService": "http://www.sl.com/terms",
    "version": "0.0.1"
  },
  "host": "www.sl.com",  # overrides localhost:500
  "basePath": "/apidocs",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/api/"
}

swagger = Swagger(config=swagger_config)


def db_init_ext(app):
    # db.init_app(app)
    migrate.init_app(app,db)

# def socketio_init_ext(app):
#     socketio.init_app(app,message_queue=config.socket_message_queue)





