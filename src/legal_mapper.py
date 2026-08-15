"""
Legal Cross-Reference Mapper & Citizen Empowerment Scorecard Module
Maps old Indian Penal Code (IPC) / CrPC sections to new Bharatiya Nyaya Sanhita (BNS) & BNSS,
and provides legal risk/rights empowerment calculations for citizens.
"""

# IPC to BNS Mapping Database
IPC_BNS_MAP = {
    "302": {"old": "IPC Section 302 (Murder)", "new": "BNS Section 103 (Punishment for Murder)", "notes": "Punishment remains death or imprisonment for life."},
    "307": {"old": "IPC Section 307 (Attempt to Murder)", "new": "BNS Section 109 (Attempt to Murder)", "notes": "Covered under offenses against life."},
    "376": {"old": "IPC Section 376 (Rape)", "new": "BNS Section 64 (Punishment for Rape)", "notes": "Enhanced protection and stringent procedure."},
    "420": {"old": "IPC Section 420 (Cheating & Dishonesty)", "new": "BNS Section 318 (Cheating)", "notes": "Includes cheating by impersonation and property delivery."},
    "379": {"old": "IPC Section 379 (Theft)", "new": "BNS Section 303 (Theft)", "notes": "Includes snatching as a specific distinct offense under Section 304."},
    "506": {"old": "IPC Section 506 (Criminal Intimidation)", "new": "BNS Section 351 (Criminal Intimidation)", "notes": "Punishment for threatening harm or injury."},
    "498a": {"old": "IPC Section 498A (Cruelty by Husband/Relatives)", "new": "BNS Section 85 (Husband/relative subjecting woman to cruelty)", "notes": "Cognizable and non-bailable offense."},
    "154_crpc": {"old": "CrPC Section 154 (FIR Filing)", "new": "BNSS Section 173 (Information in cognizable cases)", "notes": "Recognizes Zero FIR and e-FIR via electronic communication."},
    "41a_crpc": {"old": "CrPC Section 41A (Notice of Appearance)", "new": "BNSS Section 35(3) (Notice of appearance before police)", "notes": "Mandatory notice before arrest for offenses punishable under 7 years."}
}

def lookup_ipc_bns(query):
    """Look up old IPC/CrPC section numbers and return BNS/BNSS equivalencies."""
    query_clean = str(query).lower().replace("ipc", "").replace("crpc", "").replace("section", "").strip()
    
    matches = []
    for key, data in IPC_BNS_MAP.items():
        if key in query_clean or data["old"].lower().find(query_clean) != -1:
            matches.append(data)
            
    return matches

def calculate_citizen_empowerment_score(scenario_type, answers):
    """
    Computes an empirical Citizen Empowerment & Action Readiness Score (0-100%)
    based on scenario parameters.
    """
    score = 50 # Baseline
    factors = []
    
    if scenario_type == "cyber_fraud":
        time_elapsed = answers.get("time_elapsed_hours", 24)
        notified_bank = answers.get("notified_bank", False)
        called_1930 = answers.get("called_1930", False)
        has_txn_proof = answers.get("has_txn_proof", True)
        
        if time_elapsed <= 2:
            score += 30
            factors.append("✅ Within Golden Hours (0-2 hrs): High probability of freezing scammer account.")
        elif time_elapsed <= 24:
            score += 10
            factors.append("⚠️ Reported within 24 hours: Moderate recovery chance.")
        else:
            score -= 15
            factors.append("❌ Over 24 hours elapsed: Bank escalation requires formal police complaint.")
            
        if called_1930:
            score += 15
            factors.append("✅ 1930 National Cyber Helpline notified.")
        if notified_bank:
            score += 10
            factors.append("✅ Bank account/cards blocked under RBI Zero Liability rules.")
        if has_txn_proof:
            score += 5
            factors.append("✅ Transaction ID & SMS proof available.")

    elif scenario_type == "rti":
        has_specific_questions = answers.get("has_specific_questions", True)
        is_bpl = answers.get("is_bpl", False)
        knows_department = answers.get("knows_department", True)
        
        if knows_department:
            score += 20
            factors.append("✅ Exact Public Authority / Department identified.")
        if has_specific_questions:
            score += 20
            factors.append("✅ Clear, objective questions formulated (certified copy / file status).")
        if is_bpl:
            score += 10
            factors.append("✅ BPL cardholder: Fee waived under Section 7(5).")
            
    elif scenario_type == "consumer":
        has_invoice = answers.get("has_invoice", True)
        notice_sent = answers.get("notice_sent", False)
        within_2_years = answers.get("within_2_years", True)
        
        if has_invoice:
            score += 25
            factors.append("✅ Valid tax invoice / payment proof available.")
        if notice_sent:
            score += 20
            factors.append("✅ 15-day legal notice served to seller.")
        if within_2_years:
            score += 10
            factors.append("✅ Within 2-year limitation period under CPA Section 69.")

    score = max(10, min(100, score))
    
    readiness_level = "High Action Readiness" if score >= 75 else ("Moderate Readiness" if score >= 50 else "Action Required")
    
    return {
        "score": score,
        "readiness_level": readiness_level,
        "factors": factors
    }
