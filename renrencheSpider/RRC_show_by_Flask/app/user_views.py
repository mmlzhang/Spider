
from flask import Blueprint, render_template


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register/')
def register():
    """注册"""
    return render_template('user/register.html')


@user_blueprint.route('/login/')
def login():
    """登录"""
    return render_template('user/login.html')


@user_blueprint.route('/logout/')
def logout():
    """注销"""
    return 'logout'
