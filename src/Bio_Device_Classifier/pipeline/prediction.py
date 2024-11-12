# File: pipeline/prediction.py
import os
import bentoml
from bentoml.io import JSON
import torch
from transformers import AutoTokenizer
from Bio_Device_Classifier.constants import BERT_MODEL_NAME
from Bio_Device_Classifier.logging import logger

# Initialize tokenizer and model runner
tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)
model_runner = bentoml.pytorch.get("bert_classifier:latest").to_runner()

# Define the BentoML service
svc = bentoml.Service("bert_classifier_service", runners=[model_runner])

os.system("bentoml serve prediction.py:svc --reload")

@svc.api(input=JSON(), output=JSON())
def predict(input_data):
    # Extract and preprocess input
    text = input_data.get("text")
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True)

    # Run prediction
    outputs = model_runner.run(inputs["input_ids"], inputs["attention_mask"])
    _, preds = torch.max(outputs, dim=1)
    predicted_class = preds.item()  # Assuming a single prediction for simplicity

    return {"predicted_class": predicted_class}
