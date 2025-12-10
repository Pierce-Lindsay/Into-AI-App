import joblib
import model.model_experiments as model_experiments
from pathlib import Path

MODEL_SAVE_PATH = "data/best_model.joblib"

class Team_Estimator:
    def __init__(self):
        if Path(MODEL_SAVE_PATH).is_file() is not True:
            print("model not found, training best model...")
            model_experiments.update_best_model(MODEL_SAVE_PATH)
            
        print("Loading best trained model...")
        self.model = joblib.load(MODEL_SAVE_PATH)

    def predict_binaries(self, team):
        return self.model.predict(team)
    
    def predict_score(self, team):
        return self.model.predict_proba(team)[:, list(self.model.classes_).index(1)]
    
