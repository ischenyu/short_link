import sys

import yaml
import redis
from loguru import logger
from datetime import timedelta

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

if config:
    try:
        # 使用配置文件中的参数创建 Redis 客户端
        redis_client = redis.StrictRedis(
            host=config['redis']['host'],
            port=config['redis']['port'],
            password=config['redis']['password'],
            db=config['redis']['db']
        )
        logger.info("Redis 连接成功")
    except Exception as e:
        logger.error(f"Redis 连接失败: {e}")
        sys.exit()
else:
    logger.warning("未加载配置，无法连接 Redis")
    sys.exit()


def ensure_redis_connection():
    global redis_client
    try:
        # 尝试发送一个 PING 请求来测试连接是否正常
        redis_client.ping()
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
        # 如果连接异常或超时，重新建立连接
        logger.info('Redis 连接丢失，正在重新连接...')
        redis_client = redis.StrictRedis(
            host=config['redis']['host'],
            port=config['redis']['port'],
            password=config['redis']['password'],
            db=config['redis']['db']
        )


def link_add(email, link, str_link, expiration_days=30):
    ensure_redis_connection()
    try:
        # 使用哈希结构保存链接信息
        redis_client.hset('links', str_link, link)
        # 使用哈希结构保存邮箱信息
        redis_client.hset('users', str_link, email)
        # 设置整个哈希键的过期时间
        redis_client.expire('links', timedelta(days=expiration_days))
        redis_client.expire('users', timedelta(days=expiration_days))
        logger.info(f'{email} 添加链接 {link} 成功，短链接为 {str_link}')
        return True
    except Exception as e:
        logger.error(f'添加链接失败：{e}')
        return False


def link_get(short_link):
    # ensure_redis_connection()
    try:
        # 使用 hget 从哈希表 'links' 中获取原始链接
        jump_link = redis_client.hget('links', short_link)
        if jump_link:
            jump_link = jump_link.decode('utf-8')  # 将字节数据解码为字符串
            logger.info(f'获取链接 {jump_link} 成功')
            # 增加访问次数
            redis_client.hincrby('visits', short_link, 1)
            return jump_link
        else:
            logger.warning(f'短链接 {short_link} 不存在')
            return None
    except Exception as e:
        logger.error(f'获取链接失败：{e}')
        return None
