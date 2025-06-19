from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from uuid import uuid4
import pyodbc
from docx import Document
import fitz  # PyMuPDF for PDF

app = FastAPI()
UPLOAD_DIR = "app/uploads"

# SQL Server connection settings
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=Venus;"
    "DATABASE=Demo;"
    "UID=bcrisp;"
    "PWD=Bcrisp*5"
)

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(upload_file: UploadFile) -> str:
    file_id = str(uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{upload_file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    return file_path

def extract_text(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

def summarize_text(text: str) -> str:
    # MOCK summary - replace with any logic you want
    # For example, first 300 characters or some placeholder text
    return f"Mock summary: Document contains {len(text)} characters. Key points need manual review."

def store_summary_to_db(file_name: str, summary: str):
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'DocumentSummaries')
        CREATE TABLE DocumentSummaries (
            ID INT IDENTITY PRIMARY KEY,
            FileName NVARCHAR(255),
            Summary NVARCHAR(MAX),
            CreatedAt DATETIME DEFAULT GETDATE()
        )
    """)
    conn.commit()
    cursor.execute(
        "INSERT INTO DocumentSummaries (FileName, Summary) VALUES (?, ?)",
        (file_name, summary)
    )
    conn.commit()
    cursor.close()
    conn.close()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        path = save_file(file)
        raw_text = extract_text(path)
        summary = summarize_text(raw_text)
        store_summary_to_db(file.filename, summary)
        return JSONResponse({"file": file.filename, "summary": summary})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
