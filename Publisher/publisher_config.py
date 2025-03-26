from google.cloud import pubsub_v1
import json
from logger_config import logger  

PROJECT_ID = "scam-botpoc"
TOPIC_ID = "email-bot-request"

class Publisher:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(PROJECT_ID, TOPIC_ID)
        logger.info("Publisher initialized.")

    def publish_message(self, message: dict):
        """Publishes a message to the Pub/Sub topic after converting it to JSON."""
        message_json = json.dumps(message).encode("utf-8")
        logger.info(f"Publishing message: {message}")

        try:
            future = self.publisher.publish(self.topic_path, message_json)
            logger.info(f"Message published successfully: {future.result()}")
            return future.result()
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
            raise
