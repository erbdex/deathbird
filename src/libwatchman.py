from watchdog.observers import Observer

import os
import time
import watchman


def parent_directory(file_path):
    directory = os.path.dirname(file_path)
    return directory if directory else '.'

def watch_logs(files_to_watch, target):
    file = files_to_watch[0]
    directory_to_watch = parent_directory(file)

    handler = watchman.WatchmanHandler()
    observer = Observer()
    handler.watch(file)
    handler.write(target)

    observer.schedule(handler, path=directory_to_watch, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
