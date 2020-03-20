from flask import Blueprint

from .task import CommandApi

task_view = Blueprint("task_view",__name__)
