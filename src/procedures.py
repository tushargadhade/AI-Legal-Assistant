"""
Legal Procedures & Citizen Rights Guide Module
Provides structured, step-by-step actionable procedural workflows for Indian citizens under key Acts.
"""

PROCEDURES_DATABASE = {
    "rti_filing": {
        "id": "rti_filing",
        "title": "Filing a Right to Information (RTI) Application",
        "act": "Right to Information Act, 2005",
        "short_act": "RTI Act 2005",
        "category": "Transparency & Governance",
        "summary": "Step-by-step guide to request official government information, status of public works, or application updates.",
        "icon": "file-text",
        "key_sections": ["Section 6 (Requesting Information)", "Section 7 (Timeframe for Disposal)", "Section 19 (First & Second Appeals)"],
        "timeline": "30 days (48 hours if it concerns life or liberty)",
        "fee": "₹10 (Free for BPL cardholders)",
        "steps": [
            {
                "step": 1,
                "title": "Identify Public Authority & PIO",
                "description": "Determine which Department/Ministry holds the information. Locate the Public Information Officer (PIO) or Assistant PIO."
            },
            {
                "step": 2,
                "title": "Draft the RTI Question clearly",
                "description": "Write exact, specific questions (e.g., 'Provide certified copy of...', 'What is the daily progress on file X?'). Avoid asking for opinions or hypothetical scenarios."
            },
            {
                "step": 3,
                "title": "Pay the Fee & Submit Application",
                "description": "Submit online via rtionline.gov.in (for Central Ministries) or state RTI portals. For offline, attach a ₹10 Court Fee Stamp, Demand Draft, or Postal Order addressed to the Accounts Officer."
            },
            {
                "step": 4,
                "title": "Track & Await Response",
                "description": "The PIO must respond within 30 days. If information concerns life or liberty, response must be provided within 48 hours."
            },
            {
                "step": 5,
                "title": "File First Appeal (If Delayed or Rejected)",
                "description": "If no reply is received within 30 days or if rejected without valid reason, file First Appeal within 30 days to the First Appellate Authority (FAA)."
            }
        ],
        "important_note": "You do not need to give any reason for requesting information under Section 6(2) of the RTI Act."
    },
    "consumer_complaint": {
        "id": "consumer_complaint",
        "title": "Filing a Consumer Court Complaint",
        "act": "Consumer Protection Act, 2019",
        "short_act": "CPA 2019",
        "category": "Consumer Rights & Commerce",
        "summary": "Procedure to seek refund, compensation, or replacement for defective products or deficient services.",
        "icon": "shopping-bag",
        "key_sections": ["Section 2(7) (Consumer definition)", "Section 34/47/58 (Pecuniary Jurisdiction)", "Section 35 (Filing Complaint)"],
        "timeline": "Must file within 2 years from date of cause of action",
        "fee": "Nil for claims up to ₹5 Lakhs; nominal fees for higher amounts",
        "steps": [
            {
                "step": 1,
                "title": "Send Formal Legal Notice to Seller/Company",
                "description": "Send a written notice (via Registered Post or Email) describing the defect/deficiency, requesting resolution within 15 days."
            },
            {
                "step": 2,
                "title": "Determine Forum Jurisdiction",
                "description": "District Commission (Up to ₹50 Lakhs), State Commission (₹50 Lakhs to ₹2 Crores), National NCDRC (Above ₹2 Crores)."
            },
            {
                "step": 3,
                "title": "Draft Complaint with Supporting Proofs",
                "description": "Attach invoices, warranty card, communication history, photographs, expert reports, and proof of payment."
            },
            {
                "step": 4,
                "title": "File Online via e-Daakhil Portal",
                "description": "Register on edaakhil.nic.in, upload complaint document, pay prescribed fee online, and select relevant commission."
            },
            {
                "step": 5,
                "title": "Attend Hearing / Mediation",
                "description": "Under CPA 2019, parties can opt for Mediation Cell resolution. No advocate mandatory—consumers can plead their own case."
            }
        ],
        "important_note": "E-commerce purchases are fully covered under CPA 2019 rules including misleading ads and unfair trade practices."
    },
    "cyber_fraud": {
        "id": "cyber_fraud",
        "title": "Reporting Cyber Fraud & Financial Theft",
        "act": "Information Technology Act, 2000 & BNS 2023",
        "short_act": "IT Act 2000 / BNS 2023",
        "category": "Cyber Crime & Financial Protection",
        "summary": "Immediate action steps when cheated online, scammed via UPI/Netbanking, or victim of identity theft.",
        "icon": "shield-alert",
        "key_sections": ["IT Act Section 66C (Identity Theft)", "IT Act Section 66D (Cheating by Impersonation)", "BNS Section 318 (Cheating)"],
        "timeline": "Golden Hours: Report within 2-4 hours to block fraudulent transfer",
        "fee": "Free",
        "steps": [
            {
                "step": 1,
                "title": "Call Cyber Helpline 1930 Immediately",
                "description": "Dial 1930 (National Cyber Crime Helpline). Provide details of transaction ID, bank account, and scammer details to freeze funds."
            },
            {
                "step": 2,
                "title": "Block Banking Cards & UPI Handles",
                "description": "Contact your bank hotline immediately to temporarily freeze internet banking, debit/credit cards, and UPI apps."
            },
            {
                "step": 3,
                "title": "Register Complaint on cybercrime.gov.in",
                "description": "Visit National Cyber Crime Reporting Portal (cybercrime.gov.in), register under Financial Fraud, upload screenshots, SMS, and bank statement."
            },
            {
                "step": 4,
                "title": "File Written Complaint at Local Cyber Cell / Police Station",
                "description": "Submit a hardcopy complaint along with Cyber Crime Acknowledgment slip to the nearest Police Station or Cyber Cell."
            },
            {
                "step": 5,
                "title": "Submit Dispute Notice to Bank",
                "description": "As per RBI circular on Zero Liability in Unauthorized Electronic Banking Transactions, notify your bank within 3 working days."
            }
        ],
        "important_note": "Reporting within the first 2 hours ('Golden Hours') drastically increases the chance of recovering frozen funds."
    },
    "zero_fir": {
        "id": "zero_fir",
        "title": "Filing a Police Complaint & Zero FIR",
        "act": "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
        "short_act": "BNSS 2023",
        "category": "Criminal Law & Public Safety",
        "summary": "How to lodge an FIR at any police station regardless of territorial jurisdiction for cognizable offenses.",
        "icon": "shield",
        "key_sections": ["BNSS Section 173 (Information in cognizable cases / FIR)", "BNSS Section 35 (Arrest procedure & rights)", "BNSS Section 176 (Forensic investigation mandatory for 7+ yrs imprisonment)"],
        "timeline": "Immediate upon occurrence of cognizable offense",
        "fee": "Free (Copy of FIR must be provided free of cost immediately)",
        "steps": [
            {
                "step": 1,
                "title": "Approach Any Nearest Police Station",
                "description": "You can visit ANY police station, even outside the jurisdiction of crime location, to request a 'Zero FIR'."
            },
            {
                "step": 2,
                "title": "Narrate the Incident to Officer-in-Charge",
                "description": "State exact facts: date, time, location, suspect description, witnesses, and details of offense."
            },
            {
                "step": 3,
                "title": "Read & Sign the Recorded Statement",
                "description": "Verify the recorded complaint. Under BNSS Section 173, electronic communication (e-FIR) is also recognized."
            },
            {
                "step": 4,
                "title": "Obtain Free Copy of FIR",
                "description": "Under BNSS 173(2), the informant is legally entitled to receive an instant copy of the FIR free of charge."
            },
            {
                "step": 5,
                "title": "If Police Refuse to File FIR",
                "description": "Send written substance to Superintendent of Police (SP) by post or file application to Magistrate under BNSS Section 175(3)."
            }
        ],
        "important_note": "A Zero FIR is assigned number '0' and transferred to the appropriate jurisdictional police station after registration."
    },
    "domestic_violence": {
        "id": "domestic_violence",
        "title": "Seeking Protection Against Domestic Violence",
        "act": "Protection of Women from Domestic Violence Act, 2005",
        "short_act": "DVA 2005",
        "category": "Women & Family Safety",
        "summary": "Procedure to obtain immediate protection orders, residence orders, and monetary relief against abuse.",
        "icon": "heart-handshake",
        "key_sections": ["Section 3 (Definition of DV - physical, emotional, sexual, economic)", "Section 12 (Application to Magistrate)", "Section 18-22 (Protection & Residence Orders)"],
        "timeline": "Magistrate must fix first hearing within 3 days; disposal targeted in 60 days",
        "fee": "Free legal aid available under NALSA / DLSA",
        "steps": [
            {
                "step": 1,
                "title": "Call Women Helpline 181 or 112",
                "description": "For urgent rescue or safety, call emergency helpline 181 (Women Helpline) or 112 (National Emergency Response)."
            },
            {
                "step": 2,
                "title": "Contact Protection Officer / Service Provider",
                "description": "Reach out to the local Protection Officer (appointed in every district) or authorized NGO service provider."
            },
            {
                "step": 3,
                "title": "File DIR (Domestic Incident Report)",
                "description": "Protection Officer records DIR detailing incidents of physical, verbal, sexual, or economic abuse."
            },
            {
                "step": 4,
                "title": "Application to Magistrate (Section 12)",
                "description": "Submit application seeking Protection Orders (stopping contact), Residence Orders (right to reside in shared household), or Maintenance."
            },
            {
                "step": 5,
                "title": "Ex-Parte Emergency Relief",
                "description": "If immediate danger exists, Magistrate can pass interim ex-parte order on same day under Section 23."
            }
        ],
        "important_note": "Under DVA 2005, a woman cannot be evicted from shared household without legal process, regardless of title ownership."
    },
    "wage_grievance": {
        "id": "wage_grievance",
        "title": "Filing Grievance for Unpaid Wages & Workplace Safety",
        "act": "Code on Wages 2019 & OSH Code 2020",
        "short_act": "Code on Wages 2019 / OSH 2020",
        "category": "Labor & Employee Rights",
        "summary": "Steps for employees to recover withheld salaries, minimum wages, overtime pay, or report unsafe factory conditions.",
        "icon": "briefcase",
        "key_sections": ["Wages Code Section 17 (Timely Payment of Wages)", "Wages Code Section 45 (Claims Procedure)", "OSH Code Section 6 (Duties of Employer)"],
        "timeline": "Claim to be filed within 3 years",
        "fee": "Nil / Nominal",
        "steps": [
            {
                "step": 1,
                "title": "Issue Written Wage Demand to Employer",
                "description": "Send email/letter citing employment contract, attendance records, pay slips, and unpaid duration."
            },
            {
                "step": 2,
                "title": "File Complaint on Shram Suvidha / Samadhan Portal",
                "description": "Register grievance online on Ministry of Labour portal (samadhan.labour.gov.in) or state labor commissioner portal."
            },
            {
                "step": 3,
                "title": "Approach Inspector-cum-Facilitator",
                "description": "File claim under Section 45 before the designated Authority/Inspector-cum-Facilitator for recovery of wages."
            },
            {
                "step": 4,
                "title": "Conciliation & Order",
                "description": "Authority conducts inquiry. Employer can be directed to pay unpaid amount plus penalty up to 10x of claimed sum."
            }
        ],
        "important_note": "Wages must be paid before 7th/10th day of following month. Upon removal/resignation, wages must be cleared within 2 working days."
    }
}


def get_all_procedures():
    """Returns list of all available procedural guides."""
    return list(PROCEDURES_DATABASE.values())


def get_procedure_by_id(proc_id):
    """Retrieve procedure by key ID."""
    return PROCEDURES_DATABASE.get(proc_id, None)


def search_procedures(query):
    """Search procedures by keyword in query."""
    query_lower = query.lower()
    results = []
    for proc in PROCEDURES_DATABASE.values():
        match_score = 0
        if any(term in query_lower for term in proc["title"].lower().split()):
            match_score += 3
        if any(term in query_lower for term in proc["summary"].lower().split()):
            match_score += 2
        if any(term in query_lower for term in proc["category"].lower().split()):
            match_score += 1
        if any(term in query_lower for term in proc["act"].lower().split()):
            match_score += 2
            
        # Check specific keywords
        keywords = {
            "rti": ["rti", "information", "government record", "public officer", "status", "application"],
            "consumer_complaint": ["consumer", "refund", "defective", "product", "seller", "amazon", "flipkart", "fraud product", "service"],
            "cyber_fraud": ["cyber", "bank", "scam", "upi", "otp", "stolen", "online fraud", "phishing", "hacked", "money lost"],
            "zero_fir": ["fir", "police", "crime", "theft", "complaint", "assault", "accident", "station"],
            "domestic_violence": ["domestic", "abuse", "husband", "in-laws", "violence", "wife", "protection order", "beaten", "harassment"],
            "wage_grievance": ["wage", "salary", "employer", "company", "unpaid", "job", "workplace", "labor", "labour", "bonus"]
        }
        
        for k, tags in keywords.items():
            if k == proc["id"]:
                if any(t in query_lower for t in tags):
                    match_score += 4

        if match_score > 0:
            results.append((match_score, proc))

    results.sort(key=lambda x: x[0], reverse=True)
    return [r[1] for r in results]
