import customtkinter as ctk
from PIL import Image
from AddPlayer import AddPlayer
from PlayerProfile import PlayerProfile
from TeamSummary import TeamSummary
import pandas as pd
from Player import Player

class App(ctk.CTk):

    all_players: list[Player] = []
    team: list[Player] = []

    def __init__(self):
        super().__init__()
        self.geometry("1200x600")

        #Stores every player who has played since 2004
        self.all_players = []

        #Stores the user's current team
        self.team = []

        df = pd.read_csv("common_player_info.csv")

        df = df[df["to_year"] >= 2004]

        df["birthdate"] = pd.to_datetime(df["birthdate"])

        today = pd.Timestamp.today()

        df["age"] = (today - df["birthdate"]).dt.days // 365

        df = df[["display_first_last", "weight", "height", "age"]]

        #For each row, create a new player and add it to all_players
        for index, row in df.iterrows():
            name = row["display_first_last"]
            weight = row["weight"]
            height = row["height"]
            age = row["age"]

            player = Player(
                name=name,
                weight=weight,
                height=height,
                age=age,
                image_path="AI_UI_NBA_Player_Images_67/" + name + ".png"
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
