
import functools

from flask import redirect, url_for, session


def login_required(func):
    """登录验证的装饰器"""
    @functools.wraps(func)
    def wraper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for(''))
    return wraper