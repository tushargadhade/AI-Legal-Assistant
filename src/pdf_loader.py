from pypdf import PdfReader


def load_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text is None:
            text = ""

        pages.append({
            "page": page_number,
            "text": text
        })

    return pages


if __name__ == "__main__":

    pdf_path = "data/pdfs/BNS.pdf"

    pages = load_pdf(pdf_path)

    print("Total pages:", len(pages))

    print("\nFirst page:")
    print(pages[0]["text"][:1000])