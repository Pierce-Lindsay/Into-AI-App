from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, matthews_corrcoef
import model.models as models
import joblib

def update_best_model(model_save_path = "best_model.joblib"):
    EXPER_SIZE = 0.01
    EXPERIMENTING = True
    RANDOM_STATE = 1
    TRAIN_SIZE = 0.8
    print("reading in csv...")
    # resolve CSV path relative to repository root (one level up from /model/)
    # resolve CSV path relative to repository root (one level up from /model/)
    repo_root = Path(__file__).resolve().parents[1]
    data_file = repo_root / "data" / "player_stats_per_game.csv"
    if not data_file.is_file():
        raise FileNotFoundError(
            f"Data file not found at {data_file}\n"
            "Ensure 'player_stats_per_game.csv' exists in the repo 'data/' folder or run the app from the repo root."
        )
    data_frame = pd.read_csv(data_file)
    #clean up zero or NAN columns
    print("cleaning csv...")
    data_frame = data_frame.drop(data_frame.columns[0], axis = 1)

    Y = np.array(data_frame["GAME_WON"]) # grab labels
    data_frame = data_frame.drop(["GAME_WON"], axis= 1)
    #average 0 values in columns later???? must be missing values, how can be 0???
    X = pd.DataFrame(data_frame)

    if EXPERIMENTING:
        X, X_excluded, Y, Y_excluded = train_test_split(
        X, Y,             
        test_size=1-EXPER_SIZE,    
        train_size=EXPER_SIZE,   
        random_state=RANDOM_STATE,  
        shuffle=True     
        )
        
    X_train, X_test, Y_train, Y_test= train_test_split(
        X, Y,             
        test_size=1-TRAIN_SIZE,    
        train_size=TRAIN_SIZE,   
        random_state=RANDOM_STATE,  
        shuffle=True     
        )

    models_to_test= [models.SVM(X_train, Y_train),
                models.KNeighbors(X_train, Y_train), 
                models.DecisionTree(X_train, Y_train),
                models.LogRegression(X_train, Y_train)]
    print("Training models...")  
    #optimize models
    for model in models_to_test:
        model.optimize()

    #print out table 1 data
    print("Table 1: ")
    print("Model: Best Perameters : MCC Score")
    for model in models_to_test:
        model.print_best_from_optimize()

    #print out table 2 data
    print("Table 2: ")
    print("Model: Best Perameters : MCC Score")
    for model in models_to_test:
        model.update_best_predictions(X_test, Y_test)
        
     #find best score
    max_model = max(models_to_test, key=lambda m: m.test_score)
    print("Best model that should be used in the future:")
    print(f"{max_model.name}: with test MCC: {max_model.test_score}!")
    
    joblib.dump(max_model.best_model, model_save_path)
    
    
#update_best_model()