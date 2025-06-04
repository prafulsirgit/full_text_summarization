import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MODEL_DIR = os.path.join(BASE_DIR, 'fine_tuned_models')
CNN_DAILYMAIL_PATH = os.path.join(BASE_DIR, 'datasets', 'cnn_dailymail', 'train.csv')
BILLSUM_PATH = os.path.join(BASE_DIR, 'datasets', 'billsum_v4_1', 'us_train_data_final_OFFICIAL.jsonl')

# Flask settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB Max size of the file it accept

# Model settings
PEGASUS_MODEL_NAME = "google/pegasus-xsum"
BERT_MODEL_NAME = "bert-base-uncased"
LEGALBERT_MODEL_NAME = "nlpaueb/legal-bert-base-uncased"

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Suppress transformers warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
