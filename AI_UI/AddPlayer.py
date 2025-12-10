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
        self.players_per_page = 15

        #Keeps track of which specific players are currently being displayed
        self.page_index = 0

        #A list of players to display after all filters have been applied
        self.filtered_players = self.master.all_players.copy()

        #The bounds on the filters applied for age, weight, and height
        self.age_lower_bound = 0
        self.age_upper_bound = 99

        self.weight_lower_bound = 0
        self.weight_upper_bound = 500

        self.height_lower_bound = 0
        self.height_upper_bound = 108

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        back_to_team_button = ctk.CTkButton(self, text="Back to Team", font=("Arial", 20), fg_color="#900090",
                                            border_color="black", border_width=5, corner_radius=0,
                                            command=master.show_page3, width=130, height=60)
        back_to_team_button.pack(padx=(5,0), pady=(5,0), anchor="w")

        big_frame = ctk.CTkFrame(self, fg_color="transparent", height = 3000)
        big_frame.pack(anchor = "center", padx = 0, pady = 0)

        label = ctk.CTkLabel(big_frame, text="ADD PLAYER", font=("Arial", 40, "bold"))
        label.pack(pady=(5,0), anchor = "w", padx = 0)

        #A row to hold the search bar and filters button
        search_row = ctk.CTkFrame(big_frame, fg_color = "transparent")
        search_row.pack(padx=(0,0), pady=(5,0), anchor = "center")

        #A search bar for the player to search for a specific player name
        self.player_name_entry = ctk.CTkEntry(search_row, placeholder_text="Search", font = ("Arial", 20), width = 640, height = 37, border_color = "black", border_width = 5, corner_radius = 0)
        self.player_name_entry.pack(side = "left", padx=5, pady=0)

        #When the user types something in the search bar, use their search to filter out players
        self.player_name_entry.bind("<KeyRelease>", lambda event: self.filter_players())

        self.filter_button = ctk.CTkButton(search_row, text="Add Filters", font = ("Arial", 20), border_color = "black", border_width = 5, corner_radius = 0, command=self.add_filters, width = 150, height = 30, fg_color = "#777777")
        self.filter_button.pack(side = "left", pady=0)

        #Contains the filters for age, height, and weight
        self.filter_container = ctk.CTkFrame(big_frame, fg_color="transparent", height = 0)
        self.filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")

        #These filters are not displayed until the user hits the "Add Filters" button
        self.age_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height = 0)
        self.height_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height=0)
        self.weight_filter_container = ctk.CTkFrame(self.filter_container, fg_color="transparent", height=0)

        #A scrollable frame so the user can scroll through potential players
        self.scroll_frame = ctk.CTkScrollableFrame(big_frame, width=800, height=2000)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(20,0))

        #The spaces for the user to enter the upper and lower bounds for each filter
        self.age_filter_entry_lower_bound = ctk.CTkEntry(self.age_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                         height=20, border_color="black", border_width=3, corner_radius=0)

        self.age_filter_entry_upper_bound = ctk.CTkEntry(self.age_filter_container, font=("Arial", 20), width=40, placeholder_text="99",
                                                    height=20, border_color="black", border_width=3, corner_radius=0)

        self.height_filter_entry_lower_bound_ft = ctk.CTkEntry(self.height_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                    height=20, border_color="black", border_width=3, corner_radius=0)

        self.height_filter_entry_lower_bound_in = ctk.CTkEntry(self.height_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                          height=20, border_color="black", border_width=3, corner_radius=0)

        self.height_filter_entry_upper_bound_ft = ctk.CTkEntry(self.height_filter_container, font=("Arial", 20), width=40, placeholder_text="9",
                                                    height=20, border_color="black", border_width=3, corner_radius=0)

        self.height_filter_entry_upper_bound_in = ctk.CTkEntry(self.height_filter_container, font=("Arial", 20), width=40, placeholder_text="0",
                                                          height=20, border_color="black", border_width=3, corner_radius=0)

        self.weight_filter_entry_lower_bound = ctk.CTkEntry(self.weight_filter_container, font=("Arial", 20), width=60, placeholder_text="0",
                                                       height=20, border_color="black", border_width=3, corner_radius=0)

        self.weight_filter_entry_upper_bound = ctk.CTkEntry(self.weight_filter_container, font=("Arial", 20), width=60, placeholder_text="500",
                                                       height=20, border_color="black", border_width=3, corner_radius=0)

        age_filter_label = ctk.CTkLabel(self.age_filter_container, text="AGE: Between ", font=("Arial", 20, "bold"),
                                        text_color="black")
        age_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.age_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        age_filter_label_2 = ctk.CTkLabel(self.age_filter_container, text=" and ", font=("Arial", 20, "bold"),
                                          text_color="black")
        age_filter_label_2.pack(pady=(0, 0), side="left", padx=0)

        self.age_filter_entry_upper_bound.pack(side="left", padx=5, pady=0)

        height_filter_label = ctk.CTkLabel(self.height_filter_container, text="HEIGHT: Between ",
                                           font=("Arial", 20, "bold"),
                                           text_color="black")
        height_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.height_filter_entry_lower_bound_ft.pack(side="left", padx=1, pady=0)

        height_filter_label_2 = ctk.CTkLabel(self.height_filter_container, text="\'",
                                             font=("Arial", 20, "bold"),
                                             text_color="black")
        height_filter_label_2.pack(pady=(0, 0), side="left", padx=0)

        self.height_filter_entry_lower_bound_in.pack(side="left", padx=1, pady=0)

        height_filter_label_3 = ctk.CTkLabel(self.height_filter_container, text="\" and ", font=("Arial", 20, "bold"),
                                             text_color="black")
        height_filter_label_3.pack(pady=(0, 0), side="left", padx=0)

        self.height_filter_entry_upper_bound_ft.pack(side="left", padx=1, pady=0)

        height_filter_label_4 = ctk.CTkLabel(self.height_filter_container, text="\'", font=("Arial", 20, "bold"),
                                             text_color="black")
        height_filter_label_4.pack(pady=(0, 0), side="left", padx=0)

        self.height_filter_entry_upper_bound_in.pack(side="left", padx=1, pady=0)

        height_filter_label_5 = ctk.CTkLabel(self.height_filter_container, text="\"", font=("Arial", 20, "bold"),
                                             text_color="black")
        height_filter_label_5.pack(pady=(0, 0), side="left", padx=0)

        weight_filter_label = ctk.CTkLabel(self.weight_filter_container, text="WEIGHT: Between ",
                                           font=("Arial", 20, "bold"),
                                           text_color="black")
        weight_filter_label.pack(pady=(0, 0), side="left", padx=0)

        self.weight_filter_entry_lower_bound.pack(side="left", padx=5, pady=0)

        weight_filter_label_2 = ctk.CTkLabel(self.weight_filter_container, text="lbs and ", font=("Arial", 20, "bold"),
                                             text_color="black")
        weight_filter_label_2.pack(pady=(0, 0), side="left", padx=0)

        self.weight_filter_entry_upper_bound.pack(side="left", padx=5, pady=0)

        weight_filter_label_3 = ctk.CTkLabel(self.weight_filter_container, text="lbs", font=("Arial", 20, "bold"),
                                             text_color="black")
        weight_filter_label_3.pack(pady=(0, 0), side="left", padx=0)

        #The button for the user to apply their filters
        apply_button = ctk.CTkButton(self.weight_filter_container, text="Apply Filters", font=("Arial", 20),
                                     border_width=5, corner_radius=0, command=self.apply_button,
                                     border_color="black")
        apply_button.pack(padx=20)

        #Create boxes to display players
        for player in self.master.all_players[:self.players_per_page]:

            self.add_player_box(
                player = player
            )

    def add_filters(self):
        """ Display the available filters to the user """

        #Convert the "Add Filter" button into a "Remove Filter" button
        self.filter_button.configure(text = "Remove Filters", command = self.remove_filters, fg_color = "red")

        self.age_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.height_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")
        self.weight_filter_container.pack(padx=(0, 0), pady=(0, 0), anchor="w")

    def remove_filters(self):
        """ Remove the filters from the screen """

        self.age_filter_container.pack_forget()
        self.weight_filter_container.pack_forget()
        self.height_filter_container.pack_forget()

        #Reset all filter upper and lower bounds
        self.age_lower_bound = 0
        self.age_upper_bound = 99

        self.weight_lower_bound = 0
        self.weight_upper_bound = 500

        self.height_lower_bound = 0
        self.height_upper_bound = 108

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

        box_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#D0D0D0", border_color="black", border_width=5, corner_radius=0,
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

        player_name = ctk.CTkLabel(player_info_frame, fg_color="transparent", text=player.name, font=("Arial", 20))
        player_name.pack(anchor="w")

        player_age = ctk.CTkLabel(player_info_frame, fg_color="transparent", text="Age: " + str(player.age), font=("Arial", 20))
        player_age.pack(anchor="w")

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
        #If the user already has 15 players, stop them from adding the player
        if (len(self.master.team) >= 15):
            self.show_popup("Can\'t add that player! Your team is full!", "#FF9999")
        else:
            #Add the player to the team and show a popup to confirm to the user that the player was added
            self.master.page3.add_player(player)
            self.show_popup(f"Successfully added {player.name}!", "#99FF99")

        #Reapply filters because a player already on the team should not appear in the Add Player page
        self.filter_players()

    def refresh(self):
        """ Refresh the players displayed on the page """

        #Clear all players currently displayed
        for box in self.scroll_frame.winfo_children():
            box.destroy()

        #Figure out which players will be shown
        start = self.page_index * self.players_per_page
        end = start + self.players_per_page
        players_to_show = self.filtered_players[start:end]

        #Create boxes for the players to be shown
        for player in players_to_show:
            self.add_player_box(player)

        #Contains buttons to go to the next or previous set of players
        buttons_holder = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
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
        self.age_lower_bound = self.age_filter_entry_lower_bound.get()

        if len(self.age_lower_bound) == 0:
            self.age_lower_bound = 0
        else:
            self.age_lower_bound = int(self.age_lower_bound)

        self.age_upper_bound = self.age_filter_entry_upper_bound.get()

        if len(self.age_upper_bound) == 0:
            self.age_upper_bound = 99
        else:
            self.age_upper_bound = int(self.age_upper_bound)

        self.weight_lower_bound = self.weight_filter_entry_lower_bound.get()

        if len(self.weight_lower_bound) == 0:
            self.weight_lower_bound = 0
        else:
            self.weight_lower_bound = int(self.weight_lower_bound)

        self.weight_upper_bound = self.weight_filter_entry_upper_bound.get()

        if len(self.weight_upper_bound) == 0:
            self.weight_upper_bound = 500
        else:
            self.weight_upper_bound = int(self.weight_upper_bound)


        height_lower_bound_ft = self.height_filter_entry_lower_bound_ft.get()

        if len(height_lower_bound_ft) == 0:
            height_lower_bound_ft = 0
        else:
            height_lower_bound_ft = int(height_lower_bound_ft)

        height_lower_bound_in = self.height_filter_entry_lower_bound_in.get()

        if len(height_lower_bound_in) == 0:
            height_lower_bound_in = 0
        else:
            height_lower_bound_in = int(height_lower_bound_in)

        self.height_lower_bound = height_lower_bound_ft * 12 + height_lower_bound_in

        height_upper_bound_ft = self.height_filter_entry_upper_bound_ft.get()

        if len(height_upper_bound_ft) == 0:
            height_upper_bound_ft = 9
        else:
            height_upper_bound_ft = int(height_upper_bound_ft)

        height_upper_bound_in = self.height_filter_entry_upper_bound_in.get()

        if len(height_upper_bound_in) == 0:
            height_upper_bound_in = 0
        else:
            height_upper_bound_in = int(height_upper_bound_in)

        self.height_upper_bound = height_upper_bound_ft * 12 + height_upper_bound_in


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
            if player.name.lower().startswith(search_text)
               and player not in self.master.team
               and self.age_lower_bound <= player.age <= self.age_upper_bound
               and self.weight_lower_bound <= int(player.weight) <= self.weight_upper_bound
               and self.height_lower_bound <= (player.height_ft * 12 + player.height_inch) <= self.height_upper_bound

        ]

        #for player in self.filtered_players:
        #    print(player.height_ft * 12 + player.height_inch)

        #Reset to first page when the user applies new filters
        self.page_index = 0
        self.refresh()