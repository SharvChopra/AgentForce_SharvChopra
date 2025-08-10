Legal Document AI Assistant
Overview
The Legal Document AI Assistant is a web-based application designed to streamline the contract review process. It automates the analysis of legal PDFs, providing instant summaries, compliance checks, and intelligent suggestions. Built with a modern, modular architecture, this tool helps legal professionals save time, reduce errors, and proactively identify risks.

Key Features
Automated Document Analysis: Upload a PDF and the application automatically analyzes its clauses.

Clause Summaries: Get concise, bullet-point summaries of each key clause.

Proactive Risk Identification: The system generates critical questions a lawyer should ask to clarify ambiguous clauses.

Compliance Checks: An in-built checklist verifies if a document contains essential clauses. Users can also upload custom JSON checklists for their own compliance needs.

Improvement Suggestions: The AI suggests improvements to clauses to make them more favorable to the client.

Technical Stack
Backend: FastAPI for building high-performance API endpoints.

Frontend: Streamlit for a simple and interactive user interface.

LLM: Google Gemini 1.5 Flash for powerful and efficient natural language understanding.

Vector Database: ChromaDB for creating a searchable knowledge base of the document, enabling Retrieval-Augmented Generation (RAG).

Orchestration: LangChain for managing the entire AI workflow, from text splitting to LLM interaction.

Getting Started
1. Prerequisites
Before running the application, ensure you have Python 3.8+ installed. You also need a Google API key for the Gemini model.

Important: Your Google API key is sensitive information. Do not upload it to GitHub.

2. Google API Key Setup
Obtain a Google API key from the Google AI Studio.

In the root directory of this project, create a new file named .env.

Add the following line to the .env file, replacing YOUR_API_KEY with your actual key:

GOOGLE_API_KEY=YOUR_API_KEY
3. Installation
Clone the repository and install the required dependencies:

Bash

git clone https://github.com/your-username/Legal-Summarizer.git
cd Legal-Summarizer

4. Running the Application
The application consists of a backend (FastAPI) and a frontend (Streamlit). Both need to be running simultaneously.

Step 4.1: Start the Backend
Open your first terminal, navigate to the project root, and run:

Bash

uvicorn main:app --reload
Step 4.2: Start the Frontend
Open a separate terminal, navigate to the project root, and run:

Bash

streamlit run app.py
The application will open in your default web browser.

File Structure
Legal-Summarizer/
├── .env                  # Your environment file (ignored by Git)
├── .gitignore            # Specifies files and directories to ignore
├── app.py                # Streamlit frontend application
├── main.py               # FastAPI backend application
├── llm_operations.py     # Functions for interacting with the LLM
├── vector_operations.py  # Functions for creating and loading the vector database
├── compliance_checker.py # Functions for compliance checks
├── default_compliance_checklist.json # In-built compliance checklist
├── requirements.txt      # Project dependencies
└── README.md             # This file
