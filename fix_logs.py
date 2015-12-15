#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, reverie


class Fixxer():
    def __init__(self):
        self.file_to_read_from = sys.argv[1]
        self.file_to_write_to  = sys.argv[2]
        self.parser = reverie.ReverieParser()

    def fetch_read_write(self, src, target):
        # __magic__ally know where we left. Right now beginning from zero.
        # Make this persistent. in the future.
        know_where_we_left = 0
        reader = open(src, 'r')
        # line wise counter or character wise(?) Assuming line wise for now.
        reader.seek(know_where_we_left)

        # Gather and push across as many lines as possible-
        for line in reader:
            self.parser.reverie_sleep()
            formatted_log = self.parser.reformat_log(line)
            self.write_new_lines_to_target(formatted_log, target)

    def write_new_lines_to_target(self, log, target):
        writer = open(target, 'a', 0)
        writer.write(log + '\n')

    def file_modified(self, src, target):
        self.fetch_read_write(src, target)

    def initiate_watchdog(self):
        # Triggers call_handler_file_edited in case the file undergoes mods.
        self.file_modified(self.file_to_read_from, self.file_to_write_to)


if __name__ == '__main__':
    fixxer = Fixxer()
    fixxer.initiate_watchdog()
