import libwatchman
import sys
import logging


def initiate_watchdog():
    import log
    log.configure_generic_logging(False, 'log/deathbird.log', log_level=logging.INFO)
    file_to_read_from = sys.argv[1]
    file_to_write_to  = sys.argv[2]
    libwatchman.watch_logs(files_to_watch=[file_to_read_from], target=file_to_write_to)


if __name__ == '__main__':
    initiate_watchdog()
