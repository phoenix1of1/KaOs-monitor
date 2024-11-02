import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name, log_file, level=logging.DEBUG):
    """Function to setup a logger with a timed rotating file handler."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove all handlers associated with the logger
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Remove all handlers associated with the root logger object
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create a file handler that logs debug and higher level messages
    file_handler = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Prevent propagation to the root logger
    logger.propagate = False

    return logger

# Example usage:
# logger = setup_logger('my_logger', 'my_log_file.txt')
# logger.debug('This is a debug message')
# logger.info('This is an info message')