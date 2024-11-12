import bentoml
import os
from transformers import AutoTokenizer
from bentoml import SyncHTTPClient
from Bio_Device_Classifier.constants import BERT_MODEL_NAME
from Bio_Device_Classifier.logging import logger

# Global variables for tokenizer and model_runner
tokenizer = None
model_runner = None
client = None
svc = None

# Create the BentoML service and initialize the model
def initialize_service():
    global model_runner  # Declare model_runner as global
    global tokenizer      # Declare tokenizer as global
    global client     # Declare client as global
    global svc

    # # Initialize the tokenizer
    # tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)

    # try:
    #     # Initialize SyncHTTPClient pointing to the BentoML server
    #     client = SyncHTTPClient('http://localhost:3000')
    #     logger.info("BentoML SyncHTTPClient initialized successfully.")
    # except Exception as e:
    #     logger.info(f"Error initializing BentoML SyncHTTPClient: {e}")
    #     client = None
    
    # return tokenizer, client

    try:
        model_runner = bentoml.pytorch.get("bert_classifier:latest").to_runner()
        print(f"Model runner initialized: {model_runner is not None}")
        
        # Create the BentoML service
        svc = bentoml.Service("bert_classifier_service", runners=[model_runner])

        os.system("bentoml serve pipeline/prediction:svc --reload")
        
        logger.info("SVC initialized successfully.")
    except Exception as e:
        logger.info(f"Error initializing service: {e}")
        model_runner = None
    
    return tokenizer, model_runner, svc

# Call the function to initialize the service once
initialize_service()