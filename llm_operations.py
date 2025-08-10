import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
# from langchain_community.chat_models import ChatGoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)


def classify_clause(chunk_text: str) -> str:
    prompt_template = """
    Classify the following text chunk into a legal clause type (e.g. Liability,Payment Terms, Indemnification,Governing Law, Scope,Confidentiality,Dispute Resolution, Force Majeure, Intellectual Property,Warranty).
    If it does not fit a specific type, categorize it as 'General'.
    Text:"{chunk_text}"
    Clause Type:
    """

    prompt = PromptTemplate(template=prompt_template,
                            input_variables=["chunk_text"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(chunk_text=chunk_text).strip()


def summarize_clause(chunk_text: str, clause_type: str) -> str:
    prompt_template = """
    You are a legal assistant. Provide a concise, bullet-point summary of the following {clause_type} clause.
    Focus on the main legal implications and key points.
    Clause text:"{clause_text}"
    Summary:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=[
                            "clause_text", "clause_type"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(clause_text=chunk_text, clause_type=clause_type).strip()


def generate_questions(clause_text: str, clause_type: str) -> str:
    prompt_template = """
    You are a senior legal analyst associate reviewing a contract. Analyze the following {clause_type} clause for the potential risks,ambiguities, and legal implications., or missing details.
    Based on your analysis, generate three concise and specific questions that a lawyer should ask the other party to clarify or negotiate this clause.
    Clause:"{clause_text}"
    Questions:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=[
                            "clause_text", "clause_type"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(clause_text=clause_text, clause_type=clause_type).strip()


def suggest_improvements(clause_text: str, clause_type: str) -> str:
    prompt_template = """
    You are a senior legal associate. Based on the following {clause_type} clause, suggest an improved version that is more favorable to the client (assuming a standard commercial client) and clarifies any ambiguities. Briefly explain the reasoning for the changes.
    Clause:"{clause_text}"
    Suggested Improvements:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=[
                            "clause_text", "clause_type"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    return llm_chain.run(clause_text=clause_text, clause_type=clause_type).strip()
