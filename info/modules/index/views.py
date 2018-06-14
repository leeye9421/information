from flask import current_app
from flask import session

from info.models import User
from . import index_blu
from flask import render_template
from info import redis_store


@index_blu.route('/')
def index():
    user_id = session.get('user_id')
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)

    return render_template('news/index.html',data={'user_info':user.to_dict() if user else None})


@index_blu.route('/favicon.ico')
def log():
    return current_app.send_static_file('news/favicon.ico')