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
        box_frame = ctk.CTkFrame(info_holder, fg_color="#D0D0D0", border_color="black", border_width=5, corner_radius=0, width = 540, height = 391)
        box_frame.pack(side = "left", padx=20, pady=0)
        box_frame.pack_propagate(False)

        #NOTE: Info defaults to info for LeBron James but will be overridden when the user actually views the stats for a player
        player_path = "AI_UI_NBA_Player_Images_67/Lebron James.png"
        self.player_label = ctk.CTkLabel(box_frame, image=utils.load_player_image(player_path, 525, 381), text = "")
        self.player_label.pack(side = "left", padx=5, pady=5)

        player_info_frame = ctk.CTkFrame(info_holder, fg_color="transparent", border_color="black", border_width=0,
                                         corner_radius=0, width=500, height=2000)
        player_info_frame.pack(side="left", padx=20, pady=20)
        player_info_frame.pack_propagate(False)

        field_goal_frame = ctk.CTkFrame(player_info_frame, fg_color="#FF7777", border_color="black", border_width=5, corner_radius=0,
                                 width=460, height=180)
        field_goal_frame.pack(padx=20, pady=5)
        field_goal_frame.pack_propagate(False)

        self.player_fgm = ctk.CTkLabel(field_goal_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_fgm.pack(pady = (5, 0), padx = (10, 0), anchor="w")

        self.player_fga = ctk.CTkLabel(field_goal_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_fga.pack(padx = (10, 0), anchor="w")

        self.player_fg_pct = ctk.CTkLabel(field_goal_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_fg_pct.pack(padx = (10, 0), anchor="w")

        self.player_fg3m = ctk.CTkLabel(field_goal_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_fg3m.pack(padx = (10, 0), anchor="w")

        self.player_fg3a = ctk.CTkLabel(field_goal_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_fg3a.pack(padx = (10, 0), anchor="w")

        self.player_fg3_pct = ctk.CTkLabel(field_goal_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_fg3_pct.pack(padx = (10, 0), anchor="w")

        free_throw_frame = ctk.CTkFrame(player_info_frame, fg_color="#77FF77", border_color="black", border_width=5, corner_radius=0,
                                 width=490, height=95)
        free_throw_frame.pack(padx=20, pady=5)
        free_throw_frame.pack_propagate(False)

        self.player_ftm = ctk.CTkLabel(free_throw_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_ftm.pack(pady = (5,0), padx = (10, 0), anchor="w")

        self.player_fta = ctk.CTkLabel(free_throw_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_fta.pack(padx = (10, 0), anchor="w")

        self.player_ft_pct = ctk.CTkLabel(free_throw_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_ft_pct.pack(padx = (10, 0), anchor="w")

        rebound_frame = ctk.CTkFrame(player_info_frame, fg_color="#7777FF", border_color="black", border_width=5,
                                        corner_radius=0,
                                        width=490, height=95)
        rebound_frame.pack(padx=20, pady=5)
        rebound_frame.pack_propagate(False)

        self.player_oreb = ctk.CTkLabel(rebound_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_oreb.pack(pady = (5, 0), padx = (10, 0), anchor="w")

        self.player_dreb = ctk.CTkLabel(rebound_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_dreb.pack(padx = (10, 0), anchor="w")

        self.player_reb = ctk.CTkLabel(rebound_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_reb.pack(padx = (10, 0), anchor="w")

        other_frame = ctk.CTkFrame(player_info_frame, fg_color="#FFFF77", border_color="black", border_width=5,
                                     corner_radius=0,
                                     width=490, height=206)
        other_frame.pack(padx=20, pady=5)
        other_frame.pack_propagate(False)

        self.player_ast = ctk.CTkLabel(other_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_ast.pack(padx = (10, 0), pady = (5, 0), anchor="w")

        self.player_stl = ctk.CTkLabel(other_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_stl.pack(padx = (10, 0), anchor="w")

        self.player_blk = ctk.CTkLabel(other_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_blk.pack(padx = (10, 0), anchor="w")

        self.player_to = ctk.CTkLabel(other_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_to.pack(padx = (10, 0), anchor="w")

        self.player_pf = ctk.CTkLabel(other_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_pf.pack(padx = (10, 0), anchor="w")

        self.player_pts = ctk.CTkLabel(other_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_pts.pack(padx = (10, 0), anchor="w")

        self.player_plus_minus = ctk.CTkLabel(other_frame, fg_color="transparent", text="", font=("Arial", 20))
        self.player_plus_minus.pack(padx = (10, 0), anchor="w")

    def set_incoming_page(self, incoming_page):
        self.incoming_page = incoming_page

    def load_player(self, player):
        """ Used to override the current elements with the correct player information """

        self.player_name.configure(text = f"Average stats for {player.player_name}")
        self.player_fgm.configure(text = f"Field Goals Made: {round(player.fgm, 2)}")
        self.player_fga.configure(text = f"Field Goals Attempted: {round(player.fga, 2)}")
        self.player_fg_pct.configure(text = f"Field Goal Percentage: {round(100 * player.fg_pct, 2)}%")
        self.player_fg3m.configure(text = f"Field Goals from 3-point line Made: {round(player.fg3m, 2)}")
        self.player_fg3a.configure(text = f"Field Goals from 3-point line Attempted: {round(player.fg3a, 2)}")
        self.player_fg3_pct.configure(text = f"Field Goal from 3-point line Percentage: {round(100 * player.fg3_pct, 2)}%")
        self.player_ftm.configure(text = f"Free Throws Made: {round(player.ftm, 2)}")
        self.player_fta.configure(text = f"Free Throws Attempted: {round(player.fta, 2)}")
        self.player_ft_pct.configure(text = f"Free Throw Percentage: {round(100 * player.ft_pct, 2)}%")
        self.player_oreb.configure(text = f"Offensive Rebounds: {round(player.oreb, 2)}")
        self.player_dreb.configure(text = f"Defensive Rebounds: {round(player.dreb, 2)}")
        self.player_reb.configure(text = f"Total Rebounds: {round(player.reb, 2)}")
        self.player_ast.configure(text = f"Assists: {round(player.ast, 2)}")
        self.player_stl.configure(text = f"Steals: {round(player.stl, 2)}")
        self.player_blk.configure(text = f"Blocks: {round(player.blk, 2)}")
        self.player_to.configure(text = f"Turnovers: {round(player.to, 2)}")
        self.player_pf.configure(text = f"Personal Fouls: {round(player.pf, 2)}")
        self.player_pts.configure(text = f"Points: {round(player.pts, 2)}")
        self.player_plus_minus.configure(text = f"Plus-minus: {round(player.plus_minus, 2)}")


        self.player_label.configure(image=utils.load_player_image(player.image_path, 525, 381))

    def go_back(self):
        """ Used to return to the previous page. This might be either the Team Summary page or the Add Player page """

        if self.incoming_page == "Team Summary":
            self.master.show_page3()
        else:
            self.master.show_page1()