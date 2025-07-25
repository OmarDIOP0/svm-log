import os
import pickle

MODEL_PATH = os.path.join(os.path.dirname(__file__),'models','svm_pipeline_model.pkl')

def load_model():
    with open(MODEL_PATH,'rb') as file:
        model = pickle.load(file)
    return model