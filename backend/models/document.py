from pydantic import BaseModel
from typing import List


class DocumentAnalysisResponse(BaseModel):
    document_type: str
    title: str
    summary: str

    important_information: List[str]
    eligibility: List[str]
    deadlines: List[str]
    required_documents: List[str]
    steps: List[str]

    warnings: List[str] = []