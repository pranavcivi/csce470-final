import pandas as pd
from lyricsgenius import Genius
import re
import time
import pickle

def contains_non_english(text):
    pattern = r"[^a-zA-Z0-9\s\-\(\)\'\"]"
    if re.search(pattern, text):
        return True
    return False

lyrics = {}
not_found = set()
visited = set()

with open('lyrics-updated.pkl', 'rb') as f:
    lyrics = pickle.load(f)

with open('not_found-updated.pkl', 'rb') as f1:
    not_found = pickle.load(f1)

with open('visited.pkl', 'rb') as f3:
    visited = pickle.load(f3)


# going through the excel file
df = pd.read_excel('lyrics.xlsx', sheet_name='muse_v3')
# random_rows = df.sample(n=1000, random_state=1)


count = 0
for index, row in df.iterrows():
    track_name = row['track'].replace("'", "’")
    # it was me barry
    if track_name in lyrics:
        lyrics[track_name] = [lyrics[track_name], row['seeds'][0]]

with open('lyrics-updated.pkl', 'wb') as f:
    pickle.dump(lyrics, f)

with open('not_found-updated.pkl', 'wb') as f1:
    pickle.dump(not_found, f1)

with open('visited.pkl', 'wb') as f3:
    pickle.dump(visited, f3)