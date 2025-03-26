import os

# Firestore configuration
GCP_PROJECT_ID = "scam-botpoc"
FIRESTORE_COLLECTION = "email-requests"

# Pub/Sub configuration
PUBSUB_TOPIC = "email-bot-request"
PUBSUB_SUBSCRIPTION = "email-bot-request-sub"

# Cloud Tasks configuration
QUEUE_NAME = "LLM-request-queue"
QUEUE_LOCATION = "asia-south1"
TASKS_URL = "http://0.0.0.0:8001/process-llm"

# LLM API Configuration
LLM_ENDPOINT = "http://0.0.0.0:8001/process-llm"

# Logging Configuration
LOG_LEVEL = "INFO"
