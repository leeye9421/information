import redis


class Config(object):
    SECRET_KEY = 'JDASDJADIAJDASIDJSA'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@localhost:3306/information'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis配置
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = '6379'

    # session配置
    SESSION_TYPE = 'redis'  # 指定存储类型为redis数据库
    SESSION_USE_SIGNER = True  # 开启签名加密
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 制定redis数据库的地址
    permanent_session_lifetime = 3600 * 24 * 7  # 设置session过期时间


class ProductConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True


config_dict = {
    'develop':DevelopmentConfig,
    'product':ProductConfig,
}