import os
import subprocess
import sys
import threading
import time

from flask_script import Manager, Command
from flask_migrate import MigrateCommand

from utils.app import create_app


env = os.environ.get("FLASK_ENV") or "default"

app = create_app(env)
manager=Manager(app)
manager.add_command("db",MigrateCommand)


# class CeleryWorker(Command):
#     """Starts the celery worker."""
#     name = 'celery'
#     capture_all_args = True
#
#     def run(self, **argv):
#         cmd = ['celery', '-A', 'app.celeryInstance', 'worker'] + argv
#         ret = subprocess.call(cmd)
#         sys.exit(ret)


# manager.add_command("celery", CeleryWorker())



if __name__=="__main__":
  manager.run()




