from logging.handlers import RotatingFileHandler

import logging
from flask.ext.wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from config import Config,config_dict
from flask import Flask
import redis


db = SQLAlchemy()

redis_store = None
def create_app(config_name):

    app = Flask(__name__)

    # 获取对应的配置类
    config = config_dict[config_name]
    # 日志方法调用
    log_file(config.LOG_LEVEL)
    # 根据配置类获取对应的配置信息
    app.config.from_object(config)

    # 1、创建数据库对象
    db.init_app(app)


    # 2、创建redis对象
    global redis_store
    redis_store = redis.StrictRedis(Config.REDIS_HOST, Config.REDIS_PORT, decode_responses=True)

    # 3、创建session对象
    Session(app)

    # 4、创建csrf
    # CSRFProtect(app)

    # 注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)

    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)

    return app

# 日志
def log_file(level):
    # 设置日志的记录等级
    logging.basicConfig(level=level) # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)