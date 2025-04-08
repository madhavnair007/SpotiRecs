# Clustering-Based Album Builder

This module provides functionality to build personalized albums based on 3 input songs using unsupervised machine learning (clustering).

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

## Usage

### Command Line Interface

Run the album builder from the command line:

```bash
python cluster_album_builder.py
```

This will guide you through selecting 3 songs to build an album around.

### API Endpoints

The album builder also provides API endpoints that can be integrated with a web application:

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

## Integration with Existing Server

To integrate the album builder with the existing server, run:

```bash
python register_cluster_api.py
```

This will register the album builder API endpoints with the Flask application.

## Technical Details

The clustering algorithm automatically determines the optimal number of clusters based on the dataset size. It uses a maximum of 20 clusters or 1 cluster per 50 songs, whichever is smaller.

If there aren't enough songs in the primary cluster, the algorithm will look for songs in nearby clusters to ensure a complete album. 