
# 导入 Flask 类，用于创建 Web 服务器
from flask import Flask
# 导入 logger 对象，用于记录日志
from loguru import logger
from config import Config
# 导入 URL 路由规则
from models.urls import urls
from models.admin_url import admin_urls


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(urls)
app.register_blueprint(admin_urls)
app.secret_key = app.config["SECRET_KEY"]


# 如果当前脚本作为主程序运行，则启动 Flask 应用程序
if __name__ == '__main__':
    # 启动 Flask 应用程序，参数来自配置文件
    app.run(
        debug=app.config['DEBUG'],
        host=app.config['SERVER_HOST'],
        port=app.config['SERVER_PORT']
    )
