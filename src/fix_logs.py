#!/usr/bin/env python
# -*- coding: utf-8 -*-
import reverie, json, os, logging

MODE_READ = 'r'
MODE_READ_AND_WRITE = 'r+'
MODE_APPEND = 'a'
FLUSH_IMMEDIATELY = 0
NEWLINE = '\n'
POS_FILE = '/tmp/.watchman.pos'
POS_FILE_DELIMITER = '|'
class Fixxer():
    def __init__(self, src, target):
        self.file_to_read_from = src
        self.file_to_write_to  = target
        self.parser = reverie.ReverieParser()

    def fetch_read_write(self):
        # __magic__ally know where we left. Right now beginning from zero.
        # Make this persistent. in the future.
        pos = self.get_last_position(self.file_to_read_from)
        logging.info('POS VALUE: ' + str(pos))

        reader = open(self.file_to_read_from, MODE_READ)
        # line wise counter or character wise(?) Assuming line wise for now.
        reader.seek(pos)

        # Gather and push across as many lines as possible-
        for line in reader:
            # self.parser.reverie_sleep()
            # formatted_log = self.parser.test_format(line)
            formatted_log = self.parser.reformat_log(line)
            self.write_new_lines_to_target(formatted_log, self.file_to_write_to)

        # Write last position into pos file
        logging.info('Writing bytes read to pos_file')
        self.set_latest_position(reader.tell(), self.file_to_read_from)

    def write_new_lines_to_target(self, log, target):
        writer = open(target, MODE_APPEND, FLUSH_IMMEDIATELY)
        writer.write(log + NEWLINE)

    def file_modified(self):
        self.fetch_read_write()

    def get_last_position(self, src):
        pos_file_position = 0
        try:

            # create a empty dict
            pos_dict = {}

            # parse the pos_file & then populate the dict
            with open(POS_FILE, MODE_READ) as pos_file:
                for line in pos_file:
                    tokens = line.split(POS_FILE_DELIMITER)
                    if len(tokens) == 2:
                        pos_dict[tokens[0]] = int(tokens[1].rstrip('\n'))

            if src in pos_dict.keys():
                # Open the src file, get its total byte count
                with open(src, MODE_READ) as src_file:
                    # Move file pointer to the end
                    src_file.seek(0, 2)
                    # See if file is smaller than its last noted size, if yes return 0 for position
                    if pos_dict[src] >= src_file.tell():
                        pos_file_position = 0
                    else:
                        pos_file_position = pos_dict[src]
            else:
                # pos file doesnt have the files entry, its probably a new file
                pass
        except IOError as ioe:
            if ioe.errno == 2:
                # POS_FILE doesnt exist, creating it.
                newly_created_pos_file = open(POS_FILE, 'a')
                os.fsync(newly_created_pos_file.fileno())
                newly_created_pos_file.close()
            else:
                logging.exception('Exception :')
                #traceback.print_exc(file=sys.stdout)

        except Exception as e:
            logging.exception('Exception :')
            #traceback.print_exc(file=sys.stdout)

        # Return back the srcs last position only if it is found in the pos file, otherwise return 0
        return pos_file_position

    def set_latest_position(self, pos, src):
        try:

            # Create a empty dict
            pos_dict = {}

            # Parse the pos_file & then populate the dict
            with open(POS_FILE, MODE_READ_AND_WRITE, FLUSH_IMMEDIATELY) as pos_file:
                for line in pos_file:
                    tokens = line.split(POS_FILE_DELIMITER)
                    if len(tokens) == 2:
                        pos_dict[tokens[0]] = int(tokens[1].rstrip('\n'))

                # Update latest position of src
                pos_dict[src] = pos

                # Write data back to pos file
                pos_file.seek(0)
                pos_file.truncate()
                for key in pos_dict:
                    pos_file.write(key + POS_FILE_DELIMITER + str(pos_dict[key]) + NEWLINE)

                # Flush all the buffers
                pos_file.flush()
                os.fsync(pos_file.fileno())

        except Exception as e:
            logging.exception('Exception :')
            #traceback.print_exc(file=sys.stdout)

