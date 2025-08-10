# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
import PyPDF2
import re
from io import BytesIO
import os
import shutil
from typing import Dict

from vector_operations import create_vector_db, load_vector_db
from llm_operations import classify_clause, summarize_clause, generate_questions, suggest_improvements
from compliance_checker import load_checklist, check_compliance

app = FastAPI()
CHROMA_DB_DIR = "./chroma_db"


def preprocess_text(text: str) -> str:
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()


def analyze_document_clauses(vector_db):
    # This retrieves all chunks and then processes them
    all_chunks = vector_db.similarity_search(
        "all clauses in the document", k=10)
    results = []
    for doc in all_chunks:
        clause_text = doc.page_content
        try:
            clause_type = classify_clause(clause_text)
            summary = summarize_clause(clause_text, clause_type)
            questions = generate_questions(clause_text, clause_type)
            suggestions = suggest_improvements(clause_text, clause_type)

            results.append({
                "original_clause_text": clause_text,
                "clause_type": clause_type,
                "summary": summary,
                "questions_to_ask": questions,
                "suggested_improvements": suggestions
            })
        except Exception as e:
            print(f"Error processing a clause: {e}")
            continue
    return results


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a PDF.")

    try:
        pdf_content = await file.read()
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
        extracted_text = "".join(
            page.extract_text() or "" for page in pdf_reader.pages)

        if not extracted_text:
            raise HTTPException(
                status_code=400, detail="Could not extract text from the PDF.")

        clean_text = preprocess_text(extracted_text)

        if os.path.exists(CHROMA_DB_DIR):
            shutil.rmtree(CHROMA_DB_DIR)

        vector_db = create_vector_db(
            clean_text, persist_directory=CHROMA_DB_DIR)

        # Perform automatic analysis
        analysis_results = analyze_document_clauses(vector_db)

        # Perform in-built compliance check
        default_checklist = load_checklist("compliance_checklist.json")
        missing_clauses = check_compliance(vector_db, default_checklist)

        return {
            "message": "PDF processed and analyzed.",
            "analysis_results": analysis_results,
            "default_compliance_check": missing_clauses
        }

    except Exception as e:
        print(f"Error during PDF processing: {e}")
        raise HTTPException(
            status_code=500, detail=f"An internal server error occurred: {e}")


@app.post("/check-compliance/")
async def check_compliance_endpoint(checklist: Dict):
    vector_db = load_vector_db(persist_directory=CHROMA_DB_DIR)
    if not vector_db:
        raise HTTPException(
            status_code=404, detail="Vector database not found. Please upload a PDF first.")

    try:
        missing_clauses = check_compliance(vector_db, checklist)
        return {"status": "success", "missing_clauses": missing_clauses}
    except Exception as e:
        print(f"Error during compliance check: {e}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred during compliance check: {e}")
