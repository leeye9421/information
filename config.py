import logging
import redis

class Config(object):
    SECRET_KEY = 'ADJSDSAHSIDAHDA'

    # 配置mysql数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置redis数据库
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

    # 配置session
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    LOG_LEVEL = logging.ERROR

config_dict = {
    'develop':DevelopmentConfig,
    'product':ProductionConfig
}

