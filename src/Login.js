import './Login.css';

function Login() {
  return (
    <body>
      <div class="glass-container">
        <div class="login-box">
          <h2>Login</h2>
          <form action="#" method="POST">
            <input type="text" id="username" name="username" required placeholder="Email or Username" />
            <input type="password" id="password" name="password" required placeholder="Password" />
            <div class="options">
              <input type="checkbox" id="remember" name="remember" />
              <label for="remember">Remember me</label>
              <button type="button" class="link-button">Forgot Password?</button>
            </div>
            <button type="submit">Login</button>
            <p>Don't have an account? <button id="register" class="link-button">Register</button></p>
          </form>
        </div>
      </div>
    </body>
  );
}

export default Login;
