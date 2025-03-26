from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class FirestoreEmailRequestModel(BaseModel):
    client_id: str = Field(..., title="Client ID")
    request_id: str = Field(..., title="Request ID")
    email_id: str = Field(..., title="Email ID")
    subject: str = Field(..., title="Subject")
    email_content: str = Field(..., title="Email Content")
    operation_performed: str = Field(..., title="Operation Performed", pattern="^(classify|extract)$")
    callback_url: str = Field(..., title="Callback URL")
    status: ProcessingStatus = Field(default=ProcessingStatus.PENDING, title="Processing Status")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="Created At")
    updated_at: datetime = Field(default_factory=datetime.utcnow, title="Updated At")
    llm_response: Optional[dict] = Field(default=None, title="LLM Response")
