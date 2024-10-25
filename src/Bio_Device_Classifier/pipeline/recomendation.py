import nltk
import pandas as pd
from Bio_Device_Classifier.embedding import get_embeddings
from Bio_Device_Classifier.utils import pinecone_utils
from Bio_Device_Classifier.constants import INDEX_NAME

nltk.dowmload("stopwords")

def query_similar_embeddings(input_text):
    pc = pinecone_utils.initialize_pinecone()
    
    index = pc.Index(INDEX_NAME)
    
    # Get the embedding for the input text
    embedding = get_embeddings(input_text)
    
    # Query Pinecone for the top K similar embeddings
    query_result = index.query(vector=embedding.tolist(), top_k=10, include_metadata=True)
    
    # Retrieve metadata of nearest neighbors
    metadata = [match['metadata'] for match in query_result['matches']]

    return metadata
    