import './Recommendation.css';
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from 'react';

function Recommendation() {
    const [isVisible, setIsVisible] = useState(false);
    const [recommendation, setRecommendation] = useState('');
    const [inputValue, setInputValue] = useState('');

    const handleClick = () => {
        if (inputValue.trim === '') {
            setRecommendation(['Enter a song link.']);
        } else {
          setRecommendation(["Song 1", "Song 2", "Song 3"]);  
        }
        setIsVisible(true);  
    };

    return (
        <div className="recommendation-container">
            <header>
                <h1 className="mainHeading">Recommend a song!</h1>
            </header>

            <div className="container">
                <h2>Input a Song Link</h2>
                <input
                    type="text"
                    id="songLink"
                    placeholder="Enter Song Link"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                />
                <button className="btn" onClick={handleClick}>Run</button>
            </div>

            {isVisible && (
                <div className="box">
                    <p>Recommended Songs:</p>
                    <ul className="recommendation-list">
                        {recommendation.map((song, index) => (
                            <li key={index}>{song}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default Recommendation;
