
from flask import Flask

from app.blueprint import rrc_blueprint_register
from .ext_init import ext_init
from .settings import MAIN_CONFIG, STATIC_DIR, \
    TEMPLATES_DIR, start_logging
from utils.functions import RegexConverter


def create_app():
    """ 创建app,注册配置 """
    # 开启日志
    # start_logging()
    # 初始化 app
    app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
    # 注册蓝图
    rrc_blueprint_register(app=app)
    # 增加配置文件
    app.config.update(MAIN_CONFIG)
    # 为app中的url路由添加正则表达式匹配
    app.url_map.converters['regex'] = RegexConverter
    # 扩展初始化 app
    ext_init(app=app)
    return app
