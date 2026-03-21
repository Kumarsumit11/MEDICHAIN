from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from utils.medicine_parser import extract_medicines_from_pdf

app = FastAPI()

# -------------------
# CORS (Demo safe)
# -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_STORAGE = "storage"
os.makedirs(BASE_STORAGE, exist_ok=True)

def sanitize(phone: str):
    return phone.strip()

# -------------------
# 1️⃣ Upload medical record
# -------------------
@app.post("/upload")
async def upload_file(
    phone: str = Form(...),
    category: str = Form(...),  # prescription | lab_report | xray
    file: UploadFile = File(...)
):
    phone = sanitize(phone)
    category = category.lower()

    if category not in ["prescription", "lab_report", "xray"]:
        return {"error": "Invalid category"}

    folder = os.path.join(BASE_STORAGE, phone, category)
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, file.filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    return {"message": "Uploaded", "filename": file.filename}

# -------------------
# 2️⃣ List records by category
# -------------------
@app.get("/records/{phone}")
def list_records(phone: str):
    phone = sanitize(phone)
    user_path = os.path.join(BASE_STORAGE, phone)

    data = {
        "lab_report": [],
        "prescription": [],
        "xray": [],
    }

    for category in data.keys():
        folder = os.path.join(user_path, category)
        if os.path.exists(folder):
            data[category] = os.listdir(folder)

    return data

# -------------------
# 3️⃣ Download record
# -------------------
@app.get("/download/{phone}/{category}/{filename}")
def download_file(phone: str, category: str, filename: str):
    phone = sanitize(phone)
    path = os.path.join(BASE_STORAGE, phone, category, filename)

    return FileResponse(path)

# -------------------
# 4️⃣ Get current medicines (LATEST 2 prescriptions)
# -------------------
@app.get("/medicines/{phone}")
def get_current_medicines(phone: str):
    phone = sanitize(phone)
    folder = os.path.join(BASE_STORAGE, phone, "prescription")

    if not os.path.exists(folder):
        return []

    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".pdf")
    ]

    # Latest 2 prescriptions
    files.sort(key=os.path.getmtime, reverse=True)
    files = files[:2]

    medicines = []
    for pdf in files:
        medicines.extend(extract_medicines_from_pdf(pdf))

    return medicines
