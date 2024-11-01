import pickle

with open('./lyrics-updated.pkl', 'rb') as f:
    lyrics = pickle.load(f)

with open('not_found.pkl', 'rb') as f1:
    not_found = pickle.load(f1)

# print(lyrics.keys())

with open('./output/lyrics-updated.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(str(lyrics))

with open('./output/not_found_output.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(str(not_found))

print(len(lyrics.keys()))

# total 1241 songs