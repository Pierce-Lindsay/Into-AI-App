import kagglehub
# Download latest version
path = kagglehub.dataset_download("nathanlauga/nba-games")
#downloads to path printed out, will probably be at a cache folder
print("Path to dataset files:", path)