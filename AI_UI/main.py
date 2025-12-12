import customtkinter as ctk
from PIL import Image
from AddPlayer import AddPlayer
from PlayerProfile import PlayerProfile
from TeamSummary import TeamSummary
import pandas as pd
from Player import Player
from model import team_evaluator

class App(ctk.CTk):

    all_players: list[Player] = []
    team: list[Player] = []
    estimator = team_evaluator.Team_Estimator()

    def __init__(self):
        super().__init__()
        self.geometry("1200x600")

        #Stores every player who has played since 2004
        self.all_players = []

        #Stores the user's current team
        self.team = []

        # The maximum size of a team (may be decreased depending on the model)
        self.MAX_TEAM_SIZE = 8

        player_stats_df = pd.read_csv("data/player_stats_per_player.csv")

        #df = df[df["to_year"] >= 2004]

        #df["birthdate"] = pd.to_datetime(df["birthdate"])

        #today = pd.Timestamp.today()

        #df["age"] = (today - df["birthdate"]).dt.days // 365

        #df = df[["display_first_last", "weight", "height", "age"]]

        #For each row, create a new player and add it to all_players
        for index, row in player_stats_df.iterrows():
            player_name = row["PLAYER_NAME"]
            fgm = row["FGM"]
            fga = row["FGA"]
            fg_pct = row["FG_PCT"]
            fg3m = row["FG3M"]
            fg3a = row["FG3A"]
            fg3_pct = row["FG3_PCT"]
            ftm = row["FTM"]
            fta = row["FTA"]
            ft_pct = row["FT_PCT"]
            oreb = row["OREB"]
            dreb = row["DREB"]
            reb = row["REB"]
            ast = row["AST"]
            stl = row["STL"]
            blk = row["BLK"]
            to = row["TO"]
            pf = row["PF"]
            pts = row["PTS"]
            plus_minus = row["PLUS_MINUS"]
            player_id = row["PLAYER_ID"]
            #weight = row["weight"]
            #height = row["height"]
            #age = row["age"]

            player = Player(
                player_name = player_name,
                fgm = fgm,
                fga = fga,
                fg_pct = fg_pct,
                fg3m = fg3m,
                fg3a = fg3a,
                fg3_pct = fg3_pct,
                ftm = ftm,
                fta = fta,
                ft_pct = ft_pct,
                oreb = oreb,
                dreb = dreb,
                reb = reb,
                ast = ast,
                stl = stl,
                blk = blk,
                to = to,
                pf = pf,
                pts = pts,
                plus_minus = plus_minus,
                player_id = player_id,
                image_path="AI_UI/AI_UI_NBA_Player_Images_67/" + player_name + ".png"
            )

            self.all_players.append(player)


        #Create 3 pages. Start at the Team Summary
        self.page1 = AddPlayer(self)
        self.page2 = PlayerProfile(self)
        self.page3 = TeamSummary(self)

        self.page2.pack_forget()
        self.page1.pack_forget()

    def show_page1(self):
        """ Show the Add Player page """
        self.page2.pack_forget()
        self.page3.pack_forget()

        self.page1.refresh()
        self.page1.pack(fill="both", expand=True)

    def show_page2(self):
        """ Show the Player Profile page """
        self.page1.pack_forget()
        self.page3.pack_forget()
        self.page2.pack(fill="both", expand=True)

    def show_page3(self):
        """ Show the Team Summary page """
        self.page1.pack_forget()
        self.page2.pack_forget()
        self.page3.pack(fill="both", expand=True)

    def view_stats(self, player, incoming):
        """ Used to navigate to the Player Profile page with a specific player
            player: The player whose stats should be viewed
            incoming: Which page the user is navigating from """

        self.page2.load_player(player)

        self.page2.set_incoming_page(incoming)

        self.show_page2()

if __name__ == "__main__":
    app = App()
    app.mainloop()
