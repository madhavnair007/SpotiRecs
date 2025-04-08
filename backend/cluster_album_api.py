from flask import Blueprint, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import cosine_similarity

cluster_album_bp = Blueprint('cluster_album', __name__)

# Load the dataset once when the blueprint is created
df = pd.read_csv('trunc_songs.csv')

@cluster_album_bp.route('/search_songs', methods=['GET'])
def search_songs():
    query = request.args.get('query', '').lower()
    if not query:
        return jsonify({'error': 'No search query provided'}), 400

    # Search in both track_name and artist_name
    matches = df[
        df['track_name'].str.lower().str.contains(query) |
        df['artist_name'].str.lower().str.contains(query)
    ]

    # Limit to first 20 matches
    matches = matches.head(20)

    # Convert matches to list of dictionaries
    songs = matches.apply(lambda row: {
        'index': row.name,
        'track_name': row['track_name'],
        'artist_name': row['artist_name'],
        'genre': row['genre'],
        'year': int(row['year'])
    }, axis=1).tolist()

    return jsonify({'songs': songs})

@cluster_album_bp.route('/build_album', methods=['POST'])
def build_album():
    data = request.json
    song_indices = data.get('song_indices', [])
    num_songs = data.get('num_songs', 10)
    
    if not song_indices:
        return jsonify({'error': 'No song indices provided'}), 400

    try:
        # Define features for clustering
        numerical_features = ["danceability", "energy", "tempo", "acousticness", "valence"]
        categorical_features = ["genre"]
        
        # Create preprocessor
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(), categorical_features)
            ]
        )
        
        # Transform the data
        song_vectors = preprocessor.fit_transform(df)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(song_vectors)
        
        # Get similarities to input songs
        similarities = similarity_matrix[song_indices].mean(axis=0)
        
        # Get most similar songs (excluding input songs)
        most_similar_indices = []
        for idx in similarities.argsort()[::-1]:
            if idx not in song_indices and len(most_similar_indices) < num_songs:
                most_similar_indices.append(idx)
        
        # Get album details
        album_songs = df.iloc[most_similar_indices].apply(lambda row: {
            'track_name': row['track_name'],
            'artist_name': row['artist_name'],
            'genre': row['genre'],
            'year': int(row['year'])
        }, axis=1).tolist()

        return jsonify({'album': album_songs})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 