#!/usr/bin/env python
# -*- coding: utf-8 -*-
import reverie

MODE_READ = 'r'
MODE_APPEND = 'a'
FLUSH_IMMEDIATELY = 0
NEWLINE = '\n'

class Fixxer():
    def __init__(self, src, target):
        self.file_to_read_from = src
        self.file_to_write_to  = target
        self.parser = reverie.ReverieParser()

    def fetch_read_write(self):
        # __magic__ally know where we left. Right now beginning from zero.
        # Make this persistent. in the future.
        pos = self.get_last_position(self.file_to_read_from)

        reader = open(self.file_to_read_from, MODE_READ)
        # line wise counter or character wise(?) Assuming line wise for now.
        reader.seek(pos)

        # Gather and push across as many lines as possible-
        for line in reader:
            self.parser.reverie_sleep()
            # formatted_log = self.parser.test_format(line)
            formatted_log = self.parser.reformat_log(line)
            self.write_new_lines_to_target(formatted_log, self.file_to_write_to)

    def write_new_lines_to_target(self, log, target):
        writer = open(target, MODE_APPEND, FLUSH_IMMEDIATELY)
        writer.write(log + NEWLINE)

    def file_modified(self):
        self.fetch_read_write()

    def get_last_position(self, src):
        return 0
        pass

    def set_latest_position(self, pos, src):
        pass