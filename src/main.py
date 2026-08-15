"""
Main Entry Point for AI Legal Assistant
Supports launching the Web API server and interactive CLI.
"""

import os
import sys

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from build_data import build_data
from build_index import build_index
from search import search, display_results
from procedures import get_all_procedures
from backend_api import run_server

def print_banner():
    print("""
  =================================================================
                  AI LEGAL ASSISTANT (INDIA)                      
        Bridging Legal Awareness & Access to Justice for Citizens 
  =================================================================
    """)

def main():
    print_banner()
    while True:
        print("\n=============================================")
        print("           MAIN APPLICATION MENU             ")
        print("=============================================")
        print("1. Launch Web App & API Server (Recommended)")
        print("2. Search Legal Documents (CLI Mode)")
        print("3. View Citizen Rights & Procedural Guides")
        print("4. Process PDFs and Build Chunks Data")
        print("5. Build BM25 Search Index")
        print("6. Exit")
        print("=============================================")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            print("\nStarting AI Legal Assistant Web Server on http://localhost:5000 ...")
            run_server(port=5000)
        elif choice == '2':
            print("\n--- Legal Document Search (CLI) ---")
            question = input("\nEnter your legal question: ")
            if question.strip():
                results = search(query=question, top_k=5)
                display_results(results)
        elif choice == '3':
            print("\n--- Citizen Rights & Procedural Guides ---")
            procs = get_all_procedures()
            for idx, p in enumerate(procs, 1):
                print(f"{idx}. {p['title']} [{p['short_act']}]")
            
            p_choice = input("\nSelect procedure number to view details (or press Enter to return): ").strip()
            if p_choice.isdigit() and 1 <= int(p_choice) <= len(procs):
                proc = procs[int(p_choice) - 1]
                print(f"\n==========================================")
                print(f"TITLE: {proc['title']}")
                print(f"ACT:   {proc['act']}")
                print(f"TIME:  {proc['timeline']} | FEE: {proc['fee']}")
                print(f"==========================================")
                print(f"Summary: {proc['summary']}\n")
                print("STEPS:")
                for step in proc['steps']:
                    print(f" Step {step['step']}: {step['title']}")
                    print(f"   {step['description']}")
                print(f"\nNote: {proc['important_note']}")
        elif choice == '4':
            print("\n--- Processing Legal PDFs ---")
            build_data()
        elif choice == '5':
            print("\n--- Building BM25 Index ---")
            build_index()
        elif choice == '6':
            print("Exiting AI Legal Assistant...")
            break
        else:
            print("Invalid choice, please select between 1 and 6.")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    main()
