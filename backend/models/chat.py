from pydantic import BaseModel
from typing import List, Optional


class ChatRequest(BaseModel):
    message: str
    language: str = "en"


class CivicResponse(BaseModel):
    intent: str
    language: str
    title: str
    summary: str
    eligibility: Optional[str] = None
    steps: List[str]
    documents: List[str]
    department: Optional[str] = None
    application_channel: Optional[str] = None
    source_title: Optional[str] = None
    source_url: Optional[str] = None
    last_verified: Optional[str] = None


class SimplifyRequest(BaseModel):
    message: str
    language: str = "en"
    model: str = "gemini-3.5-flash-lite"


class SimplifyResponse(BaseModel):
    explanation: str
    model: str

    
class CivicUnderstanding(BaseModel):
    domain: str
    service: str
    issue: str
    entities: dict


# class DocumentAnalysisRequest(BaseModel):
#     language: str = "en"
#     model: str = "gemini-3.6-flash"


# class DocumentAnalysisResponse(BaseModel):
#     document_type: str
#     title: str
#     summary: str

#     important_dates: list[str] = []
#     eligibility: list[str] = []
#     required_documents: list[str] = []
#     required_actions: list[str] = []
#     warnings: list[str] = []

#     language: str = "en"
#     model: str = ""

#     extracted_text_preview: str = ""