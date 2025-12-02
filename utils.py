import customtkinter as ctk
from PIL import Image

def load_player_image(path, width, height):
    return ctk.CTkImage(
        light_image=Image.open(path),
        dark_image=Image.open(path),
        size=(width, height)
    )