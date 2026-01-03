"use client";
import React, { useState, useEffect, useRef } from 'react';

class TetrisAI {
  constructor() {
    this.weights = {
      aggregateHeight: -0.510066,
      completeLines: 0.760666,
      holes: -0.35663,
      bumpiness: -0.184483
    };
  }

  // Tetris piece definitions
  pieces = {
    I: [[[1,1,1,1]]],
    O: [[[1,1],[1,1]]],
    T: [[[0,1,0],[1,1,1]], [[1,0],[1,1],[1,0]], [[1,1,1],[0,1,0]], [[0,1],[1,1],[0,1]]],
    S: [[[0,1,1],[1,1,0]], [[1,0],[1,1],[0,1]]],
    Z: [[[1,1,0],[0,1,1]], [[0,1],[1,1],[1,0]]],
    J: [[[1,0,0],[1,1,1]], [[1,1],[1,0],[1,0]], [[1,1,1],[0,0,1]], [[0,1],[0,1],[1,1]]],
    L: [[[0,0,1],[1,1,1]], [[1,0],[1,0],[1,1]], [[1,1,1],[1,0,0]], [[1,1],[0,1],[0,1]]]
  };

  evaluateBoard(board) {
    const height = this.getAggregateHeight(board);
    const lines = this.getCompleteLines(board);
    const holes = this.getHoles(board);
    const bumpiness = this.getBumpiness(board);
    
    return (
      this.weights.aggregateHeight * height +
      this.weights.completeLines * lines +
      this.weights.holes * holes +
      this.weights.bumpiness * bumpiness
    );
  }

  getAggregateHeight(board) {
    let sum = 0;
    for (let col = 0; col < board[0].length; col++) {
      for (let row = 0; row < board.length; row++) {
        if (board[row][col] !== 0) {
          sum += board.length - row;
          break;
        }
      }
    }
    return sum;
  }

  getCompleteLines(board) {
    let lines = 0;
    for (let row = 0; row < board.length; row++) {
      if (board[row].every(cell => cell !== 0)) {
        lines++;
      }
    }
    return lines;
  }

  getHoles(board) {
    let holes = 0;
    for (let col = 0; col < board[0].length; col++) {
      let blockFound = false;
      for (let row = 0; row < board.length; row++) {
        if (board[row][col] !== 0) {
          blockFound = true;
        } else if (blockFound) {
          holes++;
        }
      }
    }
    return holes;
  }

  getBumpiness(board) {
    const heights = [];
    for (let col = 0; col < board[0].length; col++) {
      for (let row = 0; row < board.length; row++) {
        if (board[row][col] !== 0) {
          heights.push(board.length - row);
          break;
        }
      }
      if (heights.length === col) {
        heights.push(0);
      }
    }
    
    let bumpiness = 0;
    for (let i = 0; i < heights.length - 1; i++) {
      bumpiness += Math.abs(heights[i] - heights[i + 1]);
    }
    return bumpiness;
  }

  findBestMove(board, piece, pieceType) {
    let bestScore = -Infinity;
    let bestMove = null;
    
    const rotations = this.pieces[pieceType] || [piece];
    
    for (let rotation = 0; rotation < rotations.length; rotation++) {
      const rotatedPiece = rotations[rotation];
      
      for (let col = 0; col <= board[0].length - rotatedPiece[0].length; col++) {
        const testBoard = this.simulateDrop(board, rotatedPiece, col);
        if (testBoard) {
          const score = this.evaluateBoard(testBoard);
          if (score > bestScore) {
            bestScore = score;
            bestMove = { rotation, column: col };
          }
        }
      }
    }
    
    return bestMove;
  }

  simulateDrop(board, piece, col) {
    const newBoard = board.map(row => [...row]);
    
    // Find drop position
    let row = 0;
    while (row < board.length - piece.length) {
      if (this.checkCollision(newBoard, piece, row + 1, col)) {
        break;
      }
      row++;
    }
    
    // Place piece
    for (let r = 0; r < piece.length; r++) {
      for (let c = 0; c < piece[r].length; c++) {
        if (piece[r][c] && row + r < newBoard.length && col + c < newBoard[0].length) {
          newBoard[row + r][col + c] = 1;
        }
      }
    }
    
    // Clear complete lines
    for (let r = newBoard.length - 1; r >= 0; r--) {
      if (newBoard[r].every(cell => cell !== 0)) {
        newBoard.splice(r, 1);
        newBoard.unshift(new Array(newBoard[0].length).fill(0));
        r++; // Check the same row again
      }
    }
    
    return newBoard;
  }

  checkCollision(board, piece, row, col) {
    for (let r = 0; r < piece.length; r++) {
      for (let c = 0; c < piece[r].length; c++) {
        if (piece[r][c]) {
          const newRow = row + r;
          const newCol = col + c;
          if (newRow >= board.length || newCol < 0 || newCol >= board[0].length || board[newRow][newCol]) {
            return true;
          }
        }
      }
    }
    return false;
  }
}

export default function TetrisAI({ wasmboyRef, isEnabled }) {
  const [ai] = useState(() => new TetrisAI());
  const [isRunning, setIsRunning] = useState(false);
  const intervalRef = useRef(null);

  const readGameMemory = () => {
    if (!wasmboyRef.current) return null;
    
    try {
      // These memory addresses are examples - you'll need to find the actual addresses for Tetris
      // This requires reverse engineering the Tetris ROM
      const boardAddress = 0xC000; // Example address
      const pieceAddress = 0xC200;  // Example address
      
      // Read board state (20x10 grid)
      const board = [];
      for (let row = 0; row < 20; row++) {
        const boardRow = [];
        for (let col = 0; col < 10; col++) {
          // Read memory byte at calculated address
          const value = wasmboyRef.current.getMemoryValue(boardAddress + (row * 10) + col);
          boardRow.push(value);
        }
        board.push(boardRow);
      }
      
      // Read current piece info
      const pieceType = wasmboyRef.current.getMemoryValue(pieceAddress);
      const pieceX = wasmboyRef.current.getMemoryValue(pieceAddress + 1);
      const pieceY = wasmboyRef.current.getMemoryValue(pieceAddress + 2);
      const pieceRotation = wasmboyRef.current.getMemoryValue(pieceAddress + 3);
      
      return {
        board,
        piece: { type: pieceType, x: pieceX, y: pieceY, rotation: pieceRotation }
      };
    } catch (error) {
      console.error('Error reading game memory:', error);
      return null;
    }
  };

  const sendInput = (key) => {
    if (!wasmboyRef.current) return;
    
    try {
      // Simulate key press
      wasmboyRef.current.pressKey(key);
      setTimeout(() => {
        wasmboyRef.current.releaseKey(key);
      }, 50);
    } catch (error) {
      console.error('Error sending input:', error);
    }
  };

  const runAI = () => {
    const gameState = readGameMemory();
    if (!gameState) return;
    
    const { board, piece } = gameState;
    const bestMove = ai.findBestMove(board, null, piece.type);
    
    if (bestMove) {
      // Rotate piece to desired rotation
      const rotationsNeeded = (bestMove.rotation - piece.rotation + 4) % 4;
      for (let i = 0; i < rotationsNeeded; i++) {
        sendInput('A'); // Rotate button
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      
      // Move piece to desired column
      const movesNeeded = bestMove.column - piece.x;
      const direction = movesNeeded > 0 ? 'RIGHT' : 'LEFT';
      for (let i = 0; i < Math.abs(movesNeeded); i++) {
        sendInput(direction);
        await new Promise(resolve => setTimeout(resolve, 50));
      }
      
      // Drop piece
      sendInput('DOWN');
    }
  };

  useEffect(() => {
    if (isEnabled && isRunning) {
      intervalRef.current = setInterval(runAI, 200); // Run AI every 200ms
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }
    
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isEnabled, isRunning]);

  return (
    <div style={{ marginTop: '20px', padding: '15px', border: '2px solid #4CAF50', borderRadius: '8px' }}>
      <h3>Tetris AI Solver</h3>
      <p style={{ fontSize: '14px', color: '#666' }}>
        This AI will automatically play Tetris by analyzing the board and making optimal moves.
      </p>
      
      <button
        onClick={() => setIsRunning(!isRunning)}
        disabled={!isEnabled}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: isRunning ? '#f44336' : '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: isEnabled ? 'pointer' : 'not-allowed',
          opacity: isEnabled ? 1 : 0.5
        }}
      >
        {isRunning ? 'Stop AI' : 'Start AI'}
      </button>
      
      {!isEnabled && (
        <p style={{ color: '#f44336', fontSize: '12px', marginTop: '10px' }}>
          Load a Tetris ROM to enable the AI solver
        </p>
      )}
    </div>
  );
}