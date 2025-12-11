import joblib
MODEL_SAVE_PATH = "best_model.joblib"
class Team_Estimator:
    def __init__(self):
        import model_experiments
        from pathlib import Path
        if Path(MODEL_SAVE_PATH).is_file() is not True:
            print("model not found, training best model...")
            model_experiments.update_best_model(MODEL_SAVE_PATH)
            
        print("Loading best trained model...")
        self.model = joblib.load(MODEL_SAVE_PATH)
    #ensure a nd array or dataframe is passed in as team not a 1-d array
    #team can be a 2d - ndarray of shape, by 2, or dataframe
    def predict_binaries(self, team):
        return self.model.predict(team)
    
    #ensure a nd array or dataframe is passed in as team not a 1-d array
    def predict_score(self, team):
        return self.model.predict_proba(team)[:, list(self.model.classes_).index(1)]
    
