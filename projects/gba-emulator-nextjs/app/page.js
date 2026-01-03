"use client";
import React, { useState } from 'react';
import EmulatorDisplay from '../components/EmulatorDisplay';

export default function Home() {
  const [romFile, setRomFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('File selected:', file.name, 'Size:', file.size);
      setRomFile(file);
    } else {
      setRomFile(null);
    }
  };

  return (
    <main style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      gap: '20px',
      padding: '20px',
      minHeight: '100vh'
    }}>
      <h1>GameBoy Emulator</h1>
      <p style={{ textAlign: 'center', maxWidth: '600px' }}>
        This emulator supports <strong>GameBoy (.gb)</strong> and <strong>GameBoy Color (.gbc)</strong> ROMs only.
        <br />Note: This does NOT support GBA (Game Boy Advance) ROMs.
      </p>
      
      <div className="file-input">
        <label htmlFor="rom-upload">Load GameBoy ROM:</label>
        <input
          type="file"
          id="rom-upload"
          accept=".gb,.gbc"
          onChange={handleFileChange}
          style={{ marginLeft: '10px' }}
        />
      </div>
      
      <EmulatorDisplay romFile={romFile} />
    </main>
  );
}