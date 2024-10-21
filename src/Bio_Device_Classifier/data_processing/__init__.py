import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt
from Bio_Device_Classifier.constants import REPLACE_BY_SPACE_RE, BAD_SYMBOLS_RE, STOPWORDS, SPECIFIED_TAGS


# Initialize STOPWORDS properly if it hasn't been initialized in constants.py
if STOPWORDS is None:
    STOPWORDS = set(stopwords.words('english'))

# Compile the regular expressions from constants
REPLACE_BY_SPACE_RE = re.compile(REPLACE_BY_SPACE_RE)  # From constants.py
BAD_SYMBOLS_RE = re.compile(BAD_SYMBOLS_RE)  # From constants.py

# Function to clean text
def clean_text(text):
    if isinstance(text, str):
        text = text.lower()  # Lowercase text
        text = REPLACE_BY_SPACE_RE.sub(' ', text)  # Replace unwanted symbols with space
        text = BAD_SYMBOLS_RE.sub('', text)  # Remove unwanted characters
    return text

def data_transform(data_file):
    """Loads and preprocesses the data based on the new CSV format, removing rows with null values."""
    df = pd.read_csv(data_file)
    specified_tags = ['Class A', 'Class B', 'Class C', 'Class D']
    
    # Remove rows with null values in 'Name of Device', 'Intended Use', or 'Class'
    df = df.dropna(subset=['Name of Device', 'Intended Use', 'Class'])
    
    # Filter the specified classes
    df = df[df['Class'].isin(specified_tags)]
    
    # Clean only the 'Intended Use' column
    df['Intended Use'] = df['Intended Use'].apply(clean_text)
    
    # Extract the 'Name of Device' and cleaned 'Intended Use'
    NameOfDevice = df['Name of Device'].tolist()
    IntendedUse = df['Intended Use'].tolist()
    
    # Encode labels
    label_encoder = LabelEncoder()
    Labels = label_encoder.fit_transform(df['Class'])
    
    # Extract the index as a list
    Index = df.index.tolist()

    data = pd.DataFrame({
        'NameOfDevice': NameOfDevice,
        'IntendedUse': IntendedUse,
        'labels': Labels,
        'index': Index
    })
    
    return data
