import joblib

from pdf_loader import load_pdf
from chunker import create_chunks


documents = [

    {
        "file": "data/pdfs/BNS.pdf",
        "name": "Bharatiya Nyaya Sanhita, 2023",
        "short": "BNS"
    },

    {
        "file": "data/pdfs/BNSS.pdf",
        "name": "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "short": "BNSS"
    },

    {
        "file": "data/pdfs/BSA.pdf",
        "name": "Bharatiya Sakshya Adhiniyam, 2023",
        "short": "BSA"
    },

    {
        "file": "data/pdfs/COD.pdf",
        "name": "Code on Wages, 2019",
        "short": "COW"
    },

    {
        "file": "data/pdfs/COI.pdf",
        "name": "Constitution of India",
        "short": "COI"
    },

    {
        "file": "data/pdfs/CPA.pdf",
        "name": "Consumer Protection Act, 2019",
        "short": "CPA"
    },

    {
        "file": "data/pdfs/IRC.pdf",
        "name": "Industrial Relations Code, 2020",
        "short": "IRC"
    },

    {
        "file": "data/pdfs/IT ACT.pdf",
        "name": "Information Technology Act, 2000",
        "short": "ITA"
    },

    {
        "file": "data/pdfs/OSH.pdf",
        "name": "Occupational Safety, Health and Working Conditions Code, 2020",
        "short": "OSH"
    },

    {
        "file": "data/pdfs/PCSO.pdf",
        "name": "Protection of Children from Sexual Offences Act, 2012",
        "short": "PCSO"
    },

    {
        "file": "data/pdfs/RTI.pdf",
        "name": "Right to Information Act, 2005",
        "short": "RTI"
    },

    {
        "file": "data/pdfs/Women protect.pdf",
        "name": "Protection of Women from Domestic Violence Act, 2005",
        "short": "DVA"
    }
]

all_chunks = []


for document in documents:

    print("\n======================================")
    print("Processing:", document["name"])
    print("======================================")

    pages = load_pdf(document["file"])

    print("Pages:", len(pages))

    chunks = create_chunks(
        pages,
        document["name"],
        document["short"]
    )

    print("Chunks:", len(chunks))

    all_chunks.extend(chunks)


# Save using Joblib

joblib.dump(
    all_chunks,
    "data/chunks.joblib"
)


print("\n======================================")
print("DONE")
print("======================================")

print("Total chunks:", len(all_chunks))

print("Saved to: data/chunks.joblib")