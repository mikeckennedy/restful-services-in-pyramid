import logbook
import sys


def global_init(logfile):
    if logfile:
        logbook.TimedRotatingFileHandler(
            logfile, level=logbook.INFO, date_format='%Y-%m-%d').push_application()
    else:
        logbook.StreamHandler(sys.stdout, level=logbook.TRACE).push_application()

