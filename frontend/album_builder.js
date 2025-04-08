// Store selected songs
let selectedSongs = [];
let currentSearchResults = [];
let currentFilters = {
    genre: 'all',
    artist: 'all'
};

// Get selected songs
function getSelectedSongs() {
    return selectedSongs.map(song => song.index);
}

// Display album
function displayAlbum(album) {
    const albumResult = document.getElementById("albumResult");
    albumResult.innerHTML = "";
    
    album.forEach((song, index) => {
        const songCard = document.createElement("div");
        songCard.className = "song-card album-song";
        
        const songInfo = document.createElement("div");
        songInfo.className = "song-info";
        songInfo.innerHTML = `
            <div class="song-title">${index + 1}. ${song.track_name}</div>
            <div class="song-artist">${song.artist_name}</div>
            <div class="song-genre">${song.genre} (${song.year})</div>
        `;
        
        songCard.appendChild(songInfo);
        albumResult.appendChild(songCard);
    });
    
    document.getElementById("albumBox").style.display = "block";
}

// Build album
async function buildAlbum() {
    const selectedSongs = getSelectedSongs();
    if (selectedSongs.length !== 3) {
        alert('Please select exactly 3 songs to build an album.');
        return;
    }

    const numSongs = document.getElementById('num-songs').value;
    const excludeInputSongs = document.getElementById('exclude-input-songs').checked;
    const artistFilter = document.getElementById('artist-filter').value;

    try {
        const response = await fetch('/api/cluster_album/build_album', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                song_indices: selectedSongs,
                num_songs: parseInt(numSongs),
                exclude_input_songs: excludeInputSongs,
                artist_filter: artistFilter
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to build album');
        }

        const data = await response.json();
        displayAlbum(data.album);
    } catch (error) {
        console.error('Error building album:', error);
        alert('Failed to build album. Please try again.');
    }
} 