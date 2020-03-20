from flask import Blueprint


web_views = Blueprint("web_views",__name__)

from sl_web.index import index,login