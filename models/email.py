import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import yaml
from loguru import logger

# 加载 YAML 配置文件
try:
    with open('./config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        smtp_host = config['email']['smtp_host']
        smtp_port = config['email']['smtp_port']
except FileNotFoundError:
    logger.error("配置文件未找到")
    config = None
except yaml.YAMLError as exc:
    logger.error(f"YAML 解析错误: {exc}")
    config = None


def send_email(subject, message, to_emails):
    """
    发送邮件的函数。

    :param subject: 邮件主题
    :param message: 邮件正文
    :param to_emails: 收件人列表
    """

    # 邮件发送者信息
    from_email = config['email']['from_email']
    password = str(['email']['smtp_password'])

    # 创建一个MIMEMultipart对象并设置邮件头信息
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    # 将邮件正文添加到MIMEText对象中，并将其作为MIMEMultipart对象的一部分
    msg.attach(MIMEText(message, 'plain'))

    # 连接到SMTP服务器并发送邮件
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_emails, text)
    server.quit()
