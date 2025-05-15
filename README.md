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

The project is configured to deploy as separate serverless functions to address Vercel's 250MB size limit.

### Standard Deployment

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

### Troubleshooting Size Limit Issues

If you encounter the 250MB size limit error, try these steps:

1. Increase the function timeout and memory in Vercel project settings:
   - Go to Settings > Functions
   - Set Max Duration to 60s
   - Set Memory to 1024MB

2. Use the optimized deployment with multiple serverless functions:
   - Each API endpoint is configured as a separate function
   - Each function has its own requirements file in the `api` directory
   - The PDF processing is limited to 5 pages per document to reduce memory usage

3. Check function size and logs:
   - After deployment, go to the Vercel dashboard
   - Check the Functions tab to see the size of each function
   - Examine logs for any memory or timeout issues

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