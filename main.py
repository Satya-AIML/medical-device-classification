from Bio_Device_Classifier.pipeline.training import train_model
from Bio_Device_Classifier.pipeline.evaluation import evaluate_model
from Bio_Device_Classifier.config import config
from Bio_Device_Classifier.constants import *
from Bio_Device_Classifier.logging import logger

# Import Pinecone utilities and embedding functions
from Bio_Device_Classifier.data_processing import data_transform
from Bio_Device_Classifier.utils.pinecone_utils import initialize_pinecone, store_embeddings_to_pinecone

def main():

    logger.info("Model Training Started")

    # Train the model and get the validation dataloader
    model, val_dataloader, device = train_model()
    logger.info("Model Training Completed")

    # Evaluate the trained model
    evaluate_model(model, val_dataloader, device)
    logger.info("Embedding upsert Started")
    
    # Now integrate with Pinecone for embedding storage and retrieval
    # Initialize Pinecone
    pc = initialize_pinecone()

    # Load and preprocess the dataset for Pinecone
    pinecone_data = data_transform(DATA_FILE_PATH)

    # Store embeddings to Pinecone
    store_embeddings_to_pinecone(pc, INDEX_NAME, pinecone_data)
    logger.info("Embedding upsert Completed")

if __name__ == "__main__":
    main()
