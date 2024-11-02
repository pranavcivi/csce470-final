import pandas as pd
from lyricsgenius import Genius
import re
import time
import pickle
from langdetect import detect, LangDetectException

def contains_non_english(text):
    pattern = r"[^a-zA-Z0-9\s\-\(\)\'\"]"
    if re.search(pattern, text):
        return True
    return False

# genius = Genius('Ljj53SzSk_1gxLmf3rcGeaqDi11CVI5SZ9sw7vUk87ENYA60cha4KLeLpD8cIgub')
genius = Genius('xSvbiJTdHIYqpIoMCAXCUz_CJD5jqGLNPlO0YcDjRQHJk29ECZ0hcIynmvjiFlex')
genius.remove_section_headers = True
genius.skip_non_songs = False
genius.excluded_terms = ["Remix", "Live"]

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
random_rows = df.sample(n=1000)


count = 0
for index, row in random_rows.iterrows():
    if index in visited:
        continue
    visited.add(index)
    # if count < 1000:
    #     count += 1
    #     continue
    track_name = row['track'].replace("'", "’")
    artist_name = row['artist']
    
    try:
        song = genius.search_song(track_name, artist_name)
        pos = song.lyrics.find(f'{track_name} Lyrics')
        lyric = song.lyrics[pos:]
        if len(lyric) > 2:
            # print('here')
            emotion = row['seeds'][1:-1].split(',')[0][1:-1]
            lyrics[track_name] = [lyric, emotion]
            # print(lyric, emotion)
            # break
    except:
        not_found.add(track_name)
    time.sleep(0.5)
    # count += 1
    # if count >= 2000:
    #     break

with open('lyrics-updated.pkl', 'wb') as f:
    pickle.dump(lyrics, f)

with open('not_found-updated.pkl', 'wb') as f1:
    pickle.dump(not_found, f1)

with open('visited.pkl', 'wb') as f3:
    pickle.dump(visited, f3)