import customtkinter as ctk
from PIL import Image
import os

def load_player_image(path, width, height):

    if not os.path.exists(path):
        path = "AI_UI_NBA_Player_Images_67/Blank.png"

    return ctk.CTkImage(
        light_image=Image.open(path),
        dark_image=Image.open(path),
        size=(width, height)
    )


def team_to_dataframe(team):
    import pandas as pd

    data = {
        "weight": [],
        "height": [],
        "age": []
    }

    for player in team:
        data["weight"].append(player.weight)
        data["height"].append(player.height)
        data["age"].append(player.age)

    return pd.DataFrame(data)