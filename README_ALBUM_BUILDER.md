# Clustering-Based Album Builder

This project provides a web-based interface for building personalized albums based on 3 input songs using unsupervised machine learning (clustering).

## How It Works

The album builder uses K-means clustering to group similar songs together based on their audio features. When you provide 3 songs, the algorithm:

1. Identifies which cluster(s) your input songs belong to
2. Finds songs from the same or similar clusters
3. Ranks these songs by similarity to your input songs
4. Creates a cohesive album that maintains the musical style of your input songs

## Features Used for Clustering

The algorithm uses the following features to determine song similarity:
- **Numerical features**: danceability, energy, tempo, acousticness, valence
- **Categorical features**: genre

## Running the Application

### Prerequisites

- Python 3.6+
- Flask
- Pandas
- NumPy
- Scikit-learn

### Installation

1. Install the required Python packages:
   ```bash
   pip install flask flask-cors pandas numpy scikit-learn
   ```

2. Make sure the `trunc_songs.csv` file is in the root directory of the project.

### Starting the Server

Run the following command to start the server:

```bash
./run_album_builder.sh
```

Or manually:

```bash
python backend/register_cluster_api.py
python backend/server.py
```

### Accessing the Application

Open your web browser and navigate to:
- Main page: `http://localhost:5000/`
- Album Builder: `http://localhost:5000/cluster_album`

## Using the Album Builder

1. **Search for Songs**: Enter a song title or artist name in the search box and click "Search".
2. **Select 3 Songs**: Click "Select" next to the songs you want to include in your album. You must select exactly 3 songs.
3. **Build Your Album**: Click "Build Album" to generate a personalized album based on your selected songs.
4. **Save Your Album**: Click "Save Album" to save your album (placeholder functionality).

## Technical Details

The clustering algorithm automatically determines the optimal number of clusters based on the dataset size. It uses a maximum of 20 clusters or 1 cluster per 50 songs, whichever is smaller.

If there aren't enough songs in the primary cluster, the algorithm will look for songs in nearby clusters to ensure a complete album.

## API Endpoints

The album builder provides the following API endpoints:

1. **Search for songs**:
   ```
   GET /cluster_album/search_songs?query=<search_term>
   ```
   Returns a list of songs matching the search term.

2. **Build an album**:
   ```
   POST /cluster_album/build_album
   ```
   Request body:
   ```json
   {
     "song_indices": [123, 456, 789],
     "num_songs": 10
   }
   ```
   Returns a list of songs that form the album. 