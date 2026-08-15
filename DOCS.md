# 📚 Technical Documentation & System Specifications

## AI Legal Assistant - Architecture & Implementation Details

---

## 1. System Overview

The **AI Legal Assistant** is a Hybrid Retrieval-Augmented Generation (RAG) system engineered specifically to handle Indian legal acts and regulations.

```
       [Raw PDF Documents] (BNS, BNSS, BSA, RTI, CPA, IT Act, etc.)
                                │
                                ▼
                       [pypdf Page Extractor]
                                │
                                ▼
                     [Section & Title Chunker]
                                │
                                ▼
                    [BM25 Index & Vector Store]
                                │
                                ▼
     User Query ──► [Hybrid BM25 Keyword Search] ──► Top K Legal Chunks
                                                        │
                                                        ▼
                                       [Gemini 1.5 / Local Heuristic RAG]
                                                        │
                                                        ▼
                                       [Plain Summary + Cited Sources + Procedures]
```

---

## 2. Indexed Legal Dataset

The system parses and indexes **12 Core Acts of Indian Jurisprudence**:

1. **Bharatiya Nyaya Sanhita, 2023 (BNS)** - Replaced IPC (Criminal Law, offenses against body, property, fraud).
2. **Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)** - Replaced CrPC (Procedure, Zero FIR, arrest rights, bail).
3. **Bharatiya Sakshya Adhiniyam, 2023 (BSA)** - Replaced Evidence Act (Electronic evidence, witness statements).
4. **Right to Information Act, 2005 (RTI)** - Public authority requests, PIO duties, timelines (Section 6, 7, 19).
5. **Consumer Protection Act, 2019 (CPA)** - E-commerce disputes, product defects, e-Daakhil filing.
6. **Information Technology Act, 2000 (IT Act)** - Cyber financial fraud, identity theft (Sec 66C, 66D), data protection.
7. **Protection of Women from Domestic Violence Act, 2005 (DVA)** - Protection orders, residence rights, DIR filing.
8. **Code on Wages, 2019 (COW)** - Wage clearance rules, minimum wage, recovery via Inspector-cum-Facilitator.
9. **Occupational Safety, Health & Working Conditions Code, 2020 (OSH)** - Workplace safety & employee rights.
10. **Protection of Children from Sexual Offences Act, 2012 (PCSO)** - Special protection & reporting.
11. **Industrial Relations Code, 2020 (IRC)** - Dispute resolution for labor.
12. **Constitution of India (COI)** - Fundamental Rights (Articles 14, 19, 21), Fundamental Duties.

---

## 3. Retrieval & NLP Pipeline Algorithm

### A. Section-Aware Chunking (`src/chunker.py`)
Standard character-count chunking splits legal clauses across arbitrary boundaries, losing critical section context. Our chunker implements **Section-Aware Chunking**:
1. Inspects line patterns using regex to capture section numbers (`Section 6. Request for obtaining information...`).
2. Tracks state (`current_section`, `current_title`) continuously.
3. Attaches section metadata to every text chunk:
```json
{
  "chunk_id": "RTI_12",
  "act_name": "Right to Information Act, 2005",
  "act_short_name": "RTI",
  "page": 4,
  "section": "6",
  "section_title": "Request for obtaining information",
  "text": "A person who desires to obtain any information under this Act shall make a request in writing or through electronic means..."
}
```

### B. BM25 Okapi Keyword Retrieval (`src/search.py` & `src/build_index.py`)
- Standard BM25Okapi scoring across normalized tokenized legal text.
- Provides sub-linear TF scaling and inverse document frequency penalization for common words.

### C. Plain Language Summarization & Translation (`src/rag_engine.py`)
- **Gemini Engine**: Uses `gemini-1.5-flash` with grounded prompt constraint. Instructs model to translate legalese into 5th-grade bullet points.
- **Local Smart Engine**: Built-in fallback that operates without internet or API key. Performs rule-based legalese substitution (e.g. `shall be punishable with` ➔ `can result in punishment of`, `cognizable` ➔ `serious (police can arrest directly without warrant)`).

---

## 4. Citizen Rights Procedure Matrix (`src/procedures.py`)

| Procedure ID | Applicable Act | Target Scenario | Helpline / Portal | Key Timeline |
| :--- | :--- | :--- | :--- | :--- |
| `rti_filing` | RTI Act 2005 | Requesting govt records, work updates, exam answer sheets | `rtionline.gov.in` | 30 days (48 hrs if life/liberty) |
| `consumer_complaint` | CPA 2019 | Defective product, service deficiency, false ad | `edaakhil.nic.in` | 2 years limit |
| `cyber_fraud` | IT Act / BNS | UPI scam, OTP theft, online phishing | **1930** / `cybercrime.gov.in` | Golden hours (2-4 hrs) |
| `zero_fir` | BNSS 2023 | Reporting cognizable crime at any police station | Nearest Police Station | Instant FIR copy free |
| `domestic_violence` | DVA 2005 | Seeking protection order against abuse | **181** / **112** / Protection Officer | Hearing within 3 days |
| `wage_grievance` | Code on Wages | Unpaid salary, bonus withholding, workplace safety | `samadhan.labour.gov.in` | Claim within 3 years |

---

## 5. Non-Advice Safety & Guardrails Compliance

To comply with legal standards prohibiting unauthorized legal practice:
1. Every API response includes the mandatory `disclaimer` string.
2. Prompts strictly frame responses as **informational summaries** and **educational awareness**.
3. Direct imperative advice ("You must sue X in court") is replaced with objective procedural options ("A citizen can choose to file a complaint under Section 35 before the District Commission").

---

## 6. Verification & Automated Test Commands

```bash
# 1. Test Dataset Chunk Integrity
python src/build_data.py

# 2. Test BM25 Index Creation
python src/build_index.py

# 3. Test RAG Pipeline Execution
python -c "from rag_engine import process_user_query; print(process_user_query('What is RTI?'))"

# 4. Start Server
python src/backend_api.py
```
