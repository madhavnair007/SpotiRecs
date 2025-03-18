from flask import Flask, request, jsonify
from flask_cors import CORS

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