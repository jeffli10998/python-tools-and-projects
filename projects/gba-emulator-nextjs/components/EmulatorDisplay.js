"use client";
import React, { useRef, useEffect, useState } from 'react';

export default function EmulatorDisplay({ romFile }) {
  const canvasRef = useRef(null);
  const wasmboyRef = useRef(null);
  const [isInitialized, setIsInitialized] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('Initializing...');

  useEffect(() => {
    if (typeof window !== 'undefined' && canvasRef.current && !isInitialized) {
      setStatus('Loading WasmBoy...');
      
      import('wasmboy').then(({ WasmBoy }) => {
        console.log('WasmBoy module loaded:', WasmBoy);
        
        const WasmBoyOptions = {
          headless: false,
          useGbcWhenOptional: true,
          isAudioEnabled: true,
          frameSkip: 1,
          audioBatchProcessing: true,
          timersBatchProcessing: false,
          audioAccumulateSamples: true,
          graphicsBatchProcessing: false,
          graphicsDisableScanlineRendering: false,
          tileRendering: true,
          tileCaching: true,
          gameboyFPSCap: 60
        };

        setStatus('Configuring emulator...');
        
        WasmBoy.config(WasmBoyOptions, canvasRef.current)
          .then(() => {
            console.log('WasmBoy configured successfully!');
            wasmboyRef.current = WasmBoy;
            setIsInitialized(true);
            setStatus('Ready - Load a GameBoy ROM file');
            setError(null);
          })
          .catch((error) => {
            console.error('Error configuring WasmBoy:', error);
            setError(`Configuration error: ${error.message}`);
            setStatus('Configuration failed');
          });
      }).catch(err => {
        console.error('Failed to load WasmBoy module:', err);
        setError(`Module loading error: ${err.message}`);
        setStatus('Module loading failed');
      });
    }
  }, [isInitialized]);

  useEffect(() => {
    if (romFile && wasmboyRef.current && isInitialized) {
      console.log('Loading ROM file:', romFile.name, 'Size:', romFile.size, 'Type:', romFile.type);
      setStatus(`Loading ${romFile.name}...`);
      
      // Check if it's a valid GameBoy ROM file
      if (!romFile.name.toLowerCase().endsWith('.gb') && !romFile.name.toLowerCase().endsWith('.gbc')) {
        setError('Invalid file type. Please select a .gb or .gbc file.');
        setStatus('Invalid file type');
        return;
      }
      
      wasmboyRef.current.loadROM(romFile)
        .then(() => {
          console.log('ROM loaded successfully');
          setStatus('ROM loaded - Starting game...');
          return wasmboyRef.current.play();
        })
        .then(() => {
          console.log('Game started!');
          setStatus('Playing');
          setError(null);
        })
        .catch((error) => {
          console.error('Error loading or playing ROM:', error);
          setError(`ROM error: ${error ? error.message : 'Unknown error'}`);
          setStatus('ROM loading failed');
        });
    }
  }, [romFile, isInitialized]);

  return (
    <div className="emulator-container" style={{ textAlign: 'center', width: '100%', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: '15px' }}>
        <strong>Status:</strong> {status}
        {error && (
          <div style={{ color: 'red', marginTop: '5px' }}>
            <strong>Error:</strong> {error}
          </div>
        )}
      </div>
      
      <canvas 
        ref={canvasRef} 
        width={160} 
        height={144}
        style={{
          border: '3px solid #333',
          imageRendering: 'pixelated',
          width: 'min(80vw, 800px)', // Responsive: 80% of viewport width, max 800px
          height: 'min(72vw, 720px)', // Maintains 160:144 aspect ratio
          backgroundColor: '#000',
          display: 'block',
          margin: '0 auto',
          borderRadius: '8px',
          boxShadow: '0 4px 20px rgba(0, 0, 0, 0.3)'
        }}
      />
      
      <div style={{ marginTop: '15px', fontSize: '14px', color: '#666' }}>
        GameBoy Resolution: 160x144 (Auto-scaled for your screen)
      </div>
      
      {wasmboyRef.current && (
        <div style={{ marginTop: '20px' }}>
          <button 
            onClick={() => wasmboyRef.current.pause()}
            style={{ 
              margin: '0 8px', 
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: '#f44336',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Pause
          </button>
          <button 
            onClick={() => wasmboyRef.current.play()}
            style={{ 
              margin: '0 8px', 
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Play
          </button>
          <button 
            onClick={() => wasmboyRef.current.reset()}
            style={{ 
              margin: '0 8px', 
              padding: '10px 20px',
              fontSize: '16px',
              backgroundColor: '#2196F3',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Reset
          </button>
        </div>
      )}
    </div>
  );
}