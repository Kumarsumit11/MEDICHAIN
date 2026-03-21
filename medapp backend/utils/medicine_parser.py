import pdfplumber
import re

def extract_medicines_from_pdf(pdf_path: str):
    medicines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            for line in text.split("\n"):
                line = line.strip()

                # Detect medicine lines
                if re.match(
                    r"^(Tab|Cap|Syrup|Injection|Tablet)\s+",
                    line,
                    re.IGNORECASE,
                ):
                    medicines.append({
                        "name": line,
                        "dosage": "As prescribed",
                        "duration": "Ongoing",
                        "status": "Active",
                    })

    return medicines
