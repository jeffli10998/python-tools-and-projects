// components/GameControls.js
import React from 'react';

const GameControls = ({ onRomLoad, onPause, onReset }) => {
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      onRomLoad(file);
    }
  };

  return (
    <div>
      <h4>Game Controls</h4>
      <input type="file" accept=".gba" onChange={handleFileChange} />
      <button onClick={onPause} style={{ marginLeft: '10px' }}>Pause/Resume</button>
      <button onClick={onReset} style={{ marginLeft: '10px' }}>Reset</button>
      {/* Add more controls as needed: save state, load state, volume, etc. */}
    </div>
  );
};

export default GameControls; // Ensure only one export