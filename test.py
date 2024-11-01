from lyricsgenius import Genius
import re

# valence: pleasantness 0.24 to 8.47
# arousal: intensity 0.11 to 7.27
# dominance: control 0.23 to 7.44



# genius = Genius('Ljj53SzSk_1gxLmf3rcGeaqDi11CVI5SZ9sw7vUk87ENYA60cha4KLeLpD8cIgub')
genius = Genius('HhcPCGMwENzdfMQlauEV1Om0UormkWc6Wrwxri-LFTfBSNkzhwMSVUnR5tZG8eXW')
genius.remove_section_headers = True
genius.skip_non_songs = False
genius.excluded_terms = ["Remix", "Live"]
# artist = genius.search_artist("Chappel Roan", max_songs=10, sort="title")
# # print(artist.songs)

# for song in artist.songs:
#     lyrics_bytes = song.lyrics.encode("utf-8")
#     lyrics_str = lyrics_bytes.decode("utf-8")
#     cleaned_lyrics = re.sub(r'[^\w\s]+', '', lyrics_str)
#     print(cleaned_lyrics.encode("utf-8"))
#     # print(song.lyrics.encode("utf-8"))

song_name = "Happy"
artist = "Pharrel Williams"

song = genius.search_song(song_name, artist)
pos = song.lyrics.find(f'{song_name} Lyrics')
print(song.lyrics[pos:])