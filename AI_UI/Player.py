import pandas as pd

class Player:

    def __init__(self, player_name, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, to, pf, pts, plus_minus, player_id, image_path):
        self.player_name = player_name
        self.image_path = image_path
        self.fgm = fgm
        self.fga = fga
        self.fg_pct = fg_pct
        self.fg3m = fg3m
        self.fg3a = fg3a
        self.fg3_pct = fg3_pct
        self.ftm = ftm
        self.fta = fta
        self.ft_pct = ft_pct
        self.oreb = oreb
        self.dreb = dreb
        self.reb = reb
        self.ast = ast
        self.stl = stl
        self.blk = blk
        self.to = to
        self.pf = pf
        self.pts = pts
        self.plus_minus = plus_minus
        self.player_id = player_id

        #If the player's weight was blank kn the database, set it to -1
        """
        if pd.isna(weight):
            self.weight = -1
        else:
            self.weight = int(weight)

        #Height is separated into inches and feet
        if pd.isna(height):
            self.height_ft = -1
            self.height_inch = -1
        else:
            ft, inch = height.split("-")
            self.height_ft = int(ft)
            self.height_inch = int(inch)
        """


    def __repr__(self):
        return f"Player({self.player_name})"

    def __eq__(self, other):
        return isinstance(other, Player) and self.player_name == other.player_name and self.player_id == other.player_id

    def __hash__(self):
        return hash((        self.player_name, self.image_path, self.fgm, self.fga, self.fg_pct, self.fg3m, self.fg3a, self.fg3_pct, self.ftm, self.fta, self.ft_pct, self.oreb, self.dreb, self.reb, self.ast, self.stl, self.blk, self.to, self.pf, self.pts, self.plus_minus, self.player_id))


