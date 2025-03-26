from google.cloud import firestore
from db_model import FirestoreEmailRequestModel
from logger import logger
from config import FIRESTORE_COLLECTION

db = firestore.Client(database="email-classification-db")

def save_email_request(email_request: FirestoreEmailRequestModel):
    """ Save the email request to Firestore """
    try:
        doc_ref = db.collection(FIRESTORE_COLLECTION).document(email_request.request_id)
        doc_ref.set(email_request.dict())
        logger.info(f"Email request {email_request.request_id} stored in Firestore.")
    except Exception as e:
        logger.error(f"Error saving to Firestore: {e}")

def get_email_request(request_id: str):
    """ Retrieve an email request from Firestore using request_id """
    try:
        doc_ref = db.collection(FIRESTORE_COLLECTION).document(request_id)
        doc = doc_ref.get()
        if doc.exists:
            logger.info(f"Retrieved email request: {request_id}")
            return doc.to_dict()
        else:
            logger.warning(f"Email request {request_id} not found.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving email request: {e}")
        return None

def update_email_status(request_id: str, status: str, llm_response=None):
    """ Update email request status in Firestore """
    try:
        doc_ref = db.collection(FIRESTORE_COLLECTION).document(request_id)
        update_data = {"status": status, "updated_at": firestore.SERVER_TIMESTAMP}
        if llm_response:
            update_data["llm_response"] = llm_response
        doc_ref.update(update_data)
        logger.info(f"Email request {request_id} updated in Firestore: {status}.")
    except Exception as e:
        logger.error(f"Error updating Firestore for {request_id}: {e}")
