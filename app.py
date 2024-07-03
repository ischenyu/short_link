import secrets
import string

import yaml
from flask import Flask, render_template, request, jsonify
from loguru import logger

from models import redisdb

app = Flask(__name__)

# 加载 YAML 配置文件
try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError:
    logger.error("配置文件未找到")
    config = None
except yaml.YAMLError as exc:
    logger.error(f"YAML 解析错误: {exc}")
    config = None

def create_secure_str(length):
    letters = string.ascii_letters + string.digits
    secure_str = ''.join(secrets.choice(letters) for _ in range(length))
    return secure_str


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<short_link>', methods=['GET'])
def get_link(short_link):
    if short_link == 'favicon.ico':
        pass
    else:
        try:
            original_link = redisdb.link_get(short_link)
            if original_link:
                return render_template('jump.html', original_link=original_link)
            else:
                return render_template('404.html'), 404
        except Exception as e:
            logger.error(f'服务器错误：{e}')
            return render_template('error.html', e=e)


@app.route('/api/user/new', methods=['POST'])
def add_link():
    try:
        data = request.get_json()
        logger.info(data)
        if data:
            email = data['email']
            link = data['original_url']
            str_link = create_secure_str(6)
            if redisdb.link_add(email, link, str_link):
                return jsonify({'code': 200, 'shortened_url': 'https://s.alistnas.top/'+str_link})
            else:
                return jsonify({'code': 500, 'message': ''})
        else:
            logger.error('data is None')
            return jsonify({'code': 500})
    except Exception as e:
        logger.error(e)
        return jsonify({'code': 500, 'message': 'Server error'})


if __name__ == '__main__':
    app.run(
        debug=config['server']['debug'],
        host=config['server']['host'],
        port=config['server']['port'],
        threading=config['server']['threading']
    )

