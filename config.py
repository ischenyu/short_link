

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

    # resend Email configuration
    SMTP_HOST = 'smtp.resend.com'
    SMTP_PORT = 465
    SMTP_USER = 'resend'
    SMTP_PASSWORD = 're_TRqawMh1_5wLdr6z8L5f777nk9t9yr7aN'
    SMTP_SENDER = 'paimon@alistnas.top'

    # Admin configuration
    ADMIN_EMAIL = 'abb1234aabb@gmail.com'
    ADMIN_PASSWORD = 'admin'

    # Google Recaptcha configuration
    Site_Key = '6Ld5smgmAAAAAHcQIxntBsbfm9N6d_EPCnyqtMfH'
    Secret_Key = '6Ld5smgmAAAAACCveB-L31-dGO7FOFRzb_pQ6n2c'
