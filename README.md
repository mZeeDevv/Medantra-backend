# Vision RAG

A multimodal RAG (Retrieval-Augmented Generation) system that processes images and PDFs, uses Cohere for embeddings, and Gemini for image understanding and question answering.

## Local Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vision-rag.git
cd vision-rag
```

2. Create a virtual environment and install dependencies:
```bash
# Using venv
python -m venv .venv
source .venv/Scripts/activate  # On Windows
# OR source .venv/bin/activate  # On Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys (see `.env.example` for required variables):
```
COHERE_API_KEY=your_cohere_api_key
GOOGLE_API_KEY=your_gemini_api_key
QDRANT_CLOUD_HOST=your_qdrant_cloud_host
QDRANT_CLOUD_API_KEY=your_qdrant_cloud_api_key
```

### Run Locally

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Vercel Deployment

1. Push your code to GitHub:
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push
```

2. Sign in to [Vercel](https://vercel.com) and create a new project:
   - Connect your GitHub account
   - Select the repository
   - Configure project:
     - Framework preset: Other
     - Root directory: ./
     - Build command: None
     - Output directory: None
   
3. Add environment variables:
   - Go to Project Settings > Environment Variables
   - Add all variables from your `.env` file
   
4. Deploy!

## API Endpoints

- `POST /embed-image`: Upload and embed an image
- `POST /embed-pdf`: Upload and embed a PDF document
- `POST /ask`: Ask a question about embedded content

## Technology Stack

- FastAPI: Web framework
- Cohere: Embeddings
- Google Gemini: Image understanding and question answering
- Qdrant: Vector database
- Vercel: Deployment platform