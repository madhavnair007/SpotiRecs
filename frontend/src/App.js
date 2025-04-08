import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Recommendation from "./Recommendation";
import AlbumBuilder from "./AlbumBuilder";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/recommendation" element={<Recommendation />} />
                <Route path="/album-builder" element={<AlbumBuilder />} />
                <Route path="*" element={<Login />} /> Default route
            </Routes>
        </Router>
    );
}

export default App;
