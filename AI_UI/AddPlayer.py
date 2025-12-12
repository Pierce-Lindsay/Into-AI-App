import customtkinter as ctk
from PIL import Image
import os
import utils
import pandas as pd
from Player import Player

class AddPlayer(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        #The number of potential players being displayed on screen at a time
        self.players_per_page = 8

        #Keeps track of which specific players are currently being displayed
        self.page_index = 0

        #A list of players to display after all filters have been applied
        self.filtered_players = self.master.all_players.copy()

        #The bounds on the filters applied
        self.fgm_lower_bound = 0

        self.fga_lower_bound = 0

        self.fg_pct_lower_bound = 0

        self.fg3m_lower_bound = 0

        self.fg3a_lower_bound = 0

        self.fg3_pct_lower_bound = 0

        self.ftm_lower_bound = 0

        self.fta_lower_bound = 0

        self.ft_pct_lower_bound = 0

        self.oreb_lower_bound = 0

        self.dreb_lower_bound = 0

        self.reb_lower_bound = 0

        self.ast_lower_bound = 0

        self.stl_lower_bound = 0

        self.blk_lower_bound = 0

        self.to_upper_bound = 100

        self.pf_upper_bound = 100

        self.pts_lower_bound = 0

        self.plus_minus_lower_bound = -100



        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        back_to_team_button = ctk.CTkButton(self, text="Back to Team", font=("Arial", 20), fg_color="#900090",
                                            border_color="black", border_width=5, corner_radius=0,
                                            command=master.show_page3, width=130, height=60)
        back_to_team_button.pack(padx=(5,0), pady=(5,0), anchor="w")

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=900, height=600)
        self.scroll_frame.pack(fill="both", expand=True)

        self.big_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", height = 3000)
        self.big_frame.pack(anchor = "center", padx = 0, pady = 0)

        label = ctk.CTkLabel(self.big_frame, text="ADD PLAYER", font=("Arial", 40, "bold"))
        label.pack(pady=(5,0), anchor = "w", padx = 0)

        #A row to hold the search bar and filters button
        search_row = ctk.CTkFrame(self.big_frame, fg_color = "transparent")
        search_row.pack(padx=(0,0), pady=(5,0), anchor = "center")

        #A search bar for the player to search for a specific player name
        self.player_name_entry = ctk.CTkEntry(search_row, placeholder_text="Search", font = ("Arial", 20), width = 640, height = 37, border_color = "black", border_width = 5, corner_radius = 0)
        self.player_name_entry.pack(side = "left", padx=5, pady=0)

        #When the user types something in the search bar, use their search to filter out players
        self.player_name_entry.bind("<KeyRelease>", lambda event: self.filter_players())

        self.filter_button = ctk.CTkButton(search_row, text="Add Filters", font = ("Arial", 20), border_color = "black", border_width = 5, corner_radius = 0, command=self.add_filters, width = 150, height = 30, fg_color = "#777777")
        self.filter_button.pack(side = "left", pady=0)

        #Contains the filters
        self.filter_container = ctk.CTkFrame(self.big_frame, fg_color="transparent", height = 0)
        self.filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")

        #These filters are not displayed until the user hits the "Add Filters" button

        self.fgm_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.fga_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.fg_pct_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.fg3m_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.fg3a_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.fg3_pct_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.ftm_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.fta_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.ft_pct_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.oreb_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.dreb_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.reb_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.ast_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.stl_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.blk_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.to_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)

        self.pf_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)
        self.pts_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)
        self.plus_minus_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)



        #The spaces for the user to enter the upper and lower bounds for each filter


        #Field Goals Made

        self.fgm_filter_entry_lower_bound = ctk.CTkEntry(self.fgm_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                         height=20, border_color="black", border_width=3, corner_radius=0)

        fgm_filter_label = ctk.CTkLabel(self.fgm_filter_container, text="Field Goals Made: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        fgm_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.fgm_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)


        #Field Goals Attempted

        self.fga_filter_entry_lower_bound = ctk.CTkEntry(self.fga_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                         height=20, border_color="black", border_width=3, corner_radius=0)

        fga_filter_label = ctk.CTkLabel(self.fga_filter_container, text="Field Goals Attempted: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        fga_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.fga_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Field Goal Percentage

        self.fg_pct_filter_entry_lower_bound = ctk.CTkEntry(self.fg_pct_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                         height=20, border_color="black", border_width=3, corner_radius=0)

        fg_pct_filter_label = ctk.CTkLabel(self.fg_pct_filter_container, text="Field Goal Percentage: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        fg_pct_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.fg_pct_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)



        #Field Goals Made from 3 Point Line

        self.fg3m_filter_entry_lower_bound = ctk.CTkEntry(self.fg3m_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                         height=20, border_color="black", border_width=3, corner_radius=0)

        fg3m_filter_label = ctk.CTkLabel(self.fg3m_filter_container, text="Field Goals Made from 3 Point Line: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        fg3m_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.fg3m_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Field Goals Attempted from 3 point line

        self.fg3a_filter_entry_lower_bound = ctk.CTkEntry(self.fg3a_filter_container, font=("Arial", 20), width=40,
                                                            placeholder_text="0",
                                                            height=20, border_color="black", border_width=3,
                                                            corner_radius=0)

        fg3a_filter_label = ctk.CTkLabel(self.fg3a_filter_container, text="Field Goals Attempted from 3 Point Line: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        fg3a_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.fg3a_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Field Goal from 3 Point Line Percentage

        self.fg3_pct_filter_entry_lower_bound = ctk.CTkEntry(self.fg3_pct_filter_container, font=("Arial", 20), width=40,
                                                            placeholder_text="0",
                                                            height=20, border_color="black", border_width=3,
                                                            corner_radius=0)

        fg3_pct_filter_label = ctk.CTkLabel(self.fg3_pct_filter_container, text="Field Goal Percentage from 3 Point Line: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        fg3_pct_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.fg3_pct_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Free Throws Made


        self.ftm_filter_entry_lower_bound = ctk.CTkEntry(self.ftm_filter_container, font=("Arial", 20), width=40,
                                                            placeholder_text="0",
                                                            height=20, border_color="black", border_width=3,
                                                            corner_radius=0)

        ftm_filter_label = ctk.CTkLabel(self.ftm_filter_container, text="Free Throws Made: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        ftm_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.ftm_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Free Throws Attempted

        self.fta_filter_entry_lower_bound = ctk.CTkEntry(self.fta_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)


        fta_filter_label = ctk.CTkLabel(self.fta_filter_container, text="Free Throws Attempted: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        fta_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.fta_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Free Throw Percentage

        self.ft_pct_filter_entry_lower_bound = ctk.CTkEntry(self.ft_pct_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)

        ft_pct_filter_label = ctk.CTkLabel(self.ft_pct_filter_container, text="Free Throw Percentage: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        ft_pct_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.ft_pct_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Offensive Rebounds

        self.oreb_filter_entry_lower_bound = ctk.CTkEntry(self.oreb_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)



        oreb_filter_label = ctk.CTkLabel(self.oreb_filter_container, text="Offensive Rebounds: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        oreb_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.oreb_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Defensive Rebounds

        self.dreb_filter_entry_lower_bound = ctk.CTkEntry(self.dreb_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)




        dreb_filter_label = ctk.CTkLabel(self.dreb_filter_container, text="Defensive Rebounds: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        dreb_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.dreb_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Rebounds

        self.reb_filter_entry_lower_bound = ctk.CTkEntry(self.reb_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)




        reb_filter_label = ctk.CTkLabel(self.reb_filter_container, text="Rebounds: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        reb_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.reb_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Assists

        self.ast_filter_entry_lower_bound = ctk.CTkEntry(self.ast_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)

        ast_filter_label = ctk.CTkLabel(self.ast_filter_container, text="Assists: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        ast_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.ast_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        #Steals

        self.stl_filter_entry_lower_bound = ctk.CTkEntry(self.stl_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)


        stl_filter_label = ctk.CTkLabel(self.stl_filter_container, text="Steals: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        stl_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.stl_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)


        #Blocks

        self.blk_filter_entry_lower_bound = ctk.CTkEntry(self.blk_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)




        blk_filter_label = ctk.CTkLabel(self.blk_filter_container, text="Blocks: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        blk_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.blk_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)



        #Turnovers



        self.to_filter_entry_upper_bound = ctk.CTkEntry(self.to_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="100",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)

        to_filter_label = ctk.CTkLabel(self.to_filter_container, text="Turnovers: No More Than ", font=("Arial", 20, "bold"),
                                        text_color="black")
        to_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.to_filter_entry_upper_bound.pack(side="left", padx=5, pady=0)


        #Personal Fouls



        self.pf_filter_entry_upper_bound = ctk.CTkEntry(self.pf_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="100",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)


        pf_filter_label = ctk.CTkLabel(self.pf_filter_container, text="Personal Fouls: No More Than ", font=("Arial", 20, "bold"),
                                        text_color="black")
        pf_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.pf_filter_entry_upper_bound.pack(side="left", padx=5, pady=0)


        #Points

        self.pts_filter_entry_lower_bound = ctk.CTkEntry(self.pts_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)




        pts_filter_label = ctk.CTkLabel(self.pts_filter_container, text="Points: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        pts_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.pts_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)



        #Plus Minus

        self.plus_minus_filter_entry_lower_bound = ctk.CTkEntry(self.plus_minus_filter_container, font=("Arial", 20), width=40,
                                                         placeholder_text="0",
                                                         height=20, border_color="black", border_width=3,
                                                         corner_radius=0)




        plus_minus_filter_label = ctk.CTkLabel(self.plus_minus_filter_container, text="Plus-minus: At Least ", font=("Arial", 20, "bold"),
                                        text_color="black")
        plus_minus_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.plus_minus_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)



        #The button for the user to apply their filters
        apply_button = ctk.CTkButton(self.plus_minus_filter_container, text="Apply Filters", font=("Arial", 20),
                                     border_width=5, corner_radius=0, command=self.apply_button,
                                     border_color="black")
        apply_button.pack(padx=20)


        self.players_holder = ctk.CTkFrame(self.big_frame, fg_color="transparent", height=3000)
        self.players_holder.pack(anchor="center", padx=0, pady=0)

        #Create boxes to display players


        for player in self.master.all_players[:self.players_per_page]:

            self.add_player_box(
                player = player
            )
            


    def add_filters(self):
        """ Display the available filters to the user """

        #Convert the "Add Filter" button into a "Remove Filter" button
        self.filter_button.configure(text = "Remove Filters", command = self.remove_filters, fg_color = "red")

        self.fgm_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.fga_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.fg_pct_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.fg3m_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.fg3a_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.fg3_pct_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.ftm_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.fta_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.ft_pct_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.oreb_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.dreb_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.reb_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.ast_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.stl_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.blk_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.to_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.pf_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.pts_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.plus_minus_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")



    def remove_filters(self):
        """ Remove the filters from the screen """

        self.filter_container.configure(height = 0)

        self.fgm_filter_container.pack_forget()
        self.fga_filter_container.pack_forget()
        self.fg_pct_filter_container.pack_forget()
        self.fg3m_filter_container.pack_forget()
        self.fg3a_filter_container.pack_forget()
        self.fg3_pct_filter_container.pack_forget()
        self.ftm_filter_container.pack_forget()
        self.fta_filter_container.pack_forget()
        self.ft_pct_filter_container.pack_forget()
        self.oreb_filter_container.pack_forget()
        self.dreb_filter_container.pack_forget()
        self.reb_filter_container.pack_forget()
        self.ast_filter_container.pack_forget()
        self.stl_filter_container.pack_forget()
        self.blk_filter_container.pack_forget()
        self.to_filter_container.pack_forget()
        self.pf_filter_container.pack_forget()
        self.pts_filter_container.pack_forget()
        self.plus_minus_filter_container.pack_forget()




        #Reset all filter upper and lower bounds
        self.fgm_lower_bound = 0

        self.fga_lower_bound = 0

        self.fg_pct_lower_bound = 0

        self.fg3m_lower_bound = 0

        self.fg3a_lower_bound = 0

        self.fg3_pct_lower_bound = 0

        self.ftm_lower_bound = 0

        self.fta_lower_bound = 0

        self.ft_pct_lower_bound = 0

        self.oreb_lower_bound = 0

        self.dreb_lower_bound = 0

        self.reb_lower_bound = 0

        self.ast_lower_bound = 0

        self.stl_lower_bound = 0

        self.blk_lower_bound = 0

        self.to_upper_bound = 100

        self.pf_upper_bound = 100

        self.pts_lower_bound = 0

        self.plus_minus_lower_bound = -100

        #Convert the "Remove Filter" button into an "Add Filter" button
        self.filter_button.configure(text="Add Filters", command=self.add_filters, fg_color = "gray")

        self.filter_players()

    def show_popup(self, message, color):
        """ Show a popup on the screen
            message: The message to show
            color: The color of the popup """

        popup = ctk.CTkFrame(self, fg_color=color)
        popup_text = ctk.CTkLabel(popup, text=message, text_color="black", font=("Arial", 20, "bold"), width = 450)
        popup_text.pack(padx=10, pady=5)

        popup.place(relx=1, rely=1, x=-250, y=-550, anchor = "center")

        # Remove after 3 Seconds
        self.after(3000, popup.destroy)

    def add_player_box(self, player):
        """ Create a box that displays a player's information """

        box_frame = ctk.CTkFrame(self.players_holder, fg_color="#D0D0D0", border_color="black", border_width=5, corner_radius=0,
                                 width=800, height=130)
        box_frame.pack(padx=0, pady=(0, 0))
        box_frame.pack_propagate(False)

        player_label = ctk.CTkLabel(box_frame, image=utils.load_player_image(player.image_path, 175, 127), text="",
                                    fg_color="transparent")
        player_label.pack(side="left", padx=5, pady=(5, 6))

        player_info_frame = ctk.CTkFrame(box_frame, fg_color="#D0D0D0", border_color="black", border_width=0,
                                         corner_radius=0, width=240, height=57)
        player_info_frame.pack(side="left", padx=(20,0), pady=20)
        player_info_frame.pack_propagate(False)

        player_name = ctk.CTkLabel(player_info_frame, fg_color="transparent", text=player.player_name, font=("Arial", 20))
        player_name.pack(anchor="w")

        #player_age = ctk.CTkLabel(player_info_frame, fg_color="transparent", text="Age: " + str(player.age), font=("Arial", 20))
        #player_age.pack(anchor="w")

        stats_button = ctk.CTkButton(box_frame, text="View Stats", font=("Arial", 20), fg_color="#900090",
                                     border_color="black", border_width=5, corner_radius=0, command = lambda player = player, incoming = "Add Player": self.master.view_stats(player, incoming),
                                     width=130, height=60)
        stats_button.pack(side="left", padx=(20, 0), pady=10)

        add_button = ctk.CTkButton(box_frame, text="Add to Team", font=("Arial", 20), fg_color="#009000",
                                   border_color="black", border_width=5, corner_radius=0, command = lambda player = player: self.add_to_team(player),
                                   width=130,
                                   height=60)
        add_button.pack(side="left", pady=10, padx=(40, 0))

    def add_to_team(self, player):
        """ Add the player to the user's team """
        #If the user already has 8 players, stop them from adding the player
        if (len(self.master.team) >= self.master.MAX_TEAM_SIZE):
            self.show_popup("Can\'t add that player! Your team is full!", "#FF9999")
        else:
            #Add the player to the team and show a popup to confirm to the user that the player was added
            self.master.page3.add_player(player)
            self.show_popup(f"Successfully added {player.player_name}!", "#99FF99")

        #Reapply filters because a player already on the team should not appear in the Add Player page
        self.filter_players()

    def refresh(self):
        """ Refresh the players displayed on the page """

        #Clear all players currently displayed
        for box in self.players_holder.winfo_children():
            box.destroy()

        #Figure out which players will be shown
        start = self.page_index * self.players_per_page
        end = start + self.players_per_page
        players_to_show = self.filtered_players[start:end]

        #Create boxes for the players to be shown
        for player in players_to_show:
            self.add_player_box(player)

        #Contains buttons to go to the next or previous set of players
        buttons_holder = ctk.CTkFrame(self.players_holder, fg_color="transparent")
        buttons_holder.pack(pady=10)

        #If the player is past index 0, display a button that allows them to go to the previous page
        if self.page_index > 0:
            prev_button = ctk.CTkButton(buttons_holder, text="Previous", font=("Arial", 20), border_width=5, corner_radius=0, border_color = "black",
                                        command=self.prev_page)
            prev_button.pack(side="left", padx=10)
        #If the player is not at the final segment of players, allow them to go forward
        if end < len(self.filtered_players):
            next_button = ctk.CTkButton(buttons_holder, text="Next", font=("Arial", 20), border_width=5, corner_radius=0, border_color = "black",
                                        command=self.next_page)
            next_button.pack(side="left", padx=10)

    def apply_button(self):
        """ Apply the user's filters """

        #If the user did not specify an upper or lower bound for a certain stat, set a default for it

        self.fgm_lower_bound = int(self.fgm_filter_entry_lower_bound.get() or 0)

        self.fga_lower_bound = int(self.fga_filter_entry_lower_bound.get() or 0)

        self.fg_pct_lower_bound = int(self.fg_pct_filter_entry_lower_bound.get() or 0)

        self.fg3m_lower_bound = int(self.fg3m_filter_entry_lower_bound.get() or 0)

        self.fg3a_lower_bound = int(self.fg3a_filter_entry_lower_bound.get() or 0)

        self.fg3_pct_lower_bound = int(self.fg3_pct_filter_entry_lower_bound.get() or 0)

        self.ftm_lower_bound = int(self.ftm_filter_entry_lower_bound.get() or 0)

        self.fta_lower_bound = int(self.fta_filter_entry_lower_bound.get() or 0)

        self.ft_pct_lower_bound = int(self.ft_pct_filter_entry_lower_bound.get() or 0)

        self.oreb_lower_bound = int(self.oreb_filter_entry_lower_bound.get() or 0)

        self.dreb_lower_bound = int(self.dreb_filter_entry_lower_bound.get() or 0)

        self.reb_lower_bound = int(self.reb_filter_entry_lower_bound.get() or 0)

        self.ast_lower_bound = int(self.ast_filter_entry_lower_bound.get() or 0)

        self.stl_lower_bound = int(self.stl_filter_entry_lower_bound.get() or 0)

        self.blk_lower_bound = int(self.blk_filter_entry_lower_bound.get() or 0)

        self.to_upper_bound = int(self.to_filter_entry_upper_bound.get() or 100)

        self.pf_upper_bound = int(self.pf_filter_entry_upper_bound.get() or 100)

        self.pts_lower_bound = int(self.pts_filter_entry_lower_bound.get() or 0)

        self.plus_minus_lower_bound = int(self.plus_minus_filter_entry_lower_bound.get() or -100)

        #After upper and lower bounds are decided for each stat, apply these filters
        self.filter_players()


    def next_page(self):
        self.page_index += 1
        self.refresh()

    def prev_page(self):
        self.page_index -= 1
        self.refresh()

    def filter_players(self):
        """ Use the current filters to decide which players can be displayed """

        search_text = self.player_name_entry.get().lower()

        self.filtered_players = [
            player for player in self.master.all_players
            if player.player_name.lower().startswith(search_text)
               and player not in self.master.team
               and self.fgm_lower_bound <= player.fgm
               and self.fga_lower_bound <= player.fga
               and self.fg_pct_lower_bound <= 100 * player.fg_pct
               and self.fg3m_lower_bound <= player.fg3m
               and self.fg3a_lower_bound <= player.fg3a
               and self.fg3_pct_lower_bound <= 100 * player.fg3_pct
               and self.ftm_lower_bound <= player.ftm
               and self.fta_lower_bound <= player.fta
               and self.ft_pct_lower_bound <= 100 * player.ft_pct
               and self.oreb_lower_bound <= player.oreb
               and self.dreb_lower_bound <= player.dreb
               and self.reb_lower_bound <= player.reb
               and self.ast_lower_bound <= player.ast
               and self.stl_lower_bound <= player.stl
               and self.blk_lower_bound <= player.blk
               and player.to <= self.to_upper_bound
               and player.pf <= self.pf_upper_bound
               and self.pts_lower_bound <= player.pts
               and self.plus_minus_lower_bound <= player.plus_minus
        ]

        #Reset to first page when the user applies new filters
        self.page_index = 0
        self.refresh()