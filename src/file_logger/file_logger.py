import logging

logger = logging.getLogger('file_log')
logger.setLevel(logging.DEBUG)
fh_log = logging.FileHandler("output.log")
fh_log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d\r\n\t%(message)s', datefmt='%d-%b-%y %H:%M:%S')
fh_log.setFormatter(formatter)

logger.addHandler(fh_log)