import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

const users = [
  { username: "madhav", password: "123" },
  { username: "bhuvan", password: "456" },
  { username: "brianna", password: "789" }
];

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // useEffect(() => {
  //   const storedUser = localStorage.getItem("loggedInUser");
  //   if (storedUser) {
  //     navigate("/recommendation");
  //   }
  // }, [navigate]);

  const handleLogin = (e) => {
    e.preventDefault();

    const validUser = users.find(
      (user) => user.username === username && user.password === password
    );

    if (validUser) {
      setError("");
      // localStorage.setItem("loggedInUser", username);
      navigate("/recommendation");
    } else {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="login-container">
      <div className="glass-container">
        <div className="login-box">
          <h2>Login</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Email or Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && <p style={{ color: "red", marginTop: "5px" }}>{error}</p>}
            <button type="submit">Login</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
