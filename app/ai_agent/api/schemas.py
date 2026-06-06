# app/ai_agent/api/schemas.py
# Pydantic schemas for request and response validation
from pydantic import BaseModel
from typing import Optional

class GenerateRequest(BaseModel):
    user_input: str
    mode: Optional[str] = None
    project_id: str = "freightship"
    session_id: Optional[str] = None
    document_id: Optional[str] = None
    model_name: Optional[str] = None
