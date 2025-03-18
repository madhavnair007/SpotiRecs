from flask import Flask, request, jsonify
from flask_cors import CORS
import spotipy
client_id = "897af16839da440caa6ecefc3b8ea201"
client_secret = "fc01b529cb9941478e039201308bc2f5"


app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    song_id = data.get('song_id')
    
    recommendation = f"Recommended song for {song_id}: Example Song"

    return jsonify({'recommendation': recommendation})

if __name__ == '__main__':
    app.run(debug=True)