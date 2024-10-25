import torch
import nltk
import bentoml
from transformers import AdamW, AutoTokenizer, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from Bio_Device_Classifier.pipeline import train
from Bio_Device_Classifier.entity import BERTClassifier, TextClassificationDataset
from Bio_Device_Classifier.utils import load_data
from Bio_Device_Classifier.constants import *
from Bio_Device_Classifier.logging import logger

nltk.download("stopwords")

def train_model():
    # Load and preprocess the data
    texts, labels = load_data(DATA_FILE_PATH)

    # Split the data for local BERT model training
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    # Tokenizer and Dataset for local BERT
    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)
    train_dataset = TextClassificationDataset(train_texts, train_labels, tokenizer, MAX_LENGTH)
    val_dataset = TextClassificationDataset(val_texts, val_labels, tokenizer, MAX_LENGTH)

    # DataLoader for local BERT model
    train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_dataloader = torch.utils.data.DataLoader(val_dataset, batch_size=BATCH_SIZE)

    # Model, Optimizer, and Scheduler for local BERT model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = BERTClassifier(BERT_MODEL_NAME, NUM_CLASSES).to(device)
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE)
    total_steps = len(train_dataloader) * NUM_EPOCHS
    scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)

    # Training loop for local BERT model
    for epoch in range(NUM_EPOCHS):
        logger.info(f"Epoch {epoch + 1}/{NUM_EPOCHS}")
        train(model, train_dataloader, optimizer, scheduler, device)

    # Save the local BERT model
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    logger.info(f"Model saved to {MODEL_SAVE_PATH}")

    tag=bentoml.pytorch.save_model("bert_classifier", model)
    logger.info(f"Model saved to bentoml{tag}")
    
    return model, val_dataloader, device  # Return for evaluation
