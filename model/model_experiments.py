import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import make_scorer, matthews_corrcoef, log_loss, auc, roc_auc_score, brier_score_loss
from sklearn.model_selection import cross_val_score, StratifiedKFold, cross_validate
from sklearn.metrics import (roc_curve, auc,
                             confusion_matrix, ConfusionMatrixDisplay)
from sklearn.calibration import calibration_curve
import matplotlib.pyplot as plt
import model.models as models
import joblib

def update_best_model(model_save_path = "best_model.joblib"):
    EXPER_SIZE = 0.5
    EXPERIMENTING = True
    RANDOM_STATE = 1
    TRAIN_SIZE = 0.8
    print("reading in csv...")
    data_frame = pd.read_csv("data/player_stats_per_game.csv")
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
        stratify=Y,
        shuffle=True     
        )
        
    X_train, X_test, Y_train, Y_test= train_test_split(
        X, Y,             
        test_size=1-TRAIN_SIZE,    
        train_size=TRAIN_SIZE,   
        random_state=RANDOM_STATE,  
        stratify=Y,
        shuffle=True     
        )

    models_to_test= [#models.SVM(X_train, Y_train),
                #models.KNeighbors(X_train, Y_train), 
                #models.DecisionTree(X_train, Y_train),
                #models.LogRegression(X_train, Y_train),
                models.XGB(X_train, Y_train)]
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

def full_train_best_known(model_save_path = "best_model.joblib"):
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from xgboost import XGBClassifier
    RANDOM_STATE = 1
    TRAIN_SIZE = 0.8
    print("reading in csv...")
    data_frame = pd.read_csv("data/player_stats_per_game.csv")
    #clean up zero or NAN columns
    print("cleaning csv...")
    data_frame = data_frame.drop(data_frame.columns[0], axis = 1)

    Y = np.array(data_frame["GAME_WON"]) # grab labels
    data_frame = data_frame.drop(["GAME_WON"], axis= 1)
    #average 0 values in columns later???? must be missing values, how can be 0???
    X = pd.DataFrame(data_frame)
        
    X_train, X_test, Y_train, Y_test= train_test_split(
        X, Y,             
        test_size=1-TRAIN_SIZE,    
        train_size=TRAIN_SIZE,   
        random_state=RANDOM_STATE,  
        stratify=Y,
        shuffle=True     
        )
    #create XGBoost with the specified perams
    #these are the hard coded best statistics found from grid search
    XGB = XGBClassifier(objective = 'binary:logistic', 
                              eval_metric= 'logloss',
                              learning_rate= 0.01,
                              max_depth = 3, 
                              n_estimators = 600,
                              random_state=RANDOM_STATE)
    #create pipeline for normalization
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", XGB)])
    #create scoring metrics we care about
    #we care most about los_loss, because we want accurate probabilities
    scoring={
        'logloss': 'neg_log_loss',
        'brier': 'neg_brier_score',
        'auc': 'roc_auc',
        'mcc': make_scorer(matthews_corrcoef, response_method='predict')}
    
    #cross validate train multithreaded
    results = cross_validate(pipe, X_train, Y_train, 
                         cv=models.CV, scoring=scoring, n_jobs=-1)
    
    #display results, formatting generation assisted by Claude for convenience
    print("Cross-Validation Results:")
    print(f"Log Loss: {-results['test_logloss'].mean():.4f} (+/- {results['test_logloss'].std():.4f})")
    print(f"Brier:    {-results['test_brier'].mean():.4f} (+/- {results['test_brier'].std():.4f})")
    print(f"AUC:      {results['test_auc'].mean():.4f} (+/- {results['test_auc'].std():.4f})")
    print(f"MCC:      {results['test_mcc'].mean():.4f} (+/- {results['test_mcc'].std():.4f})")
    #do actual fit now with full traning
    pipe.fit(X_train, Y_train) 

    #get predictions and corresponding probabilities
    probs = pipe.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)

    #compute metrics
    test_logloss = log_loss(Y_test, probs)
    test_auc = roc_auc_score(Y_test, probs)
    test_mcc = matthews_corrcoef(Y_test, preds)
    test_brier = brier_score_loss(Y_test, probs)
    
    #display results, formatting generation assisted by Claude for convenience
    print(f"\nTest Set Performance:")
    print(f"Log Loss: {test_logloss:.4f}")
    print(f"Brier Loss: {test_brier:.4f}")
    print(f"AUC: {test_auc:.4f}")
    print(f"MCC: {test_mcc:.4f}")
    
    
    #save graph pngs to help visualize, formatting assised by Calude for convenience
    
    # Get calibration data
    prob_true, prob_pred = calibration_curve(Y_test, probs, n_bins=10)

    plt.figure(figsize=(8, 6))
    plt.plot(prob_pred, prob_true, marker='o', linewidth=2, 
            label='Model', color='blue', markersize=8)
    plt.plot([0, 1], [0, 1], linestyle='--', color='gray', 
            label='Perfect Calibration')
    plt.xlabel('Predicted Probability')
    plt.ylabel('True Probability (Fraction of Positives)')
    plt.title('Calibration Curve')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig("plots/calibration_curve.png")
    plt.show()
    
    # Create confusion matrix
    cm = confusion_matrix(Y_test, preds, normalize='true')

    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, 
                                display_labels=['Loss', 'Win'])
    disp.plot(ax=ax, cmap='Blues', values_format='.2%')
    plt.title('Confusion Matrix')
    plt.savefig("plots/confusion_matrix.png")
    plt.show()
    
    # Calculate ROC curve
    fpr, tpr, thresholds = roc_curve(Y_test, probs)
    roc_auc = auc(fpr, tpr)

    # Plot
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
            label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
            label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.savefig("plots/ROC_curve.png")
    plt.show()
    
    joblib.dump(pipe, model_save_path)
    


#run this file to update best known model and display results
#full_train_best_known()