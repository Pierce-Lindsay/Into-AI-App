import customtkinter as ctk
from PIL import Image
import os
import utils
from Player import Player
import model.team_evaluator as team_evaluator

class TeamSummary(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.pack(fill="both", expand=True)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        # A frame to hold everything else and ensure everything is centered
        big_frame = ctk.CTkFrame(self, fg_color="transparent")
        big_frame.pack(anchor="center", padx=0, pady=0)

        label = ctk.CTkLabel(big_frame, text="Estimated Win %: (Need More Players)", font=("Arial", 40, "bold"))
        label.pack(pady=(5,0), anchor = "w", padx = 0)

        self.player_count = ctk.CTkLabel(big_frame, text="Players: " + str(len(self.master.team)) + f"/{self.master.MAX_TEAM_SIZE}",
                                         font=("Arial", 40, "bold"))
        self.player_count.pack(pady=(5, 0), anchor="w", padx=0)

        # A scrollable frame so the user can scroll through and view all of their players
        self.scroll_frame = ctk.CTkScrollableFrame(big_frame, width=800, height=1000)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(20, 0))

        # For each player in the user's team, display their information
        for player in self.master.team:
            self.add_player_box(
                player=player
            )

        # A button to allow the user to add a new player
        add_player_button = ctk.CTkButton(self.scroll_frame, text="Add Player", font=("Arial", 20), fg_color="#009000",
                                          border_color="black", border_width=5, corner_radius=0,
                                          command=master.show_page1, width=130, height=60)
        add_player_button.pack(padx=(0, 0), pady=10, anchor="e")

        #A button to predict the win percentage of the current team
        predict_button = ctk.CTkButton(self.scroll_frame, text="Predict Win %", font=("Arial", 20), fg_color="#000090",
                                       border_color="black", border_width=5, corner_radius=0,
                                       command=lambda big_frame=big_frame: self.predict_win_percentage(big_frame),
                                       width=180, height=60)
        predict_button.pack(padx=(0, 0), pady=(0, 20), anchor="e")

    def add_player_box(self, player):
        """ Used to add a box containing the player's information to the page """

        # A box that holds the player's picture, name, and age
        box_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#B0B050", border_color="black", border_width=5,
                                 corner_radius=0,
                                 width=800, height=130)
        box_frame.pack(padx=0, pady=(0, 0))
        box_frame.pack_propagate(False)

        player_label = ctk.CTkLabel(box_frame, image=utils.load_player_image(player.image_path, 175, 127), text="",
                                    fg_color="transparent")
        player_label.pack(side="left", padx=5, pady=(5, 6))

        player_info_frame = ctk.CTkFrame(box_frame, fg_color="#B0B050", border_color="black", border_width=0,
                                         corner_radius=0, width=240, height=57)
        player_info_frame.pack(side="left", padx=(20, 0), pady=20)
        player_info_frame.pack_propagate(False)

        player_name = ctk.CTkLabel(player_info_frame, fg_color="transparent", text=player.player_name, font=("Arial", 20))
        player_name.pack(anchor="w")

        """
        player_age = ctk.CTkLabel(player_info_frame, fg_color="transparent", text="Age: " + str(player.age),
                                  font=("Arial", 20))
        player_age.pack(anchor="w")
        """

        # The user can view the stats for the player or remove them from the team
        stats_button = ctk.CTkButton(box_frame, text="View Stats", font=("Arial", 20), fg_color="#900090",
                                     border_color="black", border_width=5, corner_radius=0,
                                     command=lambda player=player, incoming="Team Summary": self.master.view_stats(
                                         player, incoming),
                                     width=130, height=60)
        stats_button.pack(side="left", padx=(20, 0), pady=10)

        remove_button = ctk.CTkButton(box_frame, text="Remove", font=("Arial", 20), fg_color="#900000",
                                      border_color="black", border_width=5, corner_radius=0,
                                      command=lambda player=player, box=box_frame: self.remove_player(player, box),
                                      width=130,
                                      height=60)
        remove_button.pack(side="left", pady=10, padx=(40, 0))

    def add_player(self, player):
        """ Used to add a new player to the team """

        # If the length is too high, print it to the terminal
        if len(self.master.team) >= self.master.MAX_TEAM_SIZE:
            print("CANT ADD ANOTHER PLAYER MORON!")
        else:
            # Add the player to the team and update the on-screen player count
            self.master.team.append(player)
            self.player_count.configure(text="Players: " + str(len(self.master.team)) + f"/{self.master.MAX_TEAM_SIZE}")

            # Add a new box for the new player
            self.add_player_box(
                player=player
            )

    def remove_player(self, player, box):
        """ Used to remove a player from the team
            player: The player to remove from the team
            box: The box holding the player's information
        """
        self.master.team.remove(player)
        self.player_count.configure(text="Players: " + str(len(self.master.team)) + f"/{self.master.MAX_TEAM_SIZE}")

        #Remove the player's box
        box.destroy()

    def predict_win_percentage(self, big_frame):
        # """ Used to predict the win percentage of the current team """

        if len(self.master.team) >= 8:
            print("called")
        
            #Convert the team to a DataFrame for prediction
            team_data = utils.team_to_dataframe(self.master.team)
        
            win_probability = self.master.estimator.predict_score(team_data)[0]
        
            win_percentage = round(win_probability * 100, 2)
            print(f"Predicted Win %: {win_percentage}%")

            #Update the label showing the estimated win percentage
            for widget in big_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Estimated Win %" in widget.cget("text"):
                    widget.configure(text="Estimated Win %: " + str(win_percentage) + "%")
                    break

        else:
            for widget in big_frame.winfo_children():
                if isinstance(widget, ctk.CTkLabel) and "Estimated Win %" in widget.cget("text"):
                    widget.configure(text="Estimated Win %: (Need More Players)")
                    break
