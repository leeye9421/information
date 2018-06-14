from flask import current_app
from . import index_blu
from flask import render_template
from info import redis_store


@index_blu.route('/')
def index():
    return render_template('news/index.html')


@index_blu.route('/favicon.ico')
def log():
    return current_app.send_static_file('news/favicon.ico')