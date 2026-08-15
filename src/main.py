import os
import sys

# Import functions from member 1
from build_data import build_data

# Import functions from member 2
from build_index import build_index
from search import search, display_results

def main():
    while True:
        print("\n===================================")
        print("LEGAL DOCUMENT SEARCH PIPELINE")
        print("===================================")
        print("1. Process PDFs and Build Data (Member 1)")
        print("2. Build BM25 Index (Member 2)")
        print("3. Search Legal Documents (Member 2)")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\n--- Processing PDFs and Building Data ---")
            build_data()
        elif choice == '2':
            print("\n--- Building BM25 Index ---")
            build_index()
        elif choice == '3':
            print("\n--- Search Legal Documents ---")
            question = input("\nEnter your legal question: ")
            if question.strip():
                results = search(query=question, top_k=5)
                display_results(results)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    main()
