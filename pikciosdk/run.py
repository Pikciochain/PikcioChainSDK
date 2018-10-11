import os
import log
import sys
from log import CustomDailyLogFile

from twisted.application import service, app
from twisted.python.log import ILogObserver

from pattern import Register
from config import get_config
from tests import run_test

config = get_config()

try:
    approot = os.path.dirname(os.path.realpath(__file__))
except NameError:  # We are the main py2exe script, not a module
    approot = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(approot)
Register.set('approot', approot)

PACKAGE_DIR = 'Safe2Net'

app_name = config.get('application', 'name')
application = service.Application(app_name)
log_file = config.get('log', 'file')
log_path = config.get('log', 'directory')
log_level = config.get('log', 'level')

logfile = CustomDailyLogFile(log_file, log_path)

application.setComponent(ILogObserver, log.FileLogObserver(
    logfile, log_level, exclude_systems=[]).emit)

if __name__ == '__main__':
    app_config = {
        'no_save': True,
        'nodaemon': False,
        'profile': False,
        'debug': False
    }

    oldstdout = sys.stdout
    oldstderr = sys.stderr

    profiler = app.AppProfiler(app_config)
    logger = app.AppLogger(app_config)

    logger.start(application)
    sys.stdout = oldstdout
    run_test()
    logger.stop()
