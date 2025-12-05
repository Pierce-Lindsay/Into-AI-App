import customtkinter as ctk
from PIL import Image
import os
import utils

class PlayerProfile(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True)

        #Whichever page the user came from is the one they should return to if they hit "Back"
        self.incoming_page = "Team Summary"

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        back_button = ctk.CTkButton(self, text="Back", font = ("Arial", 20), fg_color = "#900090", border_color = "black", border_width = 5, corner_radius = 0, command = lambda : self.go_back(), width = 130, height = 60)
        back_button.pack(padx=(5,0), pady=(5,0), anchor = "w")

        self.player_name = ctk.CTkLabel(self, text="Lebron James", font=("Arial", 50, "bold"))
        self.player_name.pack(pady=0, anchor = "w", padx=25)

        #Holds both the image and the player info
        info_holder = ctk.CTkFrame(self, fg_color="transparent", width=1000, height=1000)
        info_holder.pack(anchor = "w", padx=0, pady=0)

        #The box which holds the player image
        box_frame = ctk.CTkFrame(info_holder, fg_color="#D0D0D0", border_color="black", border_width=5, corner_radius=0, width = 360, height = 264)
        box_frame.pack(side = "left", padx=20, pady=0)
        box_frame.pack_propagate(False)

        #NOTE: Info defaults to info for LeBron James but will be overridden when the user actually views the stats for a player
        player_path = "AI_UI_NBA_Player_Images_67/Lebron James.png"
        self.player_label = ctk.CTkLabel(box_frame, image=utils.load_player_image(player_path, 350, 254), text = "")
        self.player_label.pack(side = "left", padx=5, pady=5)

        player_info_frame = ctk.CTkFrame(info_holder, fg_color="transparent", border_color="black", border_width=0,
                                         corner_radius=0, width=200, height=100)
        player_info_frame.pack(side="left", padx=20, pady=20)
        player_info_frame.pack_propagate(False)

        self.player_age = ctk.CTkLabel(player_info_frame, fg_color="transparent", text="Age: 40", font=("Arial", 20))
        self.player_age.pack(anchor="w")

        self.player_height = ctk.CTkLabel(player_info_frame, fg_color="transparent", text="Height: 6\'9\"", font=("Arial", 20))
        self.player_height.pack(anchor="w")

        self.player_weight = ctk.CTkLabel(player_info_frame, fg_color="transparent", text="Weight: 250 lbs", font=("Arial", 20))
        self.player_weight.pack(anchor="w")

    def set_incoming_page(self, incoming_page):
        self.incoming_page = incoming_page

    def load_player(self, player):
        """ Used to override the current elements with the correct player information """

        self.player_name.configure(text=player.name)
        self.player_age.configure(text=f"Age: {player.age}")

        #If the height or weight are illegitimate, just list them as Unknown
        if player.height_ft <= -1:
            self.player_height.configure(text="Height: Unknown")
        else:
            self.player_height.configure(text=f"Height: {player.height_ft}\'{player.height_inch}\"")

        if player.weight <= -1:
            self.player_weight.configure(text="Weight: Unknown")
        else:
            self.player_weight.configure(text=f"Weight: {player.weight}")

        self.player_label.configure(image=utils.load_player_image(player.image_path, 350, 254))

    def go_back(self):
        """ Used to return to the previous page. This might be either the Team Summary page or the Add Player page """

        if self.incoming_page == "Team Summary":
            self.master.show_page3()
        else:
            self.master.show_page1()