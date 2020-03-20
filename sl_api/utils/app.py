from flask import Flask

from utils.urls import init_blue
# from .ext import socketio_init_ext
from .ext import db_init_ext, api, swagger
# from .ext import celery
from .settings import TEMPLATE_DIR, STATIC_DIR,envs


def create_app(env=None):
    # 创建flask模型
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
    # 配置config
    app.config.from_object(envs.get(env))

    #初始化数据库
    db_init_ext(app)


    # celery.conf.update(app.config)

    swagger.init_app(app)
    # api
    api.init_app(app)
    # socketio_init_ext(app)
    # 初始化蓝图
    init_blue(app)



    return app