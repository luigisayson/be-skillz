import time
from functools import wraps
import logging

# create logger
logger = logging.getLogger('RedditNounTranslator')
logger.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create file handler which logs even debug messages
fh = logging.FileHandler('debug.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)


def log_elapsed_time(fun):
    @wraps(fun)
    def function_wrapper(*args, **kwargs):
        start = time.time()
        result = fun(*args, **kwargs)
        end = time.time()
        duration = end - start
        logger.info(f'{fun.__name__} finished in {duration} seconds')
        if result:
            logger.debug(f'{fun.__name__} output: {result}')
        return result
    return function_wrapper
