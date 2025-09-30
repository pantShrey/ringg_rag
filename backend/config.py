import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load API keys
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")