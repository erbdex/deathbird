import libwatchman
import sys


def initiate_watchdog():
    file_to_read_from = sys.argv[1]
    file_to_write_to  = sys.argv[2]
    libwatchman.watch_logs(files_to_watch=[file_to_read_from], target=file_to_write_to)


if __name__ == '__main__':
    initiate_watchdog()
