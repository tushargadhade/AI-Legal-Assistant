def find_section(line):

    line = line.strip()

    parts = line.split(".")

    if len(parts) >= 2:

        number = parts[0].strip()

        if number.isdigit():

            title = ".".join(parts[1:]).strip()

            if title:
                return number, title

    return None, None


def create_chunks(
    pages,
    act_name,
    act_short_name,
    chunk_size=500
):

    chunks = []

    current_section = None
    current_title = None

    chunk_number = 1

    for page in pages:

        text = page["text"]

        lines = text.splitlines()

        current_text = []

        for line in lines:

            line = line.strip()

            if line == "":
                continue

            section_number, section_title = find_section(line)

            if section_number is not None:

                current_section = section_number
                current_title = section_title

            current_text.append(line)

        words = " ".join(current_text).split()

        for i in range(0, len(words), chunk_size):

            chunk_text = " ".join(
                words[i:i + chunk_size]
            )

            chunks.append({

                "chunk_id":
                    f"{act_short_name}_{chunk_number}",

                "act_name":
                    act_name,

                "act_short_name":
                    act_short_name,

                "page":
                    page["page"],

                "section":
                    current_section,

                "section_title":
                    current_title,

                "text":
                    chunk_text
            })

            chunk_number += 1

    return chunks


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