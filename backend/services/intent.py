def detect_intent(message: str) -> str:
    text = message.lower().strip()

    # -------------------------
    # Land / Revenue
    # -------------------------

    # Land conversion / NALA
    nala_keywords = [
        "nala",
        "land conversion",
        "convert agricultural land",
        "agricultural land conversion",
        "non agricultural use",
        "non-agricultural use",
        "convert my agricultural land",
        "change land use",
        "change the use of land",
        "convert land for non agricultural use",
        "నాలా",
        "భూమి మార్పిడి",
        "భూమిని మార్చాలి",
        "భూమి ఉపయోగం మార్చాలి",
        "భూమిని వేరే ఉపయోగానికి మార్చాలి",
        "వ్యవసాయ భూమి మార్పిడి",
        "వ్యవసాయ భూమిని మార్చాలి",
        "వ్యవసాయ భూమి నుండి వేరే ఉపయోగానికి",
        "వ్యవసాయ భూమిని వేరే ఉపయోగానికి మార్చాలి",
        "వ్యవసాయేతర ఉపయోగం",
        "వ్యవసాయేతర వినియోగం"
    ]

    # Mutation / Succession
    mutation_keywords = [
        "mutation",
        "land mutation",
        "transfer land",
        "transfer property",
        "inherit land",
        "inheritance",
        "succession",
        "father died",
        "mother died",
        "parent died",
        "parents died",
        "వారసత్వం",
        "మ్యుటేషన్",
        "వారసత్వ భూమి",
        "తండ్రి చనిపోయారు",
        "తండ్రి మరణించారు",
        "తల్లి చనిపోయారు",
        "తల్లి మరణించారు",
        "వారసుల పేర్లకు",
        "వారసుల పేర్లలో",
        "వారసుల పేర్లకు",
        "భూమి వారసత్వం",
    ]

    # Land record correction
    land_correction_keywords = [
        "wrong name",
        "incorrect name",
        "name correction",
        "wrong details",
        "incorrect details",
        "land record correction",
        "record correction",
        "name is wrong",
        "name is incorrect",
        "పేరు తప్పుగా ఉంది",
        "పేరు సరిచేయాలి",
        "పేరు తప్పు",
        "భూమి రికార్డులో పేరు తప్పుగా ఉంది",
        "భూమి రికార్డులో తప్పు",
        "భూమి రికార్డు సరిచేయాలి",
    ]

    # Record of Rights / Land records
    ror_keywords = [
        "record of rights",
        "ror",
        "land record",
        "land records",
        "pattadar passbook",
        "land details",
        "పట్టాదారు",
        "పట్టాదారు పాస్‌బుక్",
        "భూమి రికార్డు",
        "భూమి రికార్డులు",
        "భూ రికార్డు",
    ]

    # -------------------------
    # IMPORTANT:
    # Check specific land problems FIRST
    # -------------------------

    if any(keyword in text for keyword in nala_keywords):
        return "land_conversion"

    if any(keyword in text for keyword in mutation_keywords):
        return "mutation_succession"

    if any(keyword in text for keyword in land_correction_keywords):
        return "land_record_correction"

    if any(keyword in text for keyword in ror_keywords):
        return "record_of_rights"

    # -------------------------
    # Certificates
    # -------------------------

    income_keywords = [
        "income certificate",
        "income proof",
        "income",
        "ఆదాయ ధృవీకరణ",
        "ఆదాయ ధృవీకరణ పత్రం",
        "ఆదాయ సర్టిఫికేట్",
    ]

    caste_keywords = [
        "caste certificate",
        "caste proof",
        "caste",
        "కుల ధృవీకరణ పత్రం",
        "కుల ధృవీకరణ",
        "కుల సర్టిఫికేట్",
    ]

    residence_keywords = [
        "residence certificate",
        "domicile certificate",
        "residence proof",
        "residential certificate",
        "నివాస ధృవీకరణ పత్రం",
        "నివాస ధృవీకరణ",
        "నివాస సర్టిఫికేట్",
    ]

    birth_death_keywords = [
        "birth certificate",
        "death certificate",
        "birth registration",
        "death registration",
        "జనన ధృవీకరణ",
        "మరణ ధృవీకరణ",
        "జనన సర్టిఫికేట్",
        "మరణ సర్టిఫికేట్",
    ]

    if any(keyword in text for keyword in income_keywords):
        return "income_certificate"

    if any(keyword in text for keyword in caste_keywords):
        return "caste_certificate"

    if any(keyword in text for keyword in residence_keywords):
        return "residence_certificate"

    if any(keyword in text for keyword in birth_death_keywords):
        return "birth_death_certificate"

    # -------------------------
    # Schemes
    # -------------------------

    gruha_jyothi_keywords = [
        "gruha jyothi",
        "free electricity",
        "200 units",
        "electricity subsidy",
        "గృహ జ్యోతి",
        "ఉచిత విద్యుత్",
    ]

    aasara_keywords = [
        "aasara",
        "aasara pension",
        "old age pension",
        "widow pension",
        "disability pension",
        "ఆసరా",
        "ఆసరా పెన్షన్",
        "వృద్ధాప్య పెన్షన్",
        "వితంతు పెన్షన్",
        "వికలాంగుల",
        "పెన్షన్‌",
        "వికలాంగులు",
        "వికలాంగుల పెన్షన్‌"
    ]

    kalyana_keywords = [
        "kalyana lakshmi",
        "shaadi mubarak",
        "marriage assistance",
        "marriage scheme",
        "కళ్యాణ లక్ష్మి",
        "షాదీ ముబారక్",
        "పెళ్లి సహాయం",
    ]
    mahalakshmi_keywords = [
    "maha lakshmi",
    "mahalakshmi",
    "maha lakshmi scheme",
    "mahalakshmi scheme",
    "free bus",
    "free bus travel",
    "free rtc bus",
    "500 gas cylinder",
    "500 rupees gas cylinder",
    "lpg subsidy",
    "women scheme",
    "మహాలక్ష్మి",
    "మహా లక్ష్మి",
    "మహాలక్ష్మి పథకం",
    "ఉచిత బస్సు",
    "ఉచిత బస్ ప్రయాణం",
    "500 రూపాయల గ్యాస్",
    "గ్యాస్ సిలిండర్",
]

    if any(keyword in text for keyword in gruha_jyothi_keywords):
        return "gruha_jyothi"

    if any(keyword in text for keyword in aasara_keywords):
        return "aasara_pension"

    if any(keyword in text for keyword in kalyana_keywords):
        return "kalyana_lakshmi"
    if any(keyword in text for keyword in mahalakshmi_keywords):
        return "mahalakshmi"
    

    # -------------------------
    # Broad categories
    # -------------------------

    if any(
        keyword in text
        for keyword in [
            "land",
            "property",
            "revenue",
            "bhumi",
            "భూమి",
            "పట్టా",
        ]
    ):
        return "land_revenue"

    if any(
        keyword in text
        for keyword in [
            "certificate",
            "సర్టిఫికేట్",
        ]
    ):
        return "certificate"

    if any(
        keyword in text
        for keyword in [
            "scheme",
            "pension",
            "పథకం",
            "పెన్షన్",
        ]
    ):
        return "government_scheme"

    return "unknown"