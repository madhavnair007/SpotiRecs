from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import spotipy
import os
from cluster_album_api import cluster_album_bp

client_id = "897af16839da440caa6ecefc3b8ea201"
client_secret = "fc01b529cb9941478e039201308bc2f5"

# User data (in a real application, this would be in a database)
users = [
    {"username": "madhav", "password": "123"},
    {"username": "bhuvan", "password": "456"},
    {"username": "brianna", "password": "789"}
]

app = Flask(__name__, static_folder='../frontend')
app.secret_key = 'your-secret-key-here'  # Required for session management
CORS(app, supports_credentials=True)

# Register the cluster album builder blueprint
app.register_blueprint(cluster_album_bp, url_prefix='/cluster_album')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = next((user for user in users if user['username'] == username and user['password'] == password), None)
    
    if user:
        session['user'] = username
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user' in session:
        return jsonify({'authenticated': True, 'username': session['user']})
    return jsonify({'authenticated': False}), 401

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
    print("- POST /login - Login endpoint")
    print("- GET /logout - Logout endpoint")
    print("- GET /check-auth - Check authentication status")
    print("- GET /cluster_album/search_songs?query=<search_term> - Search for songs")
    print("- POST /cluster_album/build_album - Build an album from 3 song indices")
    print("\nAccess the application at: http://localhost:5002")
    app.run(debug=True, port=5002)