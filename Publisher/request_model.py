from pydantic import BaseModel, Field
from typing import Literal

class EmailRequestModel(BaseModel):
    client_id: str = Field(..., title="Client ID")
    request_id: str = Field(..., title="Request ID")
    email_id: str = Field(..., title="Email ID")
    subject: str = Field(..., title="Subject")
    email_content: str = Field(..., title="Email Content")
    operation_performed: Literal["classify", "extract"] = Field(..., title="Operation Performed")
    callback_url: str = Field(..., title="Callback URL")
