# 导入 yaml 库，用于读取配置文件
import yaml
# 导入 Flask 类，用于创建 Web 服务器
from flask import Flask
# 导入 logger 对象，用于记录日志
from loguru import logger

# 导入 URL 路由规则
from models.urls import urls

# 尝试读取配置文件并解析为 Python 对象
try:
    # 打开配置文件
    with open('config.yaml', 'r') as file:
        # 安全加载 YAML 文件内容
        config = yaml.safe_load(file)
# 如果配置文件不存在，记录错误日志并设置 config 为 None
except FileNotFoundError:
    logger.error("配置文件未找到")
    config = None
# 如果 YAML 文件内容解析出错，记录错误日志并设置 config 为 None
except yaml.YAMLError as exc:
    logger.error(f"YAML 解析错误: {exc}")
    config = None

# 初始化 Flask 应用程序
app = Flask(__name__)
# 注册 URL 路由规则
app.register_blueprint(urls)
# 设置应用程序的密钥，用于加密数据
app.secret_key = config['server']['secret_key']

# 如果当前脚本作为主程序运行，则启动 Flask 应用程序
if __name__ == '__main__':
    # 启动 Flask 应用程序，参数来自配置文件
    app.run(
        debug=config['server']['debug'],
        host=config['server']['host'],
        port=config['server']['port']
    )
