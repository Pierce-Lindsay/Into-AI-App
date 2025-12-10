import pandas as pd
import numpy as np
import heapq 

PLAYER_MIN = 8
PLAYER_STAT_NAMES = ['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT',
                     'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']
FEATURE_COUNT = PLAYER_MIN * len(PLAYER_STAT_NAMES)
print("loading games...")
games = pd.read_csv("data/games.csv")
games = games.drop_duplicates(subset=["GAME_ID"])
games = games[["GAME_ID", "GAME_DATE_EST", "HOME_TEAM_ID", "VISITOR_TEAM_ID", "HOME_TEAM_WINS"]]
games['GAME_DATE_EST'] = pd.to_datetime(games['GAME_DATE_EST'])
print("loading game details...")
game_details = pd.read_csv("data/games_details.csv")
games_details = game_details.drop(columns = ["TEAM_ABBREVIATION", "TEAM_CITY","PLAYER_NAME", "NICKNAME",
                                             "START_POSITION", "COMMENT"])

full_game_details = pd.merge(games, game_details, on="GAME_ID", how="inner")
games_indexed = games.set_index("GAME_ID")
fgd_indexed = full_game_details.set_index("PLAYER_ID")
player_groups = full_game_details.groupby("PLAYER_ID", sort=False)
#print(full_game_details.head())

#first step is to compute player average stats for every game they have played in as of that specific game
#player name, stat 1, stat2, stat3, ...
#end model feature goal p1 stats, p2 stats, p3 stats...label = 1 or 0 for that game

def average_player_stats(player_id, game_id):
    #want to grab every game a player played in with data < estimate stats game date
    target_date = games_indexed.loc[game_id, "GAME_DATE_EST"]
    rows = player_groups.get_group(player_id)
    applicable_rows = rows[rows["GAME_DATE_EST"] < target_date]
    #average stats for catergory we care about
    return applicable_rows[PLAYER_STAT_NAMES].mean().to_list()
    
    
def generate_sample_from_players(game_id, player_ids):
    players_averages = []
    for player_id in player_ids:
        stats = average_player_stats(player_id, game_id)
        #minheap so we want to negate to get biggest on bottom
        heapq.heappush(players_averages, (-np.sum(stats), stats))
    #pick 8 best
    if(len(players_averages) < 8):
        print(f"error: player count: {len(players_averages)}")
        return []
    sample = np.empty(FEATURE_COUNT)
    player_len = len(PLAYER_STAT_NAMES)
    for i in range(PLAYER_MIN):
        sample[(i * player_len):(i * player_len + player_len)] = players_averages[i][1]
    return sample

#min of 8 players per NBA team, pick 8 best??
#for every game, for every player in that game
feature_dictionary_keys = []
for i in range(PLAYER_MIN):
    for key in PLAYER_STAT_NAMES:
        feature_dictionary_keys.append(key + str(i))
row_count = len(games)*2
samples = pd.DataFrame(np.empty((row_count, len(feature_dictionary_keys))), columns=feature_dictionary_keys)
labels = np.empty(row_count)
print(feature_dictionary_keys)
index = 0
i = 0   
for game_id in games["GAME_ID"]:
    print(f"game_id: {game_id}, number: {i}")
    # Get all rows for this game (filter once)
    specific_game = game_details.loc[game_details["GAME_ID"] == game_id]

    # Get game info
    extra_game_info = games.loc[games["GAME_ID"] == game_id].iloc[0]
    home = extra_game_info["HOME_TEAM_ID"]
    away = extra_game_info["VISITOR_TEAM_ID"]
    home_won = extra_game_info["HOME_TEAM_WINS"]
    away_won = 1 - home_won

    # Split using vectorized comparison (no additional copies)
    home_player_ids = specific_game.loc[specific_game["TEAM_ID"] == home, "PLAYER_ID"]
    away_player_ids = specific_game.loc[specific_game["TEAM_ID"] == away, "PLAYER_ID"]
    #add 8 best players from each as samples, two samples from each game(winners and losers)
    row = generate_sample_from_players(game_id, home_player_ids)
    if(len(row) != 0):
        samples.loc[index] = row
        labels[index] = home_won
        index+=1
    row = generate_sample_from_players(game_id, away_player_ids)
    if(len(row) != 0):
        samples.loc[index] = row
        labels[index] = away_won
        index+=1
    i+=1
    
samples["GAME_WON"] = labels
print("exporting...")
samples.to_csv("data/player_stats_per_game.csv")