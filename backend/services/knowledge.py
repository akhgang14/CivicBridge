import json
from pathlib import Path


KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "services.json"
)


def load_services():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


    
def get_localized_service(service, language):
    if language == "te":
        translation = service.get("translations", {}).get("te")

        if translation:
            localized_service = service.copy()
            localized_service.update(translation)
            return localized_service

    return service


def find_service(message: str, intent: str,language: str = "en"):
    services = load_services()
    text = message.lower()

    intent_to_service = {
        "income_certificate": "C1",
        "caste_certificate": "C2",
        "residence_certificate": "C3",
        "birth_death_certificate": "C4",

        "record_of_rights": "L1",
        "mutation_succession": "L2",
        "land_record_correction": "L3",
        "land_conversion": "L4",

        "gruha_jyothi": "S1",
        "mahalakshmi": "S2",
        "aasara_pension": "S3",
        "kalyana_lakshmi": "S4",
    }

    # Exact service mapping
    service_id = intent_to_service.get(intent)

    if service_id:
        for service in services:
            if service["id"] == service_id:
                return get_localized_service(
                    service,
                    language 
                )
                                                        
                            
    # Fallback category-based retrieval
    best_match = None
    best_score = 0

    for service in services:
        score = 0

        if service["category"] == intent:
            score += 2

        for keyword in service.get("keywords", []):
            if keyword.lower() in text:
                score += 3

        if score > best_score:
            best_score = score
            best_match = service

    if best_match:
        return get_localized_service(
            best_match,
            language
        )
    return None
    