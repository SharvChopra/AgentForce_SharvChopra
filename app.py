# app.py
import streamlit as st
import requests
import json
import io

st.set_page_config(layout="wide")

st.title("⚖️ Legal Document AI Assistant")
st.header("Upload a PDF to process and analyze contract clauses.")

fastapi_base_url = "http://127.0.0.1:8000"

st.subheader("1. Upload Your Legal Document")
uploaded_file = st.file_uploader(
    "Choose a PDF file", type="pdf", key="pdf_uploader")

if uploaded_file:
    st.info("File uploaded successfully. Processing and indexing document chunks...")
    try:
        files = {"file": (uploaded_file.name,
                          uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(
            f"{fastapi_base_url}/upload-pdf/", files=files)

        if response.status_code == 200:
            data = response.json()
            st.success("Document processed and analyzed successfully!")

            # Display automatic analysis results
            st.subheader("Document Analysis")
            if not data.get("analysis_results"):
                st.info("No clauses were found or analyzed in the document.")
            for i, result in enumerate(data.get("analysis_results", [])):
                with st.expander(f"**Clause {i+1}: {result.get('clause_type', 'N/A')}**"):
                    st.text_area("Original Content", result.get(
                        "original_clause_text", ""), height=200, key=f"orig_clause_{i}")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_area("Summary", result.get(
                            'summary', ''), height=150, key=f"summary_{i}")
                    with col2:
                        st.text_area("Questions to Ask", result.get(
                            'questions_to_ask', ''), height=150, key=f"questions_{i}")
                    st.text_area("Suggested Improvements", result.get(
                        'suggested_improvements', ''), height=150, key=f"suggestions_{i}")

            # Display default compliance check results
            st.subheader("In-built Compliance Check")
            missing_clauses = data.get("default_compliance_check", [])
            if missing_clauses:
                st.warning(
                    "⚠️ The following required clauses are potentially missing:")
                for clause in missing_clauses:
                    st.text(f"- {clause['name']}")
                    st.text(f"  Expected Text: {clause['expected_text']}")
            else:
                st.success("🎉 All in-built compliance clauses were found!")

        else:
            st.error(
                f"Error from backend during upload: {response.json().get('detail', 'Unknown error')}")

    except requests.exceptions.ConnectionError:
        st.error("Connection failed. Please ensure the FastAPI backend is running.")
    except Exception as e:
        st.error(f"An unexpected error occurred during file upload: {e}")

st.subheader("2. Check Against Custom Compliance Checklist")
st.markdown(
    "Upload a JSON file containing a compliance checklist to check for missing clauses.")
uploaded_checklist = st.file_uploader(
    "Choose a JSON file", type="json", key="checklist_uploader")

if st.button("Run Custom Compliance Check", key="compliance_button"):
    if uploaded_file and uploaded_checklist:
        st.info("Running custom compliance check...")
        try:
            checklist_data = json.load(uploaded_checklist)
            response = requests.post(
                f"{fastapi_base_url}/check-compliance/", json=checklist_data)

            if response.status_code == 200:
                compliance_results = response.json()
                if not compliance_results.get('missing_clauses'):
                    st.success(
                        "🎉 Custom compliance check passed! All required clauses were found.")
                else:
                    st.warning(
                        "⚠️ The following required clauses are potentially missing:")
                    for clause in compliance_results['missing_clauses']:
                        st.text(f"- {clause['name']}")
                        st.text(f"  Expected Text: {clause['expected_text']}")
            else:
                st.error(
                    f"Error during custom compliance check: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Connection failed. Ensure the FastAPI backend is running.")
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please check the file format.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning(
            "Please upload both a PDF and a JSON checklist to run the check.")
