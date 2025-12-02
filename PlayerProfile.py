import customtkinter as ctk
from PIL import Image
import os
import utils

class PlayerProfile(ctk.CTkFrame):
    def __init__(self, master, show_page1_callback, show_page3_callback):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        back_to_team_button = ctk.CTkButton(self, text="Back to Team", font = ("Arial", 20), fg_color = "#900090", border_color = "black", border_width = 5, corner_radius = 0, command=show_page3_callback, width = 130, height = 60)
        back_to_team_button.pack(padx=0, pady=0, anchor = "w")


        player_name = ctk.CTkLabel(self, text="Lebron James", font=("Arial", 50, "bold"))
        player_name.pack(pady=0, anchor = "w", padx=25)

        info_holder = ctk.CTkFrame(self, fg_color="transparent", width=1000, height=1000)
        info_holder.pack(anchor = "w", padx=0, pady=0)

        box_frame = ctk.CTkFrame(info_holder, fg_color="#D0D0D0", border_color="black", border_width=5, corner_radius=0, width = 360, height = 264)
        box_frame.pack(side = "left", padx=20, pady=0)
        box_frame.pack_propagate(False)

        lebron_path = "AI_UI_NBA_Player_Images_67/Lebron_James.png"
        lebron_label = ctk.CTkLabel(box_frame, image=utils.load_player_image(lebron_path, 350, 254), text = "")
        lebron_label.pack(side = "left", padx=5, pady=5)





        lebron_info_frame = ctk.CTkFrame(info_holder, fg_color="transparent", border_color="black", border_width=0,
                                         corner_radius=0, width=200, height=100)
        lebron_info_frame.pack(side="left", padx=20, pady=20)
        lebron_info_frame.pack_propagate(False)

        lebron_age = ctk.CTkLabel(lebron_info_frame, fg_color="transparent", text="Age: 40", font=("Arial", 20))
        lebron_age.pack(anchor="w")

        lebron_height = ctk.CTkLabel(lebron_info_frame, fg_color="transparent", text="Height: 6\'9\"", font=("Arial", 20))
        lebron_height.pack(anchor="w")

        lebron_weight = ctk.CTkLabel(lebron_info_frame, fg_color="transparent", text="Weight: 250 lbs", font=("Arial", 20))
        lebron_weight.pack(anchor="w")




