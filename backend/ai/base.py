from abc import ABC, abstractmethod
from typing import Dict, Any


class AIService(ABC):

    @abstractmethod
    def simplify(
        self,
        original_question: str,
        verified_answer: Dict[str, Any],
        language: str = "en"
    ) -> str:
        pass

    @abstractmethod
    def analyze_document(
        self,
        document_text: str,
        language: str = "en"
    ) -> Dict[str, Any]:
        pass