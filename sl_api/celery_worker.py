import os

from utils.app import create_app
from utils.ext import celery
from utils.settings import envs

env = os.environ.get("FLASK_ENV") or "default"

app = create_app(env)
app.app_context().push()