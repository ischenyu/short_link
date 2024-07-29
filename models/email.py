import resend
import config

resend.api_key = config.Config.SMTP_PASSWORD


def send_email(subject, code, to_emails):
    """
    发送邮件的函数。

    :param subject: 邮件主题
    :param message: 邮件正文
    :param to_emails: 收件人列表
    """

    params: resend.Emails.SendParams = {
        "from": "Paimon <paimon@alistnas.top>",
        "to": to_emails,
        "subject": subject,
        "html": "<h2>验证码</h2></br><p>你的验证码是：</p><strong style='width: 100%;'>"+ code + "</strong></br><p>，十分钟内有效，请勿将验证码泄露给其他人。</p>",
    }
    r = resend.Emails.send(params)
    print(r)
