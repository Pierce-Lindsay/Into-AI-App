import customtkinter as ctk
from PIL import Image
import os
import utils

class TeamSummary(ctk.CTkFrame):
    def __init__(self, master, show_page1_callback, show_page2_callback):
        super().__init__(master)
        self.pack(fill="both", expand=True)


        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        big_frame = ctk.CTkFrame(self, fg_color="transparent")
        big_frame.pack(anchor = "center", padx = 0, pady = 0)

        #Maybe make this label and everything else contained with in the same element so padding is easier
        label = ctk.CTkLabel(big_frame, text="Estimated Win %: (Need More Players)", font=("Arial", 40, "bold"))
        label.pack(pady=(5,0), anchor = "w", padx = 0)

        player_count = ctk.CTkLabel(big_frame, text="Players: 3/15", font=("Arial", 40, "bold"))
        player_count.pack(pady=(5, 0), anchor="w", padx=0)

        self.add_player_box(
            big_frame = big_frame,
            image_path="AI_UI_NBA_Player_Images_67/Sam_Hauser.png",
            player_name="Sam Hauser",
            player_age=27,
            command=show_page2_callback
        )

        self.add_player_box(
            big_frame=big_frame,
            image_path="AI_UI_NBA_Player_Images_67/Lebron_James.png",
            player_name="Lebron James",
            player_age=40,
            command=show_page2_callback
        )

        self.add_player_box(
            big_frame=big_frame,
            image_path="AI_UI_NBA_Player_Images_67/Keon_Ellis.png",
            player_name="Keon Ellis",
            player_age=25,
            command=show_page2_callback
        )

        back_to_team_button = ctk.CTkButton(big_frame, text="Add Player", font=("Arial", 20), fg_color="#009000",
                                            border_color="black", border_width=5, corner_radius=0,
                                            command=show_page1_callback, width=130, height=60)
        back_to_team_button.pack(padx=0, pady=10, anchor="e")

    def filter(self):
        print("67!")

    def add_to_team(self):
        print("Add the player to the team!")

    def view_stats(self):
        print("View this guy's stats!")

    def remove_player(self):
        print("REMOVE THE PLAYER!")

    def add_player_box(self, big_frame, image_path, player_name, player_age, command):

        box_frame = ctk.CTkFrame(big_frame, fg_color="#D0D0D0", border_color="black", border_width=5, corner_radius=0,
                                 width=800, height=130)
        box_frame.pack(padx=0, pady=(0, 0))
        box_frame.pack_propagate(False)

        player_label = ctk.CTkLabel(box_frame, image=utils.load_player_image(image_path, 175, 127), text="",
                                    fg_color="transparent")
        player_label.pack(side="left", padx=5, pady=(5, 6))

        player_info_frame = ctk.CTkFrame(box_frame, fg_color="#D0D0D0", border_color="black", border_width=0,
                                         corner_radius=0, width=130, height=57)
        player_info_frame.pack(side="left", padx=20, pady=20)
        player_info_frame.pack_propagate(False)

        hauser_name = ctk.CTkLabel(player_info_frame, fg_color="transparent", text=player_name, font=("Arial", 20))
        hauser_name.pack(anchor="w")

        hauser_age = ctk.CTkLabel(player_info_frame, fg_color="transparent", text="Age: " + str(player_age), font=("Arial", 20))
        hauser_age.pack(anchor="w")

        stats_button = ctk.CTkButton(box_frame, text="View Stats", font=("Arial", 20), fg_color="#900090",
                                     border_color="black", border_width=5, corner_radius=0, command=command,
                                     width=130, height=60)
        stats_button.pack(side="left", padx=(70, 0), pady=10)

        remove_button = ctk.CTkButton(box_frame, text="Remove", font=("Arial", 20), fg_color="#900000",
                                   border_color="black", border_width=5, corner_radius=0, command=self.remove_player(),
                                   width=130,
                                   height=60)
        remove_button.pack(side="left", pady=10, padx=(70, 0))



