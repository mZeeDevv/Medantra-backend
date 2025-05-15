from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from typing import List
from pydantic import BaseModel
import os
from google import genai
from dotenv import load_dotenv

# Inline minimal schema to reduce dependencies
class QuestionRequest(BaseModel):
    question: str
    user_id: str

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

# Initialize API clients with environment variables
genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Create FastAPI app with optimized imports
app = FastAPI(title="Vision RAG API - Ask Endpoint")

# Only import heavy modules when needed
def get_embedding_service():
    from app.services.embedding_service import compute_query_embedding
    return compute_query_embedding

def get_qdrant_service():
    from app.services.qdrant_service import search_user_embeddings, ensure_collection_exists
    ensure_collection_exists()
    return search_user_embeddings

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# ----- Ask Question -----
@app.post("/ask")
def ask_question(payload: QuestionRequest):
    try:
        # Get services only when needed
        compute_query_embedding = get_embedding_service()
        search_user_embeddings = get_qdrant_service()
        
        query_embedding = compute_query_embedding(payload.question)
        results = search_user_embeddings(payload.user_id, query_embedding)

        context = "\n".join([f"[Image {i.id} metadata: {i.payload}]" for i in results])
        prompt = f"{context}\n\nQ: {payload.question}\nA:"

        response = genai_client.models.generate_content(
            model="gemini-2.0-flash", # Using 2.0-flash instead of 2.5-preview to reduce dependencies
            contents=prompt
        )
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add handler for Vercel serverless function
handler = app
