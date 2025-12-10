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