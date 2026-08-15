# ⚖️ AI Legal Assistant (India)

> **Bridging Legal Awareness & Access to Justice for Citizens through AI-Powered Regulations Summarization, Citations & Procedural Guidance.**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Backend-Flask%20%7C%20REST%20API-emerald.svg)]()
[![Retrieval Engine](https://img.shields.io/badge/RAG-BM25%20%2B%20Gemini%20AI-gold.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 Hackathon Problem Statement & Impact

**Problem**: Legal documents, acts of Parliament, and government regulations are filled with complex legal jargon ("legalese"), making them inaccessible to ordinary citizens. This creates a severe barrier to justice, citizen awareness, and legal empowerment.

**Solution**: The **AI Legal Assistant** addresses this challenge by providing an end-to-end, citizen-centric platform that:
1. **Answers Legal Questions** grounded directly in official government legislation.
2. **Summarizes Dense Legalese** into simple, 5th-grade plain English bullet points.
3. **Identifies Relevant Acts & Actionable Procedures** (e.g. filing RTI, Consumer Court complaints, Cyber Fraud 1930 reporting, Zero FIR, Domestic Violence protection orders).
4. **Enforces Safety Guardrails**: Built-in non-advice disclaimers ensuring no unauthorized professional legal advice is rendered.

---

## ✨ Key Features & Innovation

| Feature | Description | Citizen Benefit |
| :--- | :--- | :--- |
| **📖 12 Indian Acts Indexed** | Pre-indexed full text of BNS (2023), BNSS (2023), BSA (2023), RTI (2005), Consumer Protection (2019), IT Act (2000), Domestic Violence (2005), Code on Wages (2019), OSH Code (2020), POCSO (2012), and Constitution of India. | Complete coverage of daily civil, criminal, consumer, labor & digital rights. |
| **💡 Plain Language Summarization** | Translates complex clauses (like *"cognizable and non-bailable"*, *"hereinafter"*, *"punishable with imprisonment of either description"*) into everyday bullet points. | Understand legal rights without needing a law degree. |
| **🔎 Grounded Citations Inspector** | Every answer provides side-by-side exact Act name, Section number, section title, page number, and verbatim clause text. | Zero hallucinations; complete source transparency. |
| **📜 "Know Your Rights" Procedure Hub** | Actionable, step-by-step citizen guides detailing timelines, required fees, helpline numbers, and online portals (rtionline.gov.in, edaakhil.nic.in, cybercrime.gov.in). | Know exact steps to take after an incident occurs. |
| **📝 Legalese Simplifier Tool** | Standalone tool where citizens can paste any complex court order or government document excerpt for an instant simple summary. | Quick understanding of legal notices or government forms. |
| **📥 One-Click PDF Export** | Export simplified legal summaries and procedure guides as clean printable PDF reports. | Save or print legal awareness notes for offline reference. |
| **🛡️ Built-in Offline Fallback** | Runs with Google Gemini API when configured, and falls back to a smart local legal engine offline. | 100% reliable for hackathon live judging demos. |

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    User([Indian Citizen / User]) <--> WebUI[Sleek Web Interface / UI]
    
    subgraph Web UI Layer
        WebUI --> QATab[Legal Q&A Assistant Workspace]
        WebUI --> ProcTab[Know Your Rights Procedure Hub]
        WebUI --> SimplifyTab[Legalese Simplifier Tool]
    end

    subgraph Backend API Layer (Flask)
        QATab --> REST_API[/api/chat Endpoint/]
        ProcTab --> Proc_API[/api/procedures Endpoint/]
        SimplifyTab --> Simp_API[/api/summarize Endpoint/]
    end

    subgraph Hybrid RAG Engine
        REST_API --> BM25[BM25 Okapi Retrieval Engine]
        BM25 <--> IndexData[(bm25_index.pkl / 12 Acts)]
        
        REST_API --> GenAI{Gemini API / Local Fallback}
        GenAI -->|With Key| GeminiModel[Google Gemini 1.5 Flash]
        GenAI -->|Offline| LocalEngine[Rule-Based Heuristic Simplifier]
        
        REST_API --> ProcEngine[Procedures Mapper / src/procedures.py]
    end

    GeminiModel --> FinalResp[Simplified Response + Citations + Guardrails]
    LocalEngine --> FinalResp
    FinalResp --> WebUI
```

---

## 🛠️ Project Structure

```
AI-Legal-Assistant/
├── data/
│   ├── pdfs/               # Official PDF texts of 12 Indian Acts
│   └── bm25_index.pkl      # Pre-built BM25 search index & chunk dataframe
├── public/
│   ├── index.html          # Web UI HTML template
│   ├── style.css           # Modern emerald glassmorphism styling
│   └── app.js              # Interactive UI logic & PDF export script
├── src/
│   ├── main.py             # App CLI runner & server launcher
│   ├── backend_api.py      # Flask REST API server
│   ├── rag_engine.py       # Hybrid retrieval & legal summarizer engine
│   ├── procedures.py       # Citizen rights procedural workflow database
│   ├── pdf_loader.py       # PDF document parser
│   ├── chunker.py          # Legal section chunking & tokenization
│   ├── build_data.py       # Dataset pipeline builder
│   └── build_index.py      # BM25 index builder
├── DOCS.md                 # Complete technical documentation
├── requirements.txt        # Dependencies manifest
└── README.md               # Project overview & quickstart
```

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone Repository & Install Dependencies
```bash
git clone https://github.com/tushargadhade/AI-Legal-Assistant.git
cd AI-Legal-Assistant

# Create virtual environment (optional but recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. (Optional) Set Gemini API Key
To enable Google Gemini AI generation:
```bash
# Windows PowerShell:
$env:GEMINI_API_KEY="your-gemini-api-key-here"

# Linux / Mac:
export GEMINI_API_KEY="your-gemini-api-key-here"
```
*Note: If no API key is set, the system automatically uses the built-in smart local legal engine!*

---

## 🖥️ How to Run

### Option A: Launch Web Application (Recommended for Demo)
Run the server:
```bash
python src/backend_api.py
```
Open your browser and navigate to:
👉 **`http://localhost:5000`**

### Option B: Interactive CLI Launcher
Run the unified command center:
```bash
python src/main.py
```
Select `1` to start the web server, `2` for CLI legal search, or `3` to view citizen procedural guides.

---

## 📡 REST API Reference

| Endpoint | Method | Description | Sample Payload / Params |
| :--- | :--- | :--- | :--- |
| `/api/status` | `GET` | System status, indexed chunks count, and API health | N/A |
| `/api/chat` | `POST` | Natural language legal Q&A with summary, citations & procedures | `{"query": "Procedure for cyber fraud"}` |
| `/api/search` | `POST` | Raw BM25 section retrieval | `{"query": "RTI section 6", "top_k": 5}` |
| `/api/procedures` | `GET` | List all citizen procedural guides | `?q=cyber` (optional search filter) |
| `/api/summarize` | `POST` | Direct legalese text simplifier | `{"text": "Legal section clause..."}` |

---

## 🎤 Hackathon Pitch & Presentation Guide

### Slide 1: The Problem
> *"Over 1.4 billion citizens in India live under complex legal codes. When a consumer receives a defective product, or a citizen faces online cyber fraud, they struggle to understand their legal rights because acts are written in dense legalese."*

### Slide 2: Our Solution — AI Legal Assistant
> *"An AI-powered legal awareness engine that translates Indian acts (BNS, BNSS, RTI, Consumer Act, IT Act) into simple 5th-grade language, shows exact verbatim legal citations, and provides step-by-step procedural workflows for filing complaints."*

### Slide 3: The 3 Pillars
1. **Source Grounding**: 100% grounded in 12 official government legislation PDFs—zero hallucinations.
2. **Actionable Procedures**: Tells citizens *where to go*, *how much fee to pay*, and *timeline for resolution*.
3. **Safety & Guardrails**: Automatic disclaimer engine protecting against unauthorized legal practice.

---

## ⚖️ Legal Disclaimer

This application is developed strictly for **educational, awareness, and informational purposes**. It does not constitute professional legal advice, formal representation, or legal counsel. Citizens requiring legal representation in court should consult a certified licensed advocate.

---

## 👥 Credits & Team

Developed for the **Hackathon Challenge**:
- **Dataset & Acts Pipeline**: Processing official gazette notifications & legislation.
- **RAG & NLP Engine**: BM25 Okapi + Google Gemini 1.5 Flash + Local Fallback Engine.
- **User Experience**: Glassmorphism dark theme with PDF export capability.

*Built with ❤️ to democratize access to legal awareness for every citizen.*