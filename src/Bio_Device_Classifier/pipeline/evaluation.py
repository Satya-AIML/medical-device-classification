import torch
from Bio_Device_Classifier.pipeline import evaluate
from Bio_Device_Classifier.logging import logger
from Bio_Device_Classifier.constants import MODEL_SAVE_PATH


def evaluate_model(model, val_dataloader, device):
    # Evaluate the trained model
    accuracy, report = evaluate(model, val_dataloader, device)
    logger.info(f"Validation Accuracy: {accuracy:.4f}")
    logger.info(f"\n{report}")
    return accuracy, report
