# 导入secrets模块，用于生成安全的随机数，用于加密等场景
import secrets
# 导入string模块，提供各种字符串常量
import string
import redis
# 导入Flask相关模块，用于构建Web应用
from flask import Blueprint, render_template, request, jsonify
# 导入loguru模块，用于日志记录
from loguru import logger
# 导入Redis数据库操作模块
from models import redisdb
from config import Config
import requests


# 定义URL路由模块
urls = Blueprint('urls', __name__)
# 设置Flask应用的秘钥，用于加密cookie等
urls.secret_key = Config.SECRET_KEY
site_key = Config.Site_Key
secret_key = Config.Secret_Key


# 生成指定长度的随机安全字符串
def create_secure_str(length):
    """
    生成指定长度的安全随机字符串。

    :param length: 生成字符串的长度
    :return: 由字母和数字组成的随机字符串
    """
    letters = string.ascii_letters + string.digits
    secure_str = ''.join(secrets.choice(letters) for _ in range(length))
    return secure_str


# 主页路由，返回主页模板
@urls.route('/')
def index():
    return render_template('index.html', site_key=site_key)


# 短链接路由，尝试从Redis中获取原始链接并返回跳转页面
@urls.route('/<short_link>', methods=['GET'])
def get_link(short_link):
    try:
        original_link = redisdb.link_get(short_link)
        if original_link:
            return render_template('jump.html', original_link=original_link)
        else:
            return render_template('404.html'), 404
    except redis.exceptions.RedisError as e:
        logger.error('发生Redis错误', exc_info=True)
        return render_template('error.html', e=e)


# 新增链接接口，接收POST请求，添加链接到Redis并返回短链接
@urls.route('/api/user/new', methods=['POST'])
def add_link():
    try:
        data = request.get_json()
        recaptcha_response = data.get('g-recaptcha-response')
        # logger.info(data)

        if not recaptcha_response:
            return jsonify({'success': False, 'message': '验证码未填写'}), 400

        recaptcha_url = 'https://recaptcha.net/recaptcha/api/siteverify'
        recaptcha_data = {
            'secret': secret_key,
            'response': recaptcha_response
        }

        recaptcha_verify = requests.post(recaptcha_url, data=recaptcha_data)
        recaptcha_result = recaptcha_verify.json()
        logger.info(recaptcha_result)
        if not recaptcha_result['success']:
            return jsonify({'success': False, 'message': '验证码错误'}), 400

        if data:
            email = data['email']
            link = data['original_url']
            str_link = create_secure_str(6)
            if redisdb.link_add(email, link, str_link):
                return jsonify({'code': 200, 'shortened_url': 'https://s.alistnas.top/' + str_link})
        else:
            logger.error('data is None')
            return jsonify({'code': 400, 'message': '请求数据为空'})
    except Exception as e:
        logger.error(e)
        return jsonify({'code': 501, 'message': '服务器错误'})
