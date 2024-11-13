# constants/__init__.py

REPLACE_BY_SPACE_RE = r'[/(){}\[\]\|@,;]'
BAD_SYMBOLS_RE = r'[^0-9a-z #+_]'
STOPWORDS = set(["english"])
SPECIFIED_TAGS = ['Class A', 'Class B', 'Class C', 'Class D']
BERT_MODEL_NAME = 'emilyalsentzer/Bio_ClinicalBERT'
NUM_CLASSES = 4
MAX_LENGTH = 128
BATCH_SIZE = 16
NUM_EPOCHS = 1
LEARNING_RATE = 2e-5
TEST_SIZE = 0.2
RANDOM_STATE = 42
DATA_FILE_PATH = "ImageGen.csv"
MODEL_SAVE_PATH = "bert_classifier_best_version.pth"
INDEX_NAME = 'mdc'
IMAGES_DIR = "/home/rajvs/Medical-Device-Classification/Generated_Images"
GENERATED_RESPONSE = "/home/rajvs/Medical-Device-Classification/output_generated_responses.json" 
