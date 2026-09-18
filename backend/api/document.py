from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from services.pdf import extract_text_from_pdf
from services.document_analysis import analyze_document


router = APIRouter()


@router.post("/analyze-document")
async def analyze_document_endpoint(
    file: UploadFile = File(...),
    model: str = Form("gemini-3.6-flash"),
    language: str = Form("en")
):
    # 1. Make sure the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    # 2. Read the uploaded PDF
    file_bytes = await file.read()

    # 3. Extract text
    text = extract_text_from_pdf(file_bytes)

    # 4. Make sure text was extracted
    if not text:
        raise HTTPException(
            status_code=400,
            detail="The PDF does not contain extractable text."
        )

    # 5. Analyze the document
    try:
        result = analyze_document(
            document_text=text,
            model=model,
            language=language
        )

        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Document analysis failed."
        )