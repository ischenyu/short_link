import random
import string

from flask import Blueprint, request, render_template, session, jsonify

from models import email

user_urls = Blueprint('user_urls', __name__)


@user_urls.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        if session.get('email'):
            pass
        else:
            return render_template('user/login.html', title='用户登录')


@user_urls.route('/user/code', methods=['POST'])
def user_get_code():
    # 生成6位验证码
    code = ''.join(random.sample(string.ascii_letters + string.digits, 6))
    try:
        data = request.get_json()
        user_email = data['email']
    except KeyError:
        return jsonify({
            'code': 500,
            'msg': '邮箱不能为空'
        })
    try:
        email.send_email('验证码', '您的验证码是：' + code, user_email)
        return jsonify({
            'code': 200,
            'msg': '验证码发送成功'
        })
    except Exception as e:
        return jsonify({
            'code': 500,
            'msg': f'验证码发送失败 error: {e}'
        })
