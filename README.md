# SpotiRecs

Madhav Nair, Bhuvan Hospet, Brianna Quinn

SpotiRecs is a full-stack web application that analyzes a user's inputed song(s) and recommends new songs that match the "vibe" using a machine learning model. Built with React, Flask, and the Spotify API.

## How it works
This project provides a web interface to build custom albums based on user-selected songs. It uses **K-Means clustering** on audio features to find and rank songs that are sonically and stylistically similar.

The clustering engine:
1. Identifies the cluster(s) your input songs belong to.
2. Finds other songs in the same or related clusters.
3. Ranks them by feature similarity to your input.
4. Returns a playlist-like album of coherent, similar songs.

## Features Used for Clustering
- **Numerical**: `danceability`, `energy`, `tempo`, `acousticness`, `valence`
- **Categorical**: `genre`

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