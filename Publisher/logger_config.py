import logging
from google.cloud import logging as cloud_logging

# Initialize Cloud Logging
client = cloud_logging.Client()
client.setup_logging()

# Configure logger
logger = logging.getLogger("email-classification")
logger.setLevel(logging.INFO)

# Define log format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Stream handler (console output)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Suppress specific unwanted logs
unwanted_loggers = [
    "notebooks_collection_agent",
    "service_generator_agent",
    "idle_shutdown_agent",
    "docker",
]

for unwanted in unwanted_loggers:
    logging.getLogger(unwanted).setLevel(logging.WARNING)  # Only show warnings/errors

# Example logs
logger.info("This is an important INFO log.")   # Will be shown
logger.error("This is an ERROR log.")           # Will be shown
