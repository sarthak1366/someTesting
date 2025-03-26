import json
import threading
from fastapi import FastAPI
from google.cloud import pubsub_v1
from db_model import FirestoreEmailRequestModel
from db_handler import save_email_request
from task_queue import enqueue_task
from logger import logger
from config import PUBSUB_SUBSCRIPTION,GCP_PROJECT_ID

# Initialize FastAPI app
app = FastAPI()

# Initialize Pub/Sub Subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(GCP_PROJECT_ID, PUBSUB_SUBSCRIPTION)

def callback(message):
    """ Process incoming Pub/Sub message """
    try:
        message_data = json.loads(message.data.decode("utf-8"))
        email_request = FirestoreEmailRequestModel(**message_data)
        save_email_request(email_request)
        logger.info(f"Pushed to Firestore: {email_request.request_id}")
        enqueue_task(email_request.request_id)
        message.ack()
        logger.info(f"Processed message: {email_request.request_id}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        message.nack()

def start_subscriber():
    """ Start listening to Pub/Sub topic in a background thread """
    future = subscriber.subscribe(subscription_path, callback=callback)
    logger.info("Subscriber listening...")
    try:
        future.result()
    except Exception as e:
        logger.error(f"Subscriber error: {e}")

# Start Pub/Sub listener in a separate thread
threading.Thread(target=start_subscriber, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
