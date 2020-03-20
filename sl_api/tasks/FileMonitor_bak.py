from datetime import datetime,timedelta
from watchdog.events import FileSystemEventHandler
import time
from watchdog.observers import Observer
from utils.ext import celery


class FileMonitor(FileSystemEventHandler):

    def __init__(self):
        self.last_modified = datetime.now()

    def on_modified(self, event):
        if datetime.now() - self.last_modified < timedelta(seconds=1):
            return
        else:
            self.last_modified = datetime.now()
        print(f'Event type: {event.event_type}  path : {event.src_path}')
        print(event.is_directory) # This attribute is also available




@celery.task()
def file_watchdog():
  path = 'ansible_app/hosts'
  event_handler = FileMonitor()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()




