from server import app
from cluster_album_api import cluster_album_bp

# Register the cluster album builder blueprint
app.register_blueprint(cluster_album_bp, url_prefix='/cluster_album')

if __name__ == '__main__':
    print("Cluster album builder API registered. The server is now running with the following endpoints:")
    print("- GET /cluster_album/search_songs?query=<search_term> - Search for songs")
    print("- POST /cluster_album/build_album - Build an album from 3 song indices")
    print("\nRun the server with: python server.py") 