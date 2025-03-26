import json
from google.cloud import tasks_v2
from config import GCP_PROJECT_ID, QUEUE_NAME, QUEUE_LOCATION, TASKS_URL
from db_handler import get_email_request
from logger import logger

# Initialize Cloud Tasks client
client = tasks_v2.CloudTasksClient()
parent = client.queue_path(GCP_PROJECT_ID, QUEUE_LOCATION, QUEUE_NAME)

def enqueue_task(request_id):
    """ Adds an email classification task to Cloud Tasks without scheduling. """
    try:
        # Fetch the full email request from Firestore
        email_request_data = get_email_request(request_id)
        email_content = email_request_data.get("email_content")
        if not email_content:
            logger.error(f"No email request found for request_id: {request_id}")
            return

        # Prepare HTTP request payload
        payload = json.dumps(email_request).encode()

        # Configure Cloud Task request
        task = {
            "http_request": {  
                "http_method": tasks_v2.HttpMethod.POST,
                "url": TASKS_URL,  # The LLM processing endpoint
                "headers": {"Content-Type": "application/json"},
                "body": payload,
            }
        }

        # Create the task in Cloud Tasks (immediately executed)
        response = client.create_task(request={"parent": parent, "task": task})
        logger.info(f"Task {response.name} created for request_id: {request_id}")

    except Exception as e:
        logger.error(f"Failed to enqueue task for {request_id}: {e}")
