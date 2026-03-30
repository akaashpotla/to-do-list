import { useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [health, setHealth] = useState(null);

  const checkHealth = async () => {
    const response = await fetch('http://localhost:8000/health');
    const data = await response.json();
    setHealth(data.status);
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <button className="App-link" onClick={checkHealth}>
          Check Health
        </button>
          Health: {health}
      </header>
    </div>
  );
}

export default App;
