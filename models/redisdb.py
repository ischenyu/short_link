import redis
from loguru import logger
from datetime import timedelta
from contextlib import contextmanager
from config import Config


@contextmanager
def redis_connection():
    """上下文管理器，用于管理Redis连接"""
    try:
        client = redis.StrictRedis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASSWORD,
            db=Config.REDIS_DB,
        )
        yield client
    except Exception as e:
        logger.error(f"Redis 连接失败: {e}")
        raise
    finally:
        client.connection_pool.disconnect()


def link_add(email, link, str_link, expiration_days=30):
    try:
        with redis_connection() as redis_client:
            with redis_client.pipeline() as pipe:
                # 使用哈希结构保存链接信息
                pipe.hset('links', str_link, link)
                # 使用哈希结构保存邮箱信息
                pipe.hset('users', str_link, email)
                # 设置整个哈希键的过期时间
                pipe.expire('links', timedelta(days=expiration_days))
                pipe.expire('users', timedelta(days=expiration_days))
                pipe.execute()
            logger.info(f'{email} 添加链接 {link} 成功，短链接为 {str_link}')
            return True
    except Exception as e:
        logger.error(f'添加链接失败：{e}')
        return False


def link_get(short_link):
    try:
        with redis_connection() as redis_client:
            with redis_client.pipeline() as pipe:
                # 使用 hget 从哈希表 'links' 中获取原始链接
                pipe.hget('links', short_link)
                pipe.hincrby('visits', short_link, 1)
                jump_link, visits = pipe.execute()
            if jump_link:
                jump_link = jump_link.decode('utf-8')  # 将字节数据解码为字符串
                logger.info(f'获取链接 {jump_link} 成功')
                return jump_link
            else:
                logger.warning(f'短链接 {short_link} 不存在')
                return None
    except Exception as e:
        logger.error(f'获取链接失败：{e}')
        return None
