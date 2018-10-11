import os
import sys
from datetime import timedelta, date

from twisted.python import log
from twisted.python.logfile import DailyLogFile

from config import get_config

INFO = 5
DEBUG = 4
WARNING = 3
ERROR = 2
CRITICAL = 1


class FileLogObserver(log.FileLogObserver):
    def __init__(self, f=None, level=WARNING, default=DEBUG,
                 filter_systems=None, exclude_systems=None):
        log.FileLogObserver.__init__(self, f or sys.stdout)
        self.level = level
        self.default = default
        self.filter_systems = filter_systems
        self.exclude_systems = exclude_systems

    def emit(self, event_dict):
        ll = event_dict.get('loglevel', self.default)
        if event_dict['isError'] or 'failure' in event_dict or \
                self.level >= ll:
            system = event_dict.get('system')
            if self.filter_systems:
                if not system or system not in self.filter_systems:
                    return
            if self.exclude_systems:
                if system and system in self.exclude_systems:
                    return
            log.FileLogObserver.emit(self, event_dict)


class Logger:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def msg(self, message, **kw):
        kw.update(self.kwargs)
        if 'system' in kw and not isinstance(kw['system'], str):
            kw['system'] = kw['system'].__class__.__name__
        log.msg(message, **kw)

    def info(self, message, **kw):
        kw['loglevel'] = INFO
        self.msg("[INFO] %s" % message, **kw)

    def debug(self, message, **kw):
        kw['loglevel'] = DEBUG
        self.msg("[DEBUG] %s" % message, **kw)

    def warning(self, message, **kw):
        kw['loglevel'] = WARNING
        self.msg("[WARNING] %s" % message, **kw)

    def error(self, message, **kw):
        kw['loglevel'] = ERROR
        self.msg("[ERROR] %s" % message, **kw)

    def critical(self, message, **kw):
        kw['loglevel'] = CRITICAL
        self.msg("[CRITICAL] %s" % message, **kw)


class CustomDailyLogFile(DailyLogFile):
    # exactly like the dailyLogFile class from python.twisted logfile
    # except it check every time it's rotating, that there's no old log to
    # delete time for old log is defined in the app's config file

    config = get_config()
    if not os.path.exists(config.get('log', 'directory')):
        os.makedirs(config.get('log', 'directory'))

    def rotate(self):
        DailyLogFile.rotate(self)
        self.delete_old_logs()

    def delete_old_logs(self):
        # delete logs if they're older than the lifetime
        config = get_config()
        log_lifetime = config.get('log', 'lifetime')
        if log_lifetime > 0:
            lifetime = timedelta(days=int(log_lifetime))
            today = date.today()
            limitation_day = today - lifetime
            for fichier in os.listdir(self.directory):
                if not os.path.isdir(fichier):
                    old_date = fichier.strip(self.name)
                    year_month_day = old_date.split('_')
                    if len(year_month_day) == 3:
                        try:
                            old_file_date = date(int(year_month_day[0]),
                                                 int(year_month_day[1]),
                                                 int(year_month_day[2]))
                            if old_file_date < limitation_day:
                                os.remove(self.directory + '/' + fichier)
                        except ValueError:
                            pass
