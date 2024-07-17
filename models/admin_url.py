# 导入Flask相关模块，用于构建Web应用
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from models import redisdb
from config import Config

# 定义URL路由模块
admin_urls = Blueprint('admin_urls', __name__)
admin_urls.secret_key = Config.SECRET_KEY


@admin_urls.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        if session.get('email'):
            return redirect(url_for('urls.admin_index'))
        else:
            return render_template('admin/login.html')
    elif request.method == 'POST':
        data = request.form
        if data['email'] == Config.ADMIN_EMAIL and data['password'] == Config.ADMIN_PASSWORD:
            session['email'] = data['email']
            return render_template('admin/index.html')
        else:
            flash('邮箱或密码错误')
            # form返回
            return render_template('admin/login.html')
