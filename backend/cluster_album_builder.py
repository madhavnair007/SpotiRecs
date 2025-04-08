import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


def build_album_from_songs(input_song_indices, num_songs=10):
    """
    Build an album based on 3 input songs using clustering.
    
    Args:
        input_song_indices: List of 3 song indices from the dataset
        num_songs: Number of songs to include in the album (default: 10)
        
    Returns:
        List of song indices that form the album
    """
    # Load the dataset
    df = pd.read_csv('trunc_songs.csv')
    
    numerical_features = ["danceability", "energy", "tempo", "acousticness", "valence"]
    categorical_features = ["genre"]
    
    # Preprocess the data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )
    

    song_vectors = preprocessor.fit_transform(df)
    

    n_clusters = min(20, len(df) // 50)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(song_vectors)
    

    input_clusters = df.iloc[input_song_indices]['cluster'].values
    

    avg_cluster = int(np.mean(input_clusters))
    

    cluster_songs = df[df['cluster'] == avg_cluster].index.tolist()
    

    if len(cluster_songs) < num_songs:
        
        all_clusters = df['cluster'].unique()
        cluster_distances = [abs(c - avg_cluster) for c in all_clusters]
        sorted_clusters = [x for _, x in sorted(zip(cluster_distances, all_clusters))]
        

        for cluster in sorted_clusters:
            if cluster != avg_cluster:
                additional_songs = df[df['cluster'] == cluster].index.tolist()
                cluster_songs.extend(additional_songs)
                if len(cluster_songs) >= num_songs:
                    break
    

    similarity_matrix = cosine_similarity(song_vectors)
    

    avg_similarities = np.mean([similarity_matrix[idx] for idx in input_song_indices], axis=0)
    

    cluster_similarities = avg_similarities[cluster_songs]
    
    # Get the most similar songs
    most_similar_indices = np.argsort(cluster_similarities)[::-1][:num_songs]
    album_indices = [cluster_songs[idx] for idx in most_similar_indices]
    

    for idx in input_song_indices:
        if idx not in album_indices:
            album_indices.append(idx)
    
    return album_indices


def get_album_details(album_indices):
    
    df = pd.read_csv('trunc_songs.csv')
    album_df = df.iloc[album_indices][['artist_name', 'track_name', 'genre', 'year']]
    return album_df


def search_songs(query):
   
    df = pd.read_csv('trunc_songs.csv')
    query = query.lower()
    
    # Search in both track_name and artist_name
    mask = (
        df['track_name'].str.lower().str.contains(query, na=False) |
        df['artist_name'].str.lower().str.contains(query, na=False)
    )
    
    return df[mask][['artist_name', 'track_name', 'genre', 'year']].reset_index()


def select_songs():
    
    selected_songs = []
    
    print("Welcome to the Album Builder!")
    print("You'll select 3 songs to build an album around.")
    
    while len(selected_songs) < 3:
        print(f"\nSelect song {len(selected_songs) + 1}/3:")
        query = input("Enter a song title or artist name to search: ")
        
        if not query.strip():
            print("Please enter a valid search term.")
            continue
        
        results = search_songs(query)
        
        if results.empty:
            print("No songs found. Try a different search term.")
            continue
        
        print("\nSearch results:")
        for i, (_, row) in enumerate(results.iterrows()):
            print(f"{i+1}. {row['artist_name']} - {row['track_name']} ({row['genre']}, {row['year']})")
        
        try:
            choice = int(input("\nEnter the number of the song you want to select (or 0 to search again): "))
            if choice == 0:
                continue
            if 1 <= choice <= len(results):
                song_idx = results.iloc[choice-1]['index']
                if song_idx not in selected_songs:
                    selected_songs.append(song_idx)
                    print(f"Added: {results.iloc[choice-1]['artist_name']} - {results.iloc[choice-1]['track_name']}")
                else:
                    print("You've already selected this song. Please choose a different one.")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    return selected_songs


def main():
    # Let the user select 3 songs
    input_songs = select_songs()
    
    # Build the album
    print("\nBuilding your album...")
    album_indices = build_album_from_songs(input_songs)
    album_details = get_album_details(album_indices)
    
    # Display the album
    print("\nYour personalized album:")
    print("-" * 50)
    for idx, row in album_details.iterrows():
        print(f"{row['artist_name']} - {row['track_name']} ({row['genre']}, {row['year']})")
    print("-" * 50)
    
    # Ask if the user wants to save the album
    save = input("\nWould you like to save this album? (y/n): ").lower()
    if save == 'y':
        filename = input("Enter a filename to save the album (default: my_album.csv): ") or "my_album.csv"
        album_details.to_csv(filename, index=False)
        print(f"Album saved to {filename}")


if __name__ == "__main__":
    main() 