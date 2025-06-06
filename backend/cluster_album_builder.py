import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity


def build_album_from_songs(input_song_indices, num_songs=10, exclude_input_songs=False, artist_filter='all'):
    """
    Build an album based on 3 input songs using clustering.
    
    Args:
        input_song_indices: List of 3 song indices from the dataset
        num_songs: Number of songs to include in the album (default: 10)
        exclude_input_songs: Whether to exclude the input songs from the album (default: False)
        artist_filter: Filter for artists in the album ('all', 'same', or 'different')
        
    Returns:
        List of song indices that form the album
    """
    # Load the dataset
    df = pd.read_csv('trunc_songs.csv')
    
    # Define features for clustering
    numerical_features = ["danceability", "energy", "tempo", "acousticness", "valence"]
    categorical_features = ["genre"]
    
    # Preprocess the data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )
    
    # Transform the data
    song_vectors = preprocessor.fit_transform(df)
    
    # Perform K-means clustering
    # We'll use a reasonable number of clusters based on the dataset size
    n_clusters = min(20, len(df) // 50)  # Ensure we don't have too many clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(song_vectors)
    
    # Find the clusters of the input songs
    input_clusters = df.iloc[input_song_indices]['cluster'].values
    
    # Calculate the average cluster of the input songs
    avg_cluster = int(np.mean(input_clusters))
    
    # Get songs from the same cluster as the input songs
    cluster_songs = df[df['cluster'] == avg_cluster].index.tolist()
    
    # If we don't have enough songs in the cluster, get songs from nearby clusters
    if len(cluster_songs) < num_songs:
        # Get songs from clusters that are close to the input clusters
        all_clusters = df['cluster'].unique()
        cluster_distances = [abs(c - avg_cluster) for c in all_clusters]
        sorted_clusters = [x for _, x in sorted(zip(cluster_distances, all_clusters))]
        
        # Add songs from nearby clusters until we have enough
        for cluster in sorted_clusters:
            if cluster != avg_cluster:
                additional_songs = df[df['cluster'] == cluster].index.tolist()
                cluster_songs.extend(additional_songs)
                if len(cluster_songs) >= num_songs:
                    break
    
    # Calculate similarity scores for all songs in the cluster
    similarity_matrix = cosine_similarity(song_vectors)
    
    # Calculate average similarity to input songs
    avg_similarities = np.mean([similarity_matrix[idx] for idx in input_song_indices], axis=0)
    
    # Filter to only include songs in our clusters
    cluster_similarities = avg_similarities[cluster_songs]
    
    # Get the most similar songs
    most_similar_indices = np.argsort(cluster_similarities)[::-1][:num_songs]
    album_indices = [cluster_songs[idx] for idx in most_similar_indices]
    
    # Apply artist filtering to the album songs
    if artist_filter != 'all':
        # Get the artists of the input songs
        input_artists = set()
        for idx in input_song_indices:
            artist_name = df.iloc[idx]['artist_name'].lower()
            input_artists.add(artist_name)
        
        # Filter album songs based on artist filter
        filtered_album_indices = []
        for idx in album_indices:
            artist_name = df.iloc[idx]['artist_name'].lower()
            
            if artist_filter == 'same' and artist_name in input_artists:
                filtered_album_indices.append(idx)
            elif artist_filter == 'different' and artist_name not in input_artists:
                filtered_album_indices.append(idx)
        
        # If we don't have enough songs after filtering, add more from the original list
        if len(filtered_album_indices) < num_songs:
            # Add songs from the original list that weren't filtered out
            for idx in album_indices:
                if idx not in filtered_album_indices:
                    filtered_album_indices.append(idx)
                    if len(filtered_album_indices) >= num_songs:
                        break
        
        album_indices = filtered_album_indices[:num_songs]
    
    # Ensure input songs are included in the album (unless exclude_input_songs is True)
    if not exclude_input_songs:
        for idx in input_song_indices:
            if idx not in album_indices:
                album_indices.append(idx)
    
    return album_indices


def get_album_details(album_indices):
    """
    Get details of the songs in the album.
    
    Args:
        album_indices: List of song indices
        
    Returns:
        DataFrame with album details
    """
    df = pd.read_csv('trunc_songs.csv')
    album_df = df.iloc[album_indices][['artist_name', 'track_name', 'genre', 'year']]
    return album_df


def search_songs(query):
    """
    Search for songs in the dataset based on a query string.
    
    Args:
        query: String to search for in song titles or artist names
        
    Returns:
        DataFrame with matching songs
    """
    df = pd.read_csv('trunc_songs.csv')
    query = query.lower()
    
    # Search in both track_name and artist_name
    mask = (
        df['track_name'].str.lower().str.contains(query, na=False) |
        df['artist_name'].str.lower().str.contains(query, na=False)
    )
    
    return df[mask][['artist_name', 'track_name', 'genre', 'year']].reset_index()


def select_songs():
    """
    Interactive function to let the user select 3 songs.
    
    Returns:
        List of 3 song indices
    """
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