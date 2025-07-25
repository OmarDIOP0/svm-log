import os
import pickle
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from . import tests

# Téléchargements NLTK
nltk.download('stopwords')
nltk.download('wordnet')

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'svm_pipeline_model.pkl')

import joblib
...
def load_model():
    print(f"Attempting to load model from: {MODEL_PATH}")
    print(f"File exists: {os.path.exists(MODEL_PATH)}")
    print(f"File size: {os.path.getsize(MODEL_PATH)} bytes")
    
    try:
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def preprocess_text(text):
    """Prétraitement du texte pour l'analyse"""
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    # Nettoyage du texte
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = [lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]
    return ' '.join(tokens)

def parse_log_file(file):
    """Parse un fichier de logs CSV simple et retourne un DataFrame"""
    logs = []
    
    # Lire tout le contenu (bytes) et décoder en texte
    content = file.read()
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        text = content.decode('latin1')  # fallback si UTF-8 échoue
    
    lines = text.splitlines()
    
    # On saute la première ligne (header)
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(',', 1)
        if len(parts) < 2:
            continue
        
        category, message = parts
        message = message.strip()
        
        # Extraire IP
        ip_match = re.search(r'\d{1,3}(?:\.\d{1,3}){3}', message)
        ip = ip_match.group(0) if ip_match else '0.0.0.0'
        
        # Extraire username
        user_match = re.search(r'user\s+([\w\-]+)', message, re.IGNORECASE)
        username = user_match.group(1) if user_match else None
        
        logs.append({
            'raw_log': line,
            'category': category,
            'message': message,
            'source_ip': ip,
            'username': username,
        })
    
    df = pd.DataFrame(logs)
    df['clean_log'] = df['message'].apply(preprocess_text)
    
    return df

