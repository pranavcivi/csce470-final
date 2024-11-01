import pandas as pd

# 812 genres, 542 seeds

df = pd.read_excel('muse_v3.xlsx', sheet_name='muse_v3')

genres = set()

# for index, row in df.iterrows():
#     genres.add(row['genre'])

for index, row in df.iterrows():
    seeds = row['seeds'][1:-1].split(',')
    for seed in seeds:
        genres.add(seed)


print(len(genres))