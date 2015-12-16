#!/usr/bin/python
from watchdog.events import FileSystemEventHandler

import fix_logs


class WatchmanHandler(FileSystemEventHandler):
    def __init__(self):
        self.files_to_watch = []
        self.target = str()

    def on_modified(self, event):
        modified_file = event.src_path
        if not self._is_relevant(modified_file):
            # Do verify if this is keeping stray file descriptors open.
            return

        print "Modified: {0}".format(modified_file)
        self.handle_modification_event(modified_file, self.target)

    def on_created(self, event):
        pass
        # print 'Created: {0}'.format(event.src_path)

    def watch(self, file):
        self.files_to_watch.append(file)

    def write(self, target):
        self.target = target

    def _is_relevant(self, file):
        return file in self.files_to_watch

    def handle_modification_event(self, src, target):
        print 'Modification in src: {0}. Destination: {1}. Updating.'.format(src, target)
        try:
            fixxer = fix_logs.Fixxer(src, target)
            fixxer.file_modified()
        except Exception as e:
            print 'Exception : {0}'.format(e)
