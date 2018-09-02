
from .rrc_views import rrc_blueprint
from .user_views import user_blueprint
# from .html_views import html_blueprint


def rrc_blueprint_register(app):
    # 注册蓝图
    app.register_blueprint(blueprint=rrc_blueprint,
                           url_prefix='/rrc')
    app.register_blueprint(blueprint=user_blueprint,
                           url_prefix='/user')

    # app.register_blueprint(blueprint=html_blueprint,
    #                        url_prefix='/html')
