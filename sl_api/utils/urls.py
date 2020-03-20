from assets.assets_views import assets_view
# from api.views import api_view
# from issue_bak.views.view import issue_views
from sl_web import web_views
from tasks import task_view


def init_blue(app):
    app.register_blueprint(blueprint=web_views, url_prefix='/')
    app.register_blueprint(blueprint=assets_view,url_prefix='/assets')
    # app.register_blueprint(blueprint=api_view, url_prefix='/api')
    app.register_blueprint(blueprint=task_view, url_prefix='/task')
