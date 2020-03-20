
from tasks.FileMonitor_bak import file_watchdog



def HostMonitor():
    file_watchdog.delay()
    return {'msg': 'ok', 'code': 200}