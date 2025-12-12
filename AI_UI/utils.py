import customtkinter as ctk
from PIL import Image
import os
import pandas as pd

def load_player_image(path, width, height):

    if not os.path.exists(path):
        path = "AI_UI/AI_UI_NBA_Player_Images_67/Blank.png"

    return ctk.CTkImage(
        light_image=Image.open(path),
        dark_image=Image.open(path),
        size=(width, height)
    )


def team_to_dataframe(team):
    """ Converts a list of Player objects into a pandas DataFrame suitable for model input """

    data = []

    feature_data_names = []
    feature_prefixes = [
        "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", 
        "FTM", "FTA", "FT_PCT", "OREB", "DREB", "REB", 
        "AST", "STL", "BLK", "TO", "PF", "PTS", "PLUS_MINUS"
    ]

    for i in range(8):
        for prefix in feature_prefixes:
            feature_data_names.append(prefix + str(i))
    
    for player in team:
        player_data = {
            "FGM": player.fgm,
            "FGA": player.fga,
            "FG_PCT": player.fg_pct,
            "FG3M": player.fg3m,
            "FG3A": player.fg3a,
            "FG3_PCT": player.fg3_pct,
            "FTM": player.ftm,
            "FTA": player.fta,
            "FT_PCT": player.ft_pct,
            "OREB": player.oreb,
            "DREB": player.dreb,
            "REB": player.reb,
            "AST": player.ast,
            "STL": player.stl,
            "BLK": player.blk,
            "TO": player.to,
            "PF": player.pf,
            "PTS": player.pts,
            "PLUS_MINUS": player.plus_minus
        }

        # Convert player_data from dict to list of values
        player_data = list(player_data.values())

        data.append(player_data)

    # Sort data by PLUS_MINUS (last element in each player's data)
    data.sort(key=lambda x: x[-1], reverse=True)

    team_df = pd.DataFrame(columns=feature_data_names)

    # Flatten the list of player data into a single list
    data = [item for sublist in data for item in sublist]

    print(data)

    team_df.loc[0] = data
    print(team_df)

    return team_df