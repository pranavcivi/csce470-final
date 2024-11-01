import pandas as pd
from sklearn.cluster import KMeans


df = pd.read_excel('muse_v3.xlsx', sheet_name='muse_v3')

scores = {}
counts = {}

for index, row in df.iterrows():
    seeds = row['seeds'][1:-1].split(',')
    for seed in seeds:
        if seed not in scores:
            scores[seed] = {}
            scores[seed]['valence'] = row['valence_tags']
            scores[seed]['arousal'] = row['arousal_tags']
            scores[seed]['dominance'] = row['dominance_tags']
            counts[seed] = 1
        else:
            scores[seed]['valence'] += row['valence_tags']
            scores[seed]['arousal'] += row['arousal_tags']
            scores[seed]['dominance'] += row['dominance_tags']
            counts[seed] += 1

for key, value in scores.items():
    scores[key]['valence'] /= counts[key]
    scores[key]['arousal'] /= counts[key]
    scores[key]['dominance'] /= counts[key]

# for key, value in scores.items():
#     print(f'{key}: {value}')

# Step 1: Convert to DataFrame
df = pd.DataFrame(scores).T  # Transpose to get emotions as rows
df.reset_index(inplace=True)
df.rename(columns={'index': 'emotion'}, inplace=True)

# Step 2: Apply KMeans Clustering
kmeans = KMeans(n_clusters=10, random_state=42)  # Choose 10 clusters
df['cluster'] = kmeans.fit_predict(df[['valence', 'arousal', 'dominance']])

# Step 3: View the clusters
print(df[['emotion', 'cluster']])

# Optionally, you can group by the clusters and see the average valence, arousal, dominance per cluster
cluster_summary = df.groupby('cluster')[['valence', 'arousal', 'dominance']].mean()
print(cluster_summary)