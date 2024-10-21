import bentoml
from transformers import AutoTokenizer
from Bio_Device_Classifier.constants import BERT_MODEL_NAME
from Bio_Device_Classifier.logging import logger

# Global variables for tokenizer and model_runner
tokenizer = None
model_runner = None

# Create the BentoML service and initialize the model
def initialize_service():
    global model_runner  # Declare model_runner as global
    global tokenizer      # Declare tokenizer as global

    # Initialize the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)

    try:
        model_runner = bentoml.pytorch.get("bert_classifier:latest").to_runner()
        print(f"Model runner initialized: {model_runner is not None}")
        model_runner.init_local()
        print(f"Model runner initialized: {model_runner is not None}")
        logger.info("Model runner initialized successfully.")
    except Exception as e:
        logger.info(f"Error initializing model runner: {e}")
        model_runner = None
    
    return tokenizer, model_runner

# Call the function to initialize the service once
initialize_service()