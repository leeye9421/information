import random
import re

from datetime import datetime
from flask import current_app, jsonify
from flask import json
from flask import make_response
from flask import request
from flask import session

from info import constants, db
from info import redis_store
from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET
from . import passport_blu


# 短信验证码
@passport_blu.route('/sms_code',methods = ['POST'])
def get_sms_code():
    # 1.获取参数：手机号、uuid、图片验证码
    json_data = request.data
    dict_data = json.loads(json_data)
    mobile = dict_data.get('mobile')
    image_code = dict_data.get('image_code')
    image_code_id = dict_data.get('image_code_id')
    print(dict_data)
    # 2.校验参数是否为空
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')
    # 3.验证手机号格式
    if not re.match('1[356789]\\d{9}',mobile):
        return jsonify(errno=RET.DATAERR,errmsg='手机号格式错误')
    # 4.取出uuid在redis中对应的图片验证码
    try:
        redis_image_code = redis_store.get('image_code:%s'%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg='查找图片验证码失败')
    # 5.判断图片验证码是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA,errmsg='图片验证码过期')
    # 6.判断验证码是否一致
    if image_code.lower() != redis_image_code.lower():
        return jsonify(errno=RET.DATAERR,errmsg='图片验证码不正确')
    # 7.生成短信验证码
    sms_code = '%06d'%random.randint(0,999999)

    # 8.通过云通讯发送短信验证码（手机号，（短信验证码、有效期），模板）
    # ccp = CCP()
    # result = ccp.send_template_sms(mobile,[sms_code,5],1)
    # if result == -1:
    #     return jsonify(errno=RET.THIRDERR,errmsg='短信验证码发送失败')

    current_app.logger.debug('短信验证码是：%s'%sms_code)

    # 9.保存到redis
    try:
        redis_store.set('sms_code:%s' % mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR,errmsg='短信保存失败')
    # 10.返回前端
    return jsonify(errno=RET.OK,errmsg='发送成功')



# 图片验证码
@passport_blu.route('/image_code')
def get_image_code():
    # 1,获取参数
    # 2.生成验证码
    # 3.保存到redis
    # 5.返回图片验证码

    # 1.获取当前验证码图片的编号id
    code_id = request.args.get('code_id')

    pre_id = request.args.get('pre_id')
    # 2.生成验证码
    name, text, image_data = captcha.generate_captcha()
    # 3.保存到redis
    try:
        redis_store.set('image_code:%s'%code_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)

        if pre_id:
            redis_store.delete('image_code:%s' %pre_id)
    except Exception as e:
        current_app.logger.error(e)

    # 4.返回验证码,设置返回数据格式
    response = make_response(image_data)
    response.headers['Content-Type'] = 'image/jpg'
    return response


# 注册用户
@passport_blu.route('/register', methods=['POST'])
def register():
    # 1.获取参数
    dict_data = request.json
    mobile = dict_data.get('mobile')
    sms_code = dict_data.get('sms_code')
    password = dict_data.get('password')
    # 2.判断是否为空
    if not all([mobile,sms_code,password]):
        return jsonify(errno=RET.PARAMERR,errmsg='参数不完整')
    # 3.验证手机号格式
    if not re.match('1[356789]\\d{9}',mobile):
        return jsonify(errno=RET.DATAERR, errmsg='手机号格式错误')
    # 4.根据手机号从redis中取出对应的短信验证码
    try:
        redis_sms_code = redis_store.get('sms_code:%s'%mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取短信验证码异常')
    # 5.判断是否过期
    if not redis_sms_code:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码过期')
    # 6.判断验证码是否一致
    if sms_code != redis_sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码填写错误')
    # 7.创建用户，设置属性
    user = User()
    user.nick_name = mobile
    user.mobile = mobile
    user.password = password
    # 8.保存到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='用户保存异常')
    # 9.返回前端页面
    return jsonify(errno=RET.OK, errmsg='注册成功')


# 登陆用户
@passport_blu.route('/login', methods=['POST'])
def login():
    # 1.获取参数
    dict_data = request.json
    mobile = dict_data.get('mobile')
    password = dict_data.get('password')
    # 2.判断参数是否为空
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 3.通过手机号取出用户对象
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询异常')
    # 4.判断用户对象是否存在
    if not user:
        return jsonify(errno=RET.NODATA, errmsg='该用户不存在')
    # 5.判断密码是否正确
    if not user.check_passowrd(password):
        return jsonify(errno=RET.PWDERR, errmsg='密码输入错误')
    # 6.记录用户的登陆状态
    session['user_id'] = user.id
    session['nick_name'] = user.nick_name
    session['mobile'] = user.mobile
    #记录用户的最后登陆时间
    user.last_login = datetime.now()
    # 7.返回前端页面
    return jsonify(errno=RET.OK, errmsg='登陆成功')


# 登出功能
@passport_blu.route('/logout',methods=['POST'])
def logout():
    session.pop('user_id',None)
    session.pop('nick_name',None)
    session.pop('mobile',None)

    return jsonify(errno=RET.OK,errmsg="ok")