__author__ = 'root'
import logging
from logutils.colorize import ColorizingStreamHandler

def configure_generic_logging(console=True, logfile='log/deathbird.log', log_level=logging.INFO):
    logging.basicConfig(level=log_level,
                        format='%(filename)s %(lineno)d %(asctime)s %(message)s',
                        filename=logfile,
                        filemode='w')

    if console:
        # console = logging.StreamHandler
        console = ColorizingStreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
