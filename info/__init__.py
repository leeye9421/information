from flask import Flask
from config import Config,config_dict
from flask.ext.wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import redis



redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)




db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # 加载配置
    app.config.from_object(config_dict(config_name))
    # 配置数据库
    db.init_app(app)
    # 配置redis
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
    # 开启csrf保护
    CSRFProtect(app)
    # 创建session对象关联app
    Session(app)

    return app


