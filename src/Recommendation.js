import './Recommendation.css';
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from 'react';

function Recommendation() {
    const [status, setStatus] = useState(null);
    const [isVisible, setIsVisible] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            const data = await new Promise((resolve) => {
                setTimeout(() => resolve('yes'), 1000);
            });
            setStatus(data);
        };

        fetchData();
    }, []);

    // useEffect(() => {
    //     const loggedInUser = localStorage.getItem("loggedInUser");
    //     if (!loggedInUser) {
    //         navigate("/login");
    //     }
    // }, [navigate]);

    // const handleLogout = () => {
    //     localStorage.removeItem("loggedInUser");
    //     navigate("/login");
    // };

    const getStyle = () => {
        if (status === 'yes') {
            return { backgroundColor: 'green', color: 'white', padding: '10px', borderRadius: '5px' };
        } else if (status === 'no') {
            return { backgroundColor: 'red', color: 'white', padding: '10px', borderRadius: '5px' };
        }
        return { backgroundColor: 'gray', color: 'white', padding: '10px', borderRadius: '5px' };
    };

    const handleClick = () => {
        setIsVisible(true);
    };

    return (
        <div className="recommendation-container">
            <header>
                <h1 className="mainHeading">Recommend a song!</h1>
            </header>
            <div className="container">
                <h2>Input a Song Link</h2>
                <div style={{ textAlign: 'center' }}>
                    <input type="text" id="songLink" placeholder="Enter Song Link" />
                </div>
            </div>

            <div className="box">
                <h2>Select a Playlist!</h2>
                <select name="playlist" id="playlist">
                    <option value="playlist1">Playlist1</option>
                    <option value="playlist2">Playlist2</option>
                    <option value="playlist3">Playlist3</option>
                </select>
            </div>

            <button className="btn" onClick={handleClick}>Run</button>

            {isVisible && (
                <div className="container">
                    <div style={{ textAlign: 'center' }}>
                        <div style={getStyle()}>
                            {status === 'yes' ? "We recommend this song!" :
                                status === 'no' ? "We don't recommend this song." : 'Loading...'}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Recommendation;
