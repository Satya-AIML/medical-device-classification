# utils.py

import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from Bio_Device_Classifier.constants import *

STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    """Cleans the input text by removing special characters and stopwords."""
    text = text.lower()
    text = re.sub(REPLACE_BY_SPACE_RE, ' ', text)
    text = re.sub(BAD_SYMBOLS_RE, '', text)
    text = ' '.join([word for word in text.split() if word not in STOPWORDS])
    return text

def load_data(data_file):
    df = pd.read_csv(data_file)
    df = df.dropna(subset=['Name of Device', 'Intended Use'])
    df['merged'] = df['Name of Device'] + ' ' + df['Intended Use']
    df = df.dropna(subset=['merged', 'Class'])
    df = df[df['Class'].isin(SPECIFIED_TAGS)]
    df['merged'] = df['merged'].apply(clean_text)
    texts = df['merged'].tolist()
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(df['Class'])
    return texts, labels
