import { useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import './AlbumBuilder.css';

function AlbumBuilder() {
    const [selectedSongs, setSelectedSongs] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [searchResults, setSearchResults] = useState([]);
    const [album, setAlbum] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = useCallback(async () => {
        if (!searchQuery.trim()) {
            setError('Please enter a search term');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch(`/api/cluster_album/search_songs?query=${encodeURIComponent(searchQuery)}`);
            const data = await response.json();
            
            if (data.error) {
                setError(data.error);
                return;
            }
            
            setSearchResults(data.songs || []);
        } catch (error) {
            setError('Error searching for songs');
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    }, [searchQuery]);

    const handleSongSelect = useCallback((song) => {
        setSelectedSongs(prev => {
            const isSelected = prev.find(s => s.index === song.index);
            if (isSelected) {
                return prev.filter(s => s.index !== song.index);
            }
            if (prev.length < 3) {
                return [...prev, song];
            }
            alert('You can only select 3 songs. Remove one first.');
            return prev;
        });
    }, []);

    const buildAlbum = useCallback(async () => {
        if (selectedSongs.length !== 3) {
            setError('Please select exactly 3 songs');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const response = await fetch('/api/cluster_album/build_album', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    song_indices: selectedSongs.map(song => song.index),
                    num_songs: 10
                }),
            });

            const data = await response.json();
            if (data.error) {
                setError(data.error);
                return;
            }

            setAlbum(data.album);
        } catch (error) {
            setError('Error building album');
            console.error(error);
        } finally {
            setIsLoading(false);
        }
    }, [selectedSongs]);

    return (
        <div className="album-builder">
            <header>
                <h1 className="mainHeading">Album Builder</h1>
                <p className="subtitle">Create a personalized album based on 3 songs you love</p>
                <Link to="/recommendation" className="nav-link">
                    Back to Song Recommendation
                </Link>
            </header>

            <div className="container">
                {error && (
                    <div className="error-message">{error}</div>
                )}

                <div className="step-container">
                    <h2 className="step-title">Step 1: Search for Songs</h2>
                    <p className="step-description">Search for songs by title or artist name</p>
                    <div className="search-box">
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Enter song title or artist name"
                            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                        />
                        <button 
                            className="btn" 
                            onClick={handleSearch}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Searching...' : 'Search'}
                        </button>
                    </div>
                    <div className="search-results">
                        {searchResults.map(song => (
                            <div key={song.index} className="song-card">
                                <div className="song-info">
                                    <div className="song-title">{song.track_name}</div>
                                    <div className="song-artist">{song.artist_name}</div>
                                    <div className="song-genre">{song.genre} ({song.year})</div>
                                </div>
                                <button 
                                    className="btn"
                                    onClick={() => handleSongSelect(song)}
                                >
                                    {selectedSongs.find(s => s.index === song.index) ? 'Remove' : 'Select'}
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="step-container">
                    <h2 className="step-title">Step 2: Selected Songs ({selectedSongs.length}/3)</h2>
                    <div className="selected-songs">
                        {selectedSongs.map(song => (
                            <div key={song.index} className="song-card selected-song">
                                <div className="song-info">
                                    <div className="song-title">{song.track_name}</div>
                                    <div className="song-artist">{song.artist_name}</div>
                                    <div className="song-genre">{song.genre} ({song.year})</div>
                                </div>
                                <button 
                                    className="btn"
                                    onClick={() => handleSongSelect(song)}
                                >
                                    Remove
                                </button>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="step-container">
                    <h2 className="step-title">Step 3: Build Your Album</h2>
                    <button 
                        className="btn"
                        onClick={buildAlbum}
                        disabled={selectedSongs.length !== 3 || isLoading}
                    >
                        {isLoading ? 'Building...' : 'Build Album'}
                    </button>
                </div>

                {album && (
                    <div className="album-container">
                        <h2>Your Personalized Album</h2>
                        <div className="album-songs">
                            {album.map((song, index) => (
                                <div key={index} className="song-card album-song">
                                    <div className="song-info">
                                        <div className="song-title">{index + 1}. {song.track_name}</div>
                                        <div className="song-artist">{song.artist_name}</div>
                                        <div className="song-genre">{song.genre} ({song.year})</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default AlbumBuilder; 