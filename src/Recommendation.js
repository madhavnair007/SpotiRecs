import './Recommendation.css';

function Recommendation() {
    return (
        <body>
        <div>
            <header>
            <h1 class="mainHeading">Recommend a song!</h1>
            </header>
            <div class="container">
                <h2>Input a Song Link</h2>
                <div text-align="center">
                    <input type="text" id="songLink" placeholder="Enter Song Link" />
                </div>
            </div>

            <div class="box">
                <p>Select a Playlist</p>
                <select name="playlist" id="playlist">
                    <option value="playlist1">Playlist1</option>
                    <option value="playlist2">Playlist2</option>
                    <option value="playlist3">Playlist3</option>
                </select>
            </div>


            <button class="btn">Run</button>
        </div>

            

        </body>
    );
}

export default Recommendation;
