from flask import Blueprint, request, jsonify
import pandas as pd
from cluster_album_builder import build_album_from_songs, get_album_details, search_songs

# Create a Blueprint for the cluster album builder API
cluster_album_bp = Blueprint('cluster_album', __name__)

@cluster_album_bp.route('/search_songs', methods=['GET'])
def api_search_songs():
    """
    Search for songs in the dataset based on a query string.
    """
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    try:
        results = search_songs(query)
        
        # Convert to list of dictionaries for JSON response
        songs = []
        for _, row in results.iterrows():
            songs.append({
                'index': int(row['index']),
                'artist_name': row['artist_name'],
                'track_name': row['track_name'],
                'genre': row['genre'],
                'year': int(row['year'])
            })
        
        return jsonify({'songs': songs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cluster_album_bp.route('/build_album', methods=['POST'])
def api_build_album():
    """
    Build an album based on 3 input songs using clustering.
    """
    data = request.json
    song_indices = data.get('song_indices', [])
    num_songs = data.get('num_songs', 10)
    exclude_input_songs = data.get('exclude_input_songs', False)
    artist_filter = data.get('artist_filter', 'all')
    
    if len(song_indices) != 3:
        return jsonify({'error': 'Exactly 3 song indices are required'}), 400
    
    try:
        # Build the album
        album_indices = build_album_from_songs(song_indices, num_songs, exclude_input_songs, artist_filter)
        album_details = get_album_details(album_indices)
        
        # Convert to list of dictionaries for JSON response
        album = []
        for idx, row in album_details.iterrows():
            album.append({
                'artist_name': row['artist_name'],
                'track_name': row['track_name'],
                'genre': row['genre'],
                'year': int(row['year'])
            })
        
        return jsonify({'album': album})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 