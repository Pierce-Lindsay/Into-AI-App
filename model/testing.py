import team_evaluator
import model_experiments
import pandas as pd
import numpy as np

def main():
    #experimenting with evaluator
    print("reading in csv...")
    data_frame = pd.read_csv("data/player_stats_per_game.csv")
    #clean up zero or NAN columns
    print("cleaning csv...")
    data_frame = data_frame.drop(data_frame.columns[0], axis = 1)
    data_frame = data_frame[(data_frame.fillna(0) != 0).any(axis=1)]

    Y = np.array(data_frame["GAME_WON"]) # grab labels
    data_frame = data_frame.drop(["GAME_WON"], axis= 1)
    data_frame = model_experiments.average_zero_vals(data_frame)
    #average 0 values in columns later???? must be missing values, how can be 0???
    X = pd.DataFrame(data_frame)
    estimator = team_evaluator.Team_Estimator()
    print("testing some predictions...")

    print(estimator.predict_score(X.head()))
    
if __name__ == "__main__":
    main()