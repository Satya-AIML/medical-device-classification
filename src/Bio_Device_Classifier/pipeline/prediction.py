# Import the from bentoml_utils.py initialization function

import torch
from Bio_Device_Classifier.utils import bentoml_utils
from Bio_Device_Classifier.utils.bentoml_utils import tokenizer, model_runner  # Import global variables
from Bio_Device_Classifier.constants import SPECIFIED_TAGS, MAX_LENGTH  # Import necessary constants

def prediction(input_data):
    # Check if model_runner is initialized
    if model_runner is None:
        raise ValueError("Model runner is not initialized. Please ensure the service is initialized.")

    # Get text input from the user
    text = input_data.get("text")

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt', max_length=MAX_LENGTH, padding='max_length', truncation=True)

    # Use model runner to make a prediction
    outputs = model_runner.run(inputs['input_ids'], inputs['attention_mask'])
    _, preds = torch.max(outputs, dim=1)

    # Convert prediction to class label
    predicted_class = SPECIFIED_TAGS[preds.item()]

    return {"predicted_class": predicted_class}

