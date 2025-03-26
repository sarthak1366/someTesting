import logging
from google.cloud import logging as cloud_logging

# Initialize Cloud Logging
client = cloud_logging.Client()
client.setup_logging()

# Configure logger
logger = logging.getLogger("email-classification")
logger.setLevel(logging.INFO)

# Define log format
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
