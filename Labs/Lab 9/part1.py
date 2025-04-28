import logging

# Create logger for file logging
logger = logging.getLogger("file_logger")
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler("example_log.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Add handler to the logger
logger.addHandler(file_handler)

loggers = {
    "sqldb": logging.getLogger("sqldb"),
    "ui": logging.getLogger("ui"),
    "frontend.js": logging.getLogger("frontend.js"),
    "backend.js": logging.getLogger("backend.js"),
    "frontend.flask": logging.getLogger("frontend.flask"),
    "backend.flask": logging.getLogger("backend.flask"),
}

for log in loggers.values():
    log.addHandler(file_handler)
    log.setLevel(logging.INFO) 

def log_messages():
    loggers["sqldb"].info("user logged in with correct password")
    loggers["sqldb"].error("file not found")
    loggers["ui"].warning("disk space low")
    loggers["frontend.js"].critical("there is no more disk space")
    loggers["backend.flask"].error("file not found")

if __name__ == "__main__":
    log_messages()