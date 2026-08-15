"""
Flask API & Web Server for AI Legal Assistant
Serves REST API endpoints and static frontend files for hackathon demonstration.
"""

import os
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Add src to python path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_engine import process_user_query, retrieve_legal_chunks, generate_local_plain_summary, DISCLAIMER_TEXT
from procedures import get_all_procedures, get_procedure_by_id, search_procedures
from legal_mapper import lookup_ipc_bns, calculate_citizen_empowerment_score, IPC_BNS_MAP

PUBLIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
app = Flask(__name__)
CORS(app)


# 1. REST API Endpoints
@app.route("/api/status", methods=["GET"])
def get_status():
    index_exists = os.path.exists("data/bm25_index.pkl")
    chunks_count = 0
    if index_exists:
        try:
            import joblib
            data = joblib.load("data/bm25_index.pkl")
            df = data.get("data")
            if df is not None:
                chunks_count = len(df)
        except Exception:
            pass

    return jsonify({
        "status": "online",
        "system": "AI Legal Assistant (India)",
        "indexed_chunks": chunks_count,
        "index_ready": index_exists,
        "gemini_api_configured": bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")),
        "disclaimer": DISCLAIMER_TEXT
    })


@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json(force=True, silent=True) or {}
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query field is required"}), 400
    result = process_user_query(query)
    return jsonify(result)


@app.route("/api/search", methods=["POST"])
def search_endpoint():
    data = request.get_json(force=True, silent=True) or {}
    query = data.get("query", "").strip()
    top_k = int(data.get("top_k", 5))
    if not query:
        return jsonify({"error": "Query field is required"}), 400
    results = retrieve_legal_chunks(query, top_k=top_k)
    return jsonify({
        "query": query,
        "count": len(results),
        "results": results,
        "disclaimer": DISCLAIMER_TEXT
    })


@app.route("/api/procedures", methods=["GET"])
def list_procedures():
    q = request.args.get("q", "").strip()
    if q:
        procs = search_procedures(q)
    else:
        procs = get_all_procedures()
    return jsonify({
        "count": len(procs),
        "procedures": procs
    })


@app.route("/api/procedures/<proc_id>", methods=["GET"])
def get_procedure_detail(proc_id):
    proc = get_procedure_by_id(proc_id)
    if not proc:
        return jsonify({"error": "Procedure not found"}), 404
    return jsonify(proc)


@app.route("/api/bns-mapper", methods=["GET"])
def bns_mapper_endpoint():
    q = request.args.get("q", "").strip()
    if q:
        matches = lookup_ipc_bns(q)
    else:
        matches = list(IPC_BNS_MAP.values())
    return jsonify({
        "query": q,
        "count": len(matches),
        "mappings": matches
    })


@app.route("/api/scorecard", methods=["POST"])
def scorecard_endpoint():
    data = request.get_json(force=True, silent=True) or {}
    scenario_type = data.get("scenario_type", "cyber_fraud")
    answers = data.get("answers", {})
    result = calculate_citizen_empowerment_score(scenario_type, answers)
    return jsonify(result)


@app.route("/api/summarize", methods=["POST"])
def summarize_text_endpoint():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text field is required"}), 400

    mock_chunk = [{
        "act_name": "Provided Legal Text",
        "act_short_name": "RAW TEXT",
        "section": "Clause",
        "section_title": "Direct Input",
        "page": 1,
        "text": text,
        "score": 1.0
    }]
    summary = generate_local_plain_summary("Simplify this legal text", mock_chunk)
    return jsonify({
        "original_text": text,
        "simplified_summary": summary,
        "disclaimer": DISCLAIMER_TEXT
    })


# 2. Explicit Static File Serving (No wildcard catch-alls)
@app.route("/")
def serve_index():
    return send_from_directory(PUBLIC_DIR, "index.html")


@app.route("/style.css")
def serve_css():
    return send_from_directory(PUBLIC_DIR, "style.css")


@app.route("/app.js")
def serve_js():
    return send_from_directory(PUBLIC_DIR, "app.js")


@app.route("/favicon.ico")
def serve_favicon():
    return "", 204


def run_server(port=5000, host="0.0.0.0", debug=False):
    print("\n==========================================")
    print("AI LEGAL ASSISTANT WEB API SERVER")
    print("==========================================")
    print(f"Server URL: http://localhost:{port}")
    print(f"API Health: http://localhost:{port}/api/status")
    print("Press Ctrl+C to stop.")
    print("==========================================\n")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server(port=5000)
