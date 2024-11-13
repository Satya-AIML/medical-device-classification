# src/Bio_Device_Classifier/utils/pinecone_utils.py

from collections import Counter
from tqdm import tqdm
import pinecone
import pandas as pd
from Bio_Device_Classifier.utils.config_loader import load_config
from Bio_Device_Classifier.embedding import get_embeddings
from Bio_Device_Classifier.constants import INDEX_NAME
from Bio_Device_Classifier.logging import logger

def create_index_func(pc, index_name):
    """Creates a Pinecone index with the specified parameters."""
    logger.info(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=768,
        metric='cosine',
        spec=pinecone.ServerlessSpec(  # Updated to match correct import
            cloud='aws',
            region='us-east-1'
        )
    )
    logger.info(f"Index '{index_name}' created successfully.")

def initialize_pinecone():
    config = load_config()
    api_key = config['PINECONE']['PINECONE_API_KEY']
    Pinecone = pinecone.Pinecone(api_key=api_key)  
    return Pinecone

def check_and_recreate_index(pc, index_name, create_index_func):
    """
    Checks if a Pinecone index exists, and if it contains records, recreates the index.
    If the index does not exist, it creates a new one.
    
    Args:
        pc: The Pinecone client.
        index_name (str): The name of the index to check or create.
        create_index_func (function): The function to call for creating a new index.
    """
    # Check if the index exists
    if index_name in pc.list_indexes():
        # Get the index object
        index = pc.Index(index_name)
        
        # Get the current number of records in the index
        record_count = index.describe_index_stats()['total_vector_count']
        
        if record_count > 0:
            logger.info(f"Index '{index_name}' exists and has {record_count} records. Recreating the index...")
            pc.delete_index(index_name)  # Delete the existing index
            logger.info(f"Index '{index_name}' deleted.")
            create_index_func(pc, index_name)  # Create a new index using the passed function
        else:
            logger.info(f"Index '{index_name}' exists but is empty. No action needed.")
    else:
        # Create a new index if it does not exist
        logger.info(f"Index '{index_name}' does not exist. Creating a new index...")
        create_index_func(pc, index_name)  # Create the new index using the passed function

def store_embeddings_to_pinecone(pc, index_name, train_data):
    index = pc.Index(index_name)

    logger.info("Upsert started.")
    
    total_rows = len(train_data)
    milestones = {25: False, 50: False, 75: False, 100: False}  # Track milestones
    
    with tqdm(total=total_rows, desc="Upserting embeddings", unit="rows") as pbar:
        for i, row in train_data.iterrows():
            text = row['NameOfDevice'] + ' ' + row['IntendedUse']
            embedding = get_embeddings(text)

            metadata = {
                'device_name': row['NameOfDevice'],
                'label': int(row['labels']),
                'index': int(row['index'])
            }

            index.upsert(vectors=[(str(i), embedding, metadata)])

            # Update progress bar
            pbar.update(1)

    logger.info("Upsert completed.")

def extract_column_names_from_metadata(metadata):
    """
    Dynamically extracts column names from metadata.
    
    Parameters:
    - metadata: A list of dictionaries containing metadata from Pinecone.

    Returns:
    - A list of column names inferred from the keys in the metadata.
    """
    # Check if metadata is not empty and extract column names from the first entry
    if metadata and isinstance(metadata, list):
        first_entry = metadata[0]  # Assuming all entries have the same structure
        return list(first_entry.keys())
    else:
        return []
    
def create_dataframe_from_metadata(metadata) -> pd.DataFrame:
    """
    Creates a pandas DataFrame from metadata, dynamically handling column names.
    
    Parameters:
    - metadata: The metadata returned from Pinecone.

    Returns:
    - A pandas DataFrame constructed from the metadata.
    """
    # Extract dynamic column names
    columns = extract_column_names_from_metadata(metadata)

    # If columns exist, create the DataFrame
    if columns:
        df = pd.DataFrame(metadata, columns=columns)
    else:
        df = pd.DataFrame()  # Empty DataFrame if no metadata
    
    return df
