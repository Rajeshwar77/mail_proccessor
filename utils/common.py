import logging
import re
# Configure logging
logging.basicConfig(level=logging.ERROR, filename='error.log')
logging.basicConfig(level=logging.INFO, filename='info.log')

def log_error(message, exception):
    logging.error(f"{message}: {exception}")

def log_debug(message):
    logging.debug(message)

def log_info(message):
    logging.info(message)

def extract_email(s):
    pattern = r'<([^>]+)>'
    match = re.search(pattern, s)
    if match:
        return match.group(1)  # Returns the matched group inside the brackets
    return s  # Return the original string if no match is found