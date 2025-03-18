import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('trunc_songs.csv')

numerical_features = ["danceability", "energy", "tempo", "acousticness", "valence"]
categorical_features = ["genre"]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ]
)

song_vectors = preprocessor.fit_transform(df)

# print(song_vectors.shape)

similarity_matrix = cosine_similarity(song_vectors)

input_index = 0
similarities = similarity_matrix[input_index]

most_similar_idx = np.argsort(similarities)[::-1][1]

print("Most similar song index:", df["track_name"][most_similar_idx])