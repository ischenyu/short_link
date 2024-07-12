# 导入secrets模块，用于生成安全的随机数，用于加密等场景
import secrets
# 导入string模块，提供各种字符串常量
import string
# 导入yaml模块，用于解析和生成YAML格式的配置文件
import yaml

# 导入Flask相关模块，用于构建Web应用
from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
# 导入loguru模块，用于日志记录
from loguru import logger
# 导入Redis数据库操作模块
from models import redisdb

# 尝试加载配置文件，如果失败则记录错误并使用默认配置或空配置
# 加载 YAML 配置文件
try:
    with open('./config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    logger.error("配置文件未找到")
    config = None
except yaml.YAMLError as exc:
    logger.error(f"YAML 解析错误: {exc}")
    config = None

# 定义URL路由模块
urls = Blueprint('urls', __name__)
# 设置Flask应用的秘钥，用于加密cookie等
urls.secret_key = config['server']['secret_key']

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
    return render_template('index.html')

# 短链接路由，尝试从Redis中获取原始链接并返回跳转页面
@urls.route('/<short_link>', methods=['GET'])
def get_link(short_link):
    try:
        original_link = redisdb.link_get(short_link)
        if original_link:
            return render_template('jump.html', original_link=original_link)
        else:
            return render_template('404.html'), 404
    except Exception as e:
        logger.error(f'服务器错误：{e}')
        return render_template('error.html', e=e)

# 新增链接接口，接收POST请求，添加链接到Redis并返回短链接
@urls.route('/api/user/new', methods=['POST'])
def add_link():
    try:
        data = request.get_json()
        logger.info(data)
        if data:
            email = data['email']
            link = data['original_url']
            str_link = create_secure_str(6)
            if redisdb.link_add(email, link, str_link):
                return jsonify({'code': 200, 'shortened_url': 'https://s.alistnas.top/' + str_link})
            else:
                return jsonify({'code': 500, 'message': ''})
        else:
            logger.error('data is None')
            return jsonify({'code': 500})
    except Exception as e:
        logger.error(e)
        return jsonify({'code': 500, 'message': 'Server error'})

# 管理员登录路由，支持GET和POST请求，用于登录验证和登录页面展示
@urls.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        if session.get('email'):
            return redirect(url_for('urls.admin_index'))
        else:
            return render_template('admin/login.html')
    elif request.method == 'POST':
        data = request.form
        if data['email'] == config['admin']['email'] and data['password'] == config['admin']['password']:
            session['email'] = data['email']
            return render_template('admin/index.html')
        else:
            flash('邮箱或密码错误')
            # form返回
            return render_template('admin/login.html')
