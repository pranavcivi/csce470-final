from flask import Flask, redirect, render_template, url_for
from lyricsgenius import Genius
import pickle
import math
from collections import Counter
app = Flask(__name__)
import os
from flask import Flask, render_template, request, jsonify


# os.environ['HTTP_PROXY'] = ''
# os.environ['HTTPS_PROXY'] = ''
# os.environ['NO_PROXY'] = 'genius.com,localhost,127.0.0.1'

category_match = {
    'frustration': 'hectic',
    'thrilling': 'energetic',
    'confident': 'inspired',
    'neutral': 'reflective',
    'hectic': 'hectic',
    'passionate': 'passionate',
    'eager': 'energetic',
    'animated': 'passionate',
    'fulfilled': 'content',
    'electric': 'passionate',
    'enthusiastic': 'energetic',
    'delightful': 'happy',
    'excited': 'energetic',
    'satisfaction': 'content',
    'curious': 'motivated',
    'content': 'content',
    'pleasing': 'happy',
    'indifferent': 'calm',
    'lukewarm': 'calm',
    'anxious': 'hectic',
    'happy': 'happy',
    'determined': 'inspired',
    'distressed': 'emotional',
    'serious': 'reflective',
    'sorrowful': 'emotional',
    'sad': 'emotional',
    'mild': 'content'
}

playlists = {
    'happy' : [],
    'energetic' : [],
    'motivated' : [],
    'calm' : [],
    'emotional' : [],
    'hectic' : [],
    'content' : [],
    'passionate' : [],
    'reflective' : [],
    'inspired' : []
}

k1 = 1.0
b = 0.9

genius = Genius('HhcPCGMwENzdfMQlauEV1Om0UormkWc6Wrwxri-LFTfBSNkzhwMSVUnR5tZG8eXW')
# genius._session.proxies = {
#     "http": None,
#     "https": None
# }
genius.remove_section_headers = True
genius.skip_non_songs = False
genius.excluded_terms = ["Remix", "Live"]
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours',
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself',
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to',
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most',
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't",
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# with open('../classifications.pkl', 'rb') as f1:
#     classifications = pickle.load(f1)
with open(os.path.join(BASE_DIR, 'big-songs-updated.pkl'), 'rb') as f2:
    big_songs = pickle.load(f2)
with open(os.path.join(BASE_DIR, 'lyrics-updated.pkl'), 'rb') as f:
    song_lyrics = pickle.load(f)

def tokenize(lyrics):
    words = lyrics.lower().split()
    return [word for word in words if word not in stop_words]

def bm25(query, document, doc_length, doc_freqs, avg_doc_length):
    score = 0.0
    query_terms = tokenize(query)
    term_freqs = Counter(document)

    for term in query_terms:
        if term in doc_freqs:  # term must appear in the corpus
            # Calculate BM25 components
            doc_freq = doc_freqs[term]
            idf = math.log((len(big_songs) - doc_freq + 0.5) / (doc_freq + 0.5) + 1)
            term_freq = term_freqs[term]
            term_score = idf * (term_freq * (k1 + 1)) / (term_freq + k1 * (1 - b + b * doc_length / avg_doc_length))
            score += term_score
    return score

@app.route('/')
def base():
    return render_template('base.html', playlists=playlists, ranked_docs=None)

@app.route('/algo/<songName>/<songArtist>')
def algo(songName, songArtist):

    song = genius.search_song(songName, songArtist)
    pos = song.lyrics.find(f'{songName} Lyrics')
    query = song.lyrics[pos:]
    query = query.lower()
    query = ''.join([char if char.isalpha() or char.isspace() else '' for char in query.replace('\n', ' ')])

    tokenized_songs = {}
    for category, all_lyrics in big_songs.items():
        tokenized_songs[category] = tokenize(all_lyrics)

    # calculate document lengths
    doc_lengths = {}
    for  category, all_lyrics in tokenized_songs.items():
        doc_lengths[category] = len(all_lyrics)

    # avg doc length
    avg_doc_length = sum(doc_lengths.values()) / len(doc_lengths)
    doc_freqs = {}
    for doc in tokenized_songs.values():
        unique_terms = set(doc)
        for term in unique_terms:
            doc_freqs[term] = doc_freqs.get(term, 0) + 1

    scores = []
    for doc_id, doc in tokenized_songs.items():
        score = bm25(query, doc, doc_lengths[doc_id], doc_freqs, avg_doc_length)
        scores.append((doc_id, score))

    # Sort documents by score in descending order
    ranked_docs = sorted(scores, key=lambda x: x[1], reverse=True)
    best_category = ranked_docs[0][0]
    ''' either the number one emotion or the emotion with the most matches for the top five categories '''
    top_categories = [category_match[ranked_docs[i][0]] for i in range(min(5, len(ranked_docs)))]
    category_counts = Counter(top_categories)
    most_common_category = category_counts.most_common(1)[0][0]
    category_to_use = most_common_category if category_counts[most_common_category] > 1 else category_match[best_category]
    playlists[category_to_use].append(f'{songName} by {songArtist}')
    # playlists[category_match[best_category]].append(f'{songName} by {songArtist}')
    # print(ranked_docs[0])

    # Display the ranking results
    # print("Document Rankings:")
    # for rank, (doc_id, score) in enumerate(ranked_docs, start=1):
    #     print(f"Rank {rank}: Document {doc_id} with score {score:.4f}")



    return render_template('base.html', playlists=playlists, ranked_docs=ranked_docs, song_name=songName, song_artist=songArtist)

@app.route('/reset_playlists', methods=['POST'])
def reset_playlists():
    global playlists
    # Reset the playlists dictionary
    playlists = {key: [] for key in playlists}
    # return redirect('https://csce470-final.onrender.com/')
    return ''

@app.route("/hello")
def hello_world():
    return render_template('hello.html', person='bruh bruh')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)