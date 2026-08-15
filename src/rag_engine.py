"""
RAG Engine for AI Legal Assistant
Combines BM25 retrieval across Indian Legal Acts with Gemini AI & fallback local plain-language summarization.
"""

import os
import re
import joblib
import pandas as pd
from rank_bm25 import BM25Okapi

from procedures import search_procedures, get_all_procedures

INDEX_PATH = "data/bm25_index.pkl"
CSV_PATH = "data/chunks.csv"

DISCLAIMER_TEXT = (
    "⚠️ DISCLAIMER: This AI Legal Assistant provides informational summaries of government laws and legal regulations "
    "for educational and awareness purposes only. It DOES NOT provide professional legal advice, representation, or opinions. "
    "For formal legal advice or court matters, please consult a qualified licensed advocate or legal practitioner."
)


def preprocess(text):
    """Normalize text for BM25 search."""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = text.split()
    return tokens


def ensure_index():
    """Ensure data files and BM25 index exist."""
    if os.path.exists(INDEX_PATH):
        return True

    print("Index file not found. Rebuilding data and index...")
    try:
        from build_data import build_data
        from build_index import build_index
        build_data()
        build_index()
        return True
    except Exception as e:
        print(f"Error building index: {e}")
        return False


def retrieve_legal_chunks(query, top_k=5):
    """Search BM25 index and return top matching legal chunks."""
    if not os.path.exists(INDEX_PATH):
        success = ensure_index()
        if not success:
            return []

    try:
        index_data = joblib.load(INDEX_PATH)
        bm25 = index_data["bm25"]
        df = index_data["data"]

        query_tokens = preprocess(query)
        if not query_tokens:
            return []

        scores = bm25.get_scores(query_tokens)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        results = []
        for idx in ranked_indices[:top_k]:
            if scores[idx] <= 0 and len(results) >= 2:
                # Cut off zero scores if we already have some top matches
                continue

            row = df.iloc[idx]
            results.append({
                "act_name": str(row.get("act_name", "Indian Act")),
                "act_short_name": str(row.get("act_short_name", "LAW")),
                "section": str(row.get("section", "N/A")),
                "section_title": str(row.get("section_title", "General Provisions")),
                "page": int(row.get("page", 1)),
                "text": str(row.get("text", "")),
                "score": float(scores[idx])
            })
        return results
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []


def generate_gemini_response(query, retrieved_chunks):
    """Use Google Gemini API to produce simple-language legal summary with citations."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        context_blocks = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            context_blocks.append(
                f"--- SOURCE {i} ---\n"
                f"Act: {chunk['act_name']} ({chunk['act_short_name']})\n"
                f"Section: {chunk['section']} - {chunk['section_title']}\n"
                f"Page: {chunk['page']}\n"
                f"Legal Text Snippet:\n{chunk['text']}\n"
            )

        context_str = "\n".join(context_blocks)

        prompt = f"""
You are an expert citizen legal AI assistant for India. Your goal is to explain legal regulations in super simple, 5th-grade plain language so everyday citizens can easily understand their rights and relevant laws.

STRICT SAFETY RULE: You must NEVER provide direct professional legal advice or tell a user what to do in court. Keep your response strictly informational, educational, and grounded in the provided legal sources.

USER QUESTION:
"{query}"

RETRIEVED OFFICIAL LEGAL CLAUSES:
{context_str}

INSTRUCTIONS FOR YOUR RESPONSE:
1. **Simple Summary**: Explain the relevant law in simple, clear everyday bullet points. Translate complex legalese (like "hereinafter", "punishable with imprisonment of either description", "cognizable") into plain English.
2. **Relevant Acts & Sections**: List the specific Acts and Sections that apply.
3. **Key Takeaway / Citizen Guidance**: Provide actionable educational steps (e.g. where to file, what documents are needed, helpline numbers if applicable).
4. Do NOT use overly dense legal jargon. Keep formatting clean with Markdown headers and bullet points.

Begin your response directly.
"""
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
    except Exception as e:
        print(f"Gemini API generation failed/unavailable: {e}")
        return None


def generate_local_plain_summary(query, retrieved_chunks):
    """
    Intelligent local heuristic summarizer fallback that converts legal legalese into simple language
    when Gemini API key is not present.
    """
    if not retrieved_chunks:
        return (
            "### 🔍 No Specific Legal Acts Found\n\n"
            "We could not find an exact section match in the database for your query. "
            "However, you can explore our **Procedural Guides** below for general legal guidance on RTI, Cyber Crime, "
            "Consumer Complaints, FIR filing, or Domestic Violence safety."
        )

    top_act = retrieved_chunks[0]["act_name"]
    top_section = retrieved_chunks[0]["section"]
    top_title = retrieved_chunks[0]["section_title"]

    # Deduplicate acts
    acts_involved = list(dict.fromkeys([c["act_name"] for c in retrieved_chunks]))

    summary_lines = []
    summary_lines.append(f"### 💡 Plain Language Legal Summary\n")
    summary_lines.append(f"Based on **{top_act}** (and related regulations), here is what the law states in simple terms:\n")

    for i, chunk in enumerate(retrieved_chunks[:3], 1):
        clean_text = chunk["text"]
        # Basic legalese simplification rules
        clean_text = re.sub(r'shall be punishable with', 'can result in punishment of', clean_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'hereinafter referred to as', 'called', clean_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'cognizable and non-bailable', 'serious (police can arrest directly without warrant)', clean_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'bailable', 'eligible for bail', clean_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'provided that', 'Note:', clean_text, flags=re.IGNORECASE)

        # Truncate text if too long
        if len(clean_text) > 350:
            clean_text = clean_text[:350] + "..."

        sec_str = f"Section {chunk['section']}" if chunk['section'] != "N/A" else "General Clause"
        summary_lines.append(f"• **{chunk['act_short_name']} ({sec_str} - {chunk['section_title']})**:")
        summary_lines.append(f"  > \"{clean_text}\"")
        summary_lines.append(f"  *Key Takeaway*: This clause governs provisions regarding {chunk['section_title'].lower()} under {chunk['act_short_name']}.\n")

    summary_lines.append(f"### 📋 Applicable Government Acts Identified")
    for act in acts_involved:
        summary_lines.append(f"- **{act}**")

    summary_lines.append("\n### ⚖️ Citizen Awareness Note")
    summary_lines.append(
        "- **Plain Language Translation**: Legal documents use precise formal terms, but in practice, you have the right to request clarification or approach designated officers (like PIO for RTI, Protection Officers for DV, or Cyber Cell for financial scams)."
    )
    summary_lines.append("- Refer to the side-by-side **Original Legal Clause** inspector to read the verbatim government text.")

    return "\n".join(summary_lines)


def process_user_query(query):
    """
    Main pipeline function:
    1. Search BM25 legal database
    2. Try Gemini API for simple language summary; fallback to local smart engine
    3. Retrieve relevant procedural workflows
    4. Attach safety disclaimer
    """
    query = query.strip()
    if not query:
        return {
            "error": "Query cannot be empty",
            "disclaimer": DISCLAIMER_TEXT
        }

    # 1. Retrieve legal chunks
    chunks = retrieve_legal_chunks(query, top_k=5)

    # 2. Generate summary
    ai_summary = generate_gemini_response(query, chunks)
    mode = "Gemini AI Engine"
    if not ai_summary:
        ai_summary = generate_local_plain_summary(query, chunks)
        mode = "Local Smart Engine"

    # 3. Find matching procedural guides
    recommended_procedures = search_procedures(query)

    return {
        "query": query,
        "mode": mode,
        "summary": ai_summary,
        "citations": chunks,
        "recommended_procedures": recommended_procedures,
        "disclaimer": DISCLAIMER_TEXT
    }


if __name__ == "__main__":
    test_q = "What is the procedure and punishment for cyber financial fraud?"
    res = process_user_query(test_q)
    print("MODE:", res["mode"])
    print("SUMMARY:\n", res["summary"][:500])
    print("CITATIONS FOUND:", len(res["citations"]))
    print("PROCEDURES FOUND:", len(res["recommended_procedures"]))
