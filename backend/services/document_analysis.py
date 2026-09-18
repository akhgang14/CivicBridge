from typing import Dict, Any

from ai.factory import get_ai_service


def analyze_document(
    document_text: str,
    model: str,
    language: str = "en"
) -> Dict[str, Any]:

    ai_service = get_ai_service(model)

    return ai_service.analyze_document(
        document_text=document_text,
        language=language
    )