from flask import Blueprint

assets_view = Blueprint("assets_view",__name__)

from .assets_views import AssetsList,AliyunEcsList,AssetsUpdate
