

class Config:
    # Server configuration
    SERVER_HOST = '0.0.0.0'
    SERVER_PORT = 5001
    DEBUG = False
    SECRET_KEY = 'rzbw4hb12yz29ey7530j'

    # Redis configuration
    REDIS_HOST = '192.168.1.3'
    REDIS_PORT = 6379
    REDIS_PASSWORD = 'Dingtalk1234561017'
    REDIS_DB = 0

    # Email configuration
    SMTP_HOST = 'smtp.163.com'
    SMTP_PORT = 465
    SMTP_USER = 'abb1234aabb@163.com'
    SMTP_PASSWORD = 'ENWHVUCJXFARZRBA'
    SMTP_SENDER = 'paimon@alistnas.top'

    # Admin configuration
    ADMIN_EMAIL = 'abb1234aabb@gmail.com'
    ADMIN_PASSWORD = 'admin'
