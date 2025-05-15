import requests
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

def test_api(base_url="http://localhost:8000"):
    """
    Test the Vision RAG API endpoints
    """
    print(f"\nTesting API at {base_url}...\n")
    
    # Test the root endpoint
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print(f"✅ Root endpoint: {response.json()}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test the Cohere API key
    cohere_key = os.getenv("COHERE_API_KEY")
    if not cohere_key:
        print("❌ Missing COHERE_API_KEY environment variable")
    else:
        print(f"✅ COHERE_API_KEY is set")
    
    # Test the Google API key
    google_key = os.getenv("GOOGLE_API_KEY")
    if not google_key:
        print("❌ Missing GOOGLE_API_KEY environment variable")
    else:
        print(f"✅ GOOGLE_API_KEY is set")
    
    # Test the Qdrant connection
    qdrant_host = os.getenv("QDRANT_CLOUD_HOST")
    qdrant_key = os.getenv("QDRANT_CLOUD_API_KEY")
    if not qdrant_host or not qdrant_key:
        print("❌ Missing Qdrant environment variables")
    else:
        print(f"✅ Qdrant environment variables are set")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test the Vision RAG API")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the API")
    args = parser.parse_args()
    
    test_api(args.url)
