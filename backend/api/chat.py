from fastapi import APIRouter, HTTPException
from models.chat import (
    ChatRequest,
    CivicResponse,
    SimplifyRequest,
    SimplifyResponse,
)

from services.intent import detect_intent
from services.knowledge import find_service
from ai.factory import get_ai_service

router = APIRouter()


@router.post("/chat", response_model=CivicResponse)
def chat(request: ChatRequest):

    # 1. Determine what the user is asking about
    intent = detect_intent(request.message)

    # 2. Find the authoritative CivicBridge service
    service = find_service(request.message, intent,request.language)

    # 3. If CivicBridge found a verified service,
    #    use Gemini ONLY to explain it.
    if service:
        return CivicResponse(
            intent=intent,
            language=request.language,
            title=service["title"],
            summary=service["summary"],
            eligibility=service.get("eligibility"),
            steps=service["steps"],
            documents=service["documents"],
            department=service.get("department"),
            application_channel=service.get("application_channel"),
            source_title=service.get("source_title"),
            source_url=service.get("source_url"),
            last_verified=service.get("last_verified")
        )

    if intent == "land_revenue":
        return CivicResponse(
            intent=intent,
            language=request.language,
            title="Land & Revenue Assistance",
            summary="We identified your question as a land or revenue-related issue.",
            steps=[
                "Tell us what specific land-related problem you are facing.",
                "We will identify the relevant government process.",
                "We will show the documents and next steps."
            ],
            documents=[],
            department="Revenue Department",
            source=None
        )

    if intent == "certificate":
        return CivicResponse(
            intent=intent,
            language=request.language,
            title="Certificate Assistance",
            summary="We identified your question as a certificate-related request.",
            steps=[
                "Tell us which certificate you need.",
                "We will explain the eligibility and application process.",
                "We will provide the required documents."
            ],
            documents=[],
            department="Revenue Department",
            source=None
        )

    if intent == "government_scheme":
        return CivicResponse(
            intent=intent,
            language=request.language,
            title="Government Scheme Assistance",
            summary="We identified your question as a government-scheme related request.",
            steps=[
                "Tell us which scheme you are asking about.",
                "We will explain who may be eligible.",
                "We will show the application process and required documents."
            ],
            documents=[],
            department=None,
            source=None
        )

    if intent == "document_explanation":
        return CivicResponse(
            intent=intent,
            language=request.language,
            title="Document Explanation",
            summary="We can help explain a government or legal document in simpler language.",
            steps=[
                "Upload the document.",
                "We will identify the important information.",
                "We will explain what action may be required."
            ],
            documents=[],
            department=None,
            source=None
        )

    # 5. Completely unknown request
    return CivicResponse(
        intent="unknown",
        language=request.language,
        title="Let's understand your problem",
        summary="I need a little more information to identify the right government service.",
        steps=[
            "Describe what you are trying to do.",
            "Tell us which state the issue relates to."
        ],
        documents=[],
        department=None,
        source=None
    )
@router.post(
    "/chat/simplify",
    response_model=SimplifyResponse
)
def simplify_chat(request: SimplifyRequest):

    intent = detect_intent(request.message)

    service = find_service(
        request.message,
        intent,
        request.language
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="No verified CivicBridge information was found for this question."
        )

    # Validate and create the AI service
    try:
        ai = get_ai_service(request.model)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    # Call Gemini
    try:
        explanation = ai.simplify(
            original_question=request.message,
            verified_answer=service,
            language=request.language
        )

        return SimplifyResponse(
            explanation=explanation,
            model=request.model
        )

    except Exception as error:

        print(f"Gemini simplification error: {error}")

        raise HTTPException(
            status_code=503,
            detail="AI simplification is temporarily unavailable. Please try again."
        )
