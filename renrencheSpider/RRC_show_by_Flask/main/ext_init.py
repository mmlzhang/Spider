
"""注册要初始化的app"""

from flask_session import Session
from flask_wtf import CSRFProtect

from app.models import db


# session会话设置
session = Session()
# 使用wtf提供的csrf保护机制
csrf = CSRFProtect()


def ext_init(app):
    session.init_app(app=app)
    # db.init_app(app=app)
    csrf.init_app(app=app)