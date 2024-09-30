import React, { useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import axios from "axios";
import "./App.css";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [role, setRole] = useState(null);
  const [isRegistering, setIsRegistering] = useState(false); // New state to toggle between login and register

  useEffect(() => {
    if (token) {
      setRole(jwtDecode(token).role);
    }
  }, [token])

  const handleLogin = (token, userRole) => {
    setToken(token);
    setRole(userRole);
    localStorage.setItem("token", token);
  };

  const handleLogout = () => {
    setToken(null);
    setRole(null);
    localStorage.removeItem("token"); // Clear token from storage
  };

  return (
    <div className="app">
      <h1>Document-based GPT System</h1>
      {!token ? (
        isRegistering ? (
          <>
            <Register />
            <p>
              Already registered?{" "}
              <a href="#" onClick={() => setIsRegistering(false)}>
                Click here to login
              </a>
            </p>
          </>
        ) : (
          <>
            <Login onLogin={handleLogin} />
            <p>
              Not registered yet?{" "}
              <a href="#" onClick={() => setIsRegistering(true)}>
                Click here to register
              </a>
            </p>
          </>
        )
      ) : (
        <>
        <p>
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
          </p>
          <ChatBox token={token} />
          {role === "admin" && <UploadDocument token={token} />}
        </>
      )}
    </div>
  );
}

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("user");
  const [adminKey, setAdminKey] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async () => {
    try {
      const payload = { username, password, role };
      if (role === "admin") payload.admin_key = adminKey;

      const response = await axios.post("http://localhost:8000/v1/auth/register/", payload, {
        headers: { "Content-Type": "application/json" },
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Registration failed. " + error.response.data.detail);
    }
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      {role === "admin" && (
        <input placeholder="Admin Key" value={adminKey} onChange={(e) => setAdminKey(e.target.value)} />
      )}
      <button onClick={handleRegister}>Register</button>
      {message && <p>{message}</p>}
    </div>
  );
}

function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const response = await axios.post("http://localhost:8000/v1/auth/token/", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const token = response.data.access_token;
      const userRole = jwtDecode(token).role; // Decode the role from the token
      onLogin(token, userRole);
    } catch (error) {
      console.error("Login failed", error.response.data.detail);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

function ChatBox({ token }) {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  const handleAsk = async () => {
    if (!query.trim()) {
      alert("Please enter a question!");
      return;
    }

    try {
      const result = await axios.post(
        "http://localhost:8000/v1/query/ask/",
        { query },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setResponse(result.data);
    } catch (error) {
      console.error(error.response.data); // Log error for debugging
    }
  };

  return (
    <div className="chat-box">
      <div className="chat-window">
        {response && (
          <div className="response-container">
            <h3>Answer:</h3>
            <div className="response-content">
              <p>{response.answer}</p>
              <h4>Sources:</h4>
              <div className="sources">
                <ul>
                  {response.sources.map((source, index) => (
                    <li key={index} className="source-item">
                      <p><strong>File Path:</strong> {source.file_path}</p>
                      <p><strong>Chunk Index:</strong> {source.chunk_index}</p>
                      <p><strong>Text:</strong> {source.text}</p>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question..."
        />
        <button onClick={handleAsk}>Send</button>
      </div>
    </div>
  );
}

function UploadDocument({ token }) {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const result = await axios.post("http://localhost:8000/v1/document/upload/", formData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessage(result.data.message);
    } catch (error) {
      setMessage("Upload failed. Ensure you're authorized.");
      console.error(error);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Document (Admin Only)</h2>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        accept=".txt"
      />
      <button onClick={handleUpload}>Upload</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
