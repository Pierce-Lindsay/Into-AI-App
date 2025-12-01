#run this file to grab the kaggle database and place it in the gitignored data folder
import kagglehub
import os
import shutil

# Download latest version
path = kagglehub.dataset_download("nathanlauga/nba-games")
#downloads to path printed out, will probably be at a cache folder
print("Path to dataset files:", path)

dataset = "nathanlauga/nba-games"
# default cache path, we don't want this
cache_path = kagglehub.dataset_download(dataset)  
path_we_want = "data"
os.makedirs(path_we_want, exist_ok=True) #if doesn't exist make

# Move files over
for fname in os.listdir(cache_path):
    shutil.copy(os.path.join(cache_path, fname), path_we_want)