import json
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from typing import List, Dict


def load_checklist(file_path: str) -> Dict:
    with open(file_path, 'r') as f:
        return json.load(f)


def check_compliance(
    vector_db: Chroma, checklist: Dict, similarity_threshold: float = 0.7
) -> List[Dict]:
    missing_clauses = []
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    for required_clause in checklist.get('required_clauses', []):
        required_clause_name = required_clause['name']
        required_clause_text = required_clause['text']
        
        docs_and_scores = vector_db.similarity_search_with_relevance_scores(
            query=required_clause_text,
            k=1,
            score_threshold=0.0
        )

        if not docs_and_scores or docs_and_scores[0][1] < similarity_threshold:
            missing_clauses.append({
                "name": required_clause_name,
                "expected_text": required_clause_text,
                "reason": "Missing or not sufficiently similar to any document clause."
            })
        else:
            found_clause, score = docs_and_scores[0]
            print(f"Found '{required_clause_name}' with score {score:.2f}: {found_clause.page_content[:50]}...")
            
    return missing_clauses