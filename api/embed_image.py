from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import sys
import os
from PIL import Image
import io, base64
import os
from google import genai
from dotenv import load_dotenv

# Add the parent directory to the Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

# Initialize API clients with environment variables
genai_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Create FastAPI app
app = FastAPI(title="Vision RAG API - Embed Image Endpoint")

# Only import heavy modules when needed
def ensure_collection_ready():
    from app.services.qdrant_service import ensure_collection_exists
    ensure_collection_exists()

# Call this once at initialization
ensure_collection_ready()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

# Image processing utility functions
def pil_to_base64(pil_image: Image.Image) -> str:
    MAX_PIXELS = 1568 * 1568
    # Resize if needed
    w, h = pil_image.size
    if w * h > MAX_PIXELS:
        scale = (MAX_PIXELS / (w * h)) ** 0.5
        pil_image = pil_image.resize((int(w * scale), int(h * scale)))
    
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    base64_img = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{base64_img}"

def describe_image_with_gemini(image: Image) -> str:
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image, "Caption this image in one sentence."],
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error in Gemini caption: {e}")
        return "Image without caption"

# ----- Embed Image -----
@app.post("/embed-image")
async def embed_image(file: UploadFile = File(...), user_id: str = Form(...)):
    try:
        # Import services only when needed to minimize cold start time
        from app.services.embedding_service import compute_image_embedding
        from app.services.qdrant_service import store_embedding
        
        image = Image.open(file.file)
        base64_img = pil_to_base64(image) 
        embedding = compute_image_embedding(base64_img)
        caption = describe_image_with_gemini(image)

        store_embedding(user_id, embedding, {
            "source": "image",
            "filename": file.filename,
            "caption": caption
        })
        return {"status": "stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add handler for Vercel serverless function
handler = app
