import requests
import json
from config import LLM_SERVICE_URL
from db_handler import update_email_request
from logger import logger

def process_email_with_llm(email_request):
    """ Sends email content to the LLM service and updates Firestore with the result. """
    try:
        # Prepare the request payload
        payload = {
            "email_id": email_request["email_id"],
            "subject": email_request["subject"],
            "email_content": email_request["email_content"],
            "operation_performed": email_request["operation_performed"]
        }

        logger.info(f"Sending email for LLM classification: {payload}")

        # Send request to LLM service
        response = requests.post(LLM_SERVICE_URL, json=payload, timeout=30)

        if response.status_code == 200:
            llm_result = response.json()
            logger.info(f"LLM Response: {llm_result}")

            # Update Firestore with LLM response
            update_email_request(email_request["request_id"], status="completed", llm_response=llm_result)
        else:
            logger.error(f"LLM service failed: {response.status_code}, {response.text}")
            update_email_request(email_request["request_id"], status="failed", llm_response={"error": response.text})

    except Exception as e:
        logger.error(f"Error processing email with LLM: {e}")
        update_email_request(email_request["request_id"], status="failed", llm_response={"error": str(e)})
