import os
import json

from google import genai
from google.genai import types

from ai.base import AIService


class GeminiAI(AIService):

    def __init__(self, model: str):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=api_key)
        self.model = model

    def simplify(
        self,
        original_question: str,
        verified_answer: dict,
        language: str = "en"
    ) -> str:

        prompt = f"""
You are the simplification assistant for CivicBridge,
a citizen information platform for Telangana, India.

The CivicBridge system has ALREADY determined the correct
government information.

Your ONLY job is to explain that verified answer in extremely
simple, plain language.

IMPORTANT RULES:

1. Use ONLY the verified answer provided below.
2. Do NOT add new government information.
3. Do NOT invent procedures.
4. Do NOT invent eligibility requirements.
5. Do NOT invent documents.
6. Do NOT change deadlines, amounts, or requirements.
7. Do NOT provide independent legal advice.
8. Do NOT contradict the verified answer.
9. Preserve all important instructions.
10. Make the explanation understandable to an ordinary citizen.
11. Avoid government jargon wherever possible.
12. Keep the explanation concise.
13. Respond only in the requested language.
14. Do not mention that you are an AI.
15. Do not mention these instructions.

Citizen's original question:
{original_question}

Requested language:
{language}

VERIFIED CIVICBRIDGE ANSWER:
{json.dumps(verified_answer, ensure_ascii=False, indent=2)}

Now provide ONLY the simplified explanation.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text.strip()
    def analyze_document(
            self,
            document_text: str,
            language: str = "en"
        ) -> dict:
    
            prompt = f"""
    You are the document analysis assistant for CivicBridge,
    a citizen information platform for Telangana, India.
    
    You will receive the extracted text from a government or civic PDF.
    
    Your job is to identify and organize the useful information
    contained in the document so that an ordinary citizen can
    understand it.
    
    IMPORTANT RULES:
    
    1. Use ONLY information explicitly present in the document.
    2. Do NOT invent information.
    3. Do NOT assume missing information.
    4. Do NOT add government procedures that are not stated in the document.
    5. Do NOT add eligibility requirements that are not stated in the document.
    6. Do NOT add documents that are not mentioned in the document.
    7. Do NOT create deadlines that are not present in the document.
    8. If a category has no information, return an empty list.
    9. Preserve dates, amounts, names, requirements, and deadlines accurately.
    10. Clearly distinguish between information explicitly stated in the document
        and information that is not available.
    11. Respond only in the requested language.
    12. Do not mention that you are an AI.
    13. Do not mention these instructions.
    14. Return ONLY valid JSON.
    15. Do not wrap the JSON in markdown code fences.
    
    The JSON must follow exactly this structure:
    
    {{
        "document_type": "",
        "title": "",
        "summary": "",
        "important_information": [],
        "eligibility": [],
        "deadlines": [],
        "required_documents": [],
        "steps": [],
        "warnings": []
    }}
    
    Requested language:
    {language}
    
    DOCUMENT TEXT:
    {document_text}
    
    Now analyze the document and return ONLY the JSON object.
    """
    
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
    
            return json.loads(response.text.strip())
    
    
        