import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from config import WEAVIATE_URL, WEAVIATE_API_KEY, COHERE_API_KEY

def create_weaviate_client():
    """Create and configure a Weaviate client connection."""
    headers = {"X-Cohere-Api-Key": COHERE_API_KEY}
    
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        headers=headers
    )
    
    return client

def setup_collection(client):
    """Set up the Documents collection in Weaviate if it doesn't exist."""
    try:
        client.collections.create(
            "Documents",
            vectorizer_config=[
                Configure.NamedVectors.text2vec_cohere(
                    name="content_vector",
                    source_properties=["text_chunk"],
                    model="embed-multilingual-light-v3.0"
                )
            ]
        )
        print("Collection created successfully")
    except Exception as e:
        print(f"Collection already exists or error: {str(e)}")

# Initialize the client
client = create_weaviate_client()

# Set up the collection
setup_collection(client)

def get_client():
    """Get the Weaviate client instance."""
    return client

def close_client():
    """Close the Weaviate client connection."""
    client.close()