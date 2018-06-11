from flask import Flask
from config import Config
from flask.ext.wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import redis

app = Flask(__name__)

REDIS_STORE = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)

app.config.from_object(Config)
CSRFProtect(app)
Session(app)

db = SQLAlchemy(app)