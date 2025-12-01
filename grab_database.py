import kagglehub
# Download latest version
path = kagglehub.dataset_download("nathanlauga/nba-games")

print("Path to dataset files:", path)