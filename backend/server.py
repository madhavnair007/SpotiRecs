from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import spotipy
import os
from cluster_album_api import cluster_album_bp

client_id = "897af16839da440caa6ecefc3b8ea201"
client_secret = "fc01b529cb9941478e039201308bc2f5"


app = Flask(__name__, static_folder='../frontend')
CORS(app)

# Register the cluster album builder blueprint
app.register_blueprint(cluster_album_bp, url_prefix='/cluster_album')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    song_id = data.get('song_id')
    
    recommendation = f"Recommended song for {song_id}: Example Song"

    return jsonify({'recommendation': recommendation})

# Serve frontend files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'recomendation.html')

@app.route('/cluster_album')
def cluster_album():
    return send_from_directory(app.static_folder, 'cluster_album.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    print("Server is running with the following endpoints:")
    print("- GET /cluster_album/search_songs?query=<search_term> - Search for songs")
    print("- POST /cluster_album/build_album - Build an album from 3 song indices")
    print("\nAccess the application at: http://localhost:5002")
    app.run(debug=True, port=5002)