import torch
from transformers import AutoTokenizer, AutoModel
from Bio_Device_Classifier.constants import BERT_MODEL_NAME

def load_embeddings(model_name=BERT_MODEL_NAME):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    return tokenizer, model, device


def get_embeddings(text):
    tokenizer, model, device = load_embeddings()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=768)
    # Move inputs to the appropriate device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = model(**inputs)
    embeddings = torch.mean(outputs.last_hidden_state, dim=1).detach().cpu().numpy().squeeze()
    return embeddings

