import React, { useState, useEffect } from "react";

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';


export default function Stopwatch() {
  // state to store time
  const [time, setTime] = useState(0);

  // state to check stopwatch running or not
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    let intervalId;
    if (isRunning) {
      // setting time from 0 to 1 every 10 milisecond using javascript setInterval method
      intervalId = setInterval(() => setTime(time + 1), 10);
    }
    return () => clearInterval(intervalId);
  }, [isRunning, time]);

  // Hours calculation
  const hours = Math.floor(time / 360000);

  // Minutes calculation
  const minutes = Math.floor((time % 360000) / 6000);

  // Seconds calculation
  const seconds = Math.floor((time % 6000) / 100);

  // Milliseconds calculation
  const milliseconds = time % 100;

  // Method to start and stop timer
  const startAndStop = () => {
    setIsRunning(!isRunning);
  };

  const BorderBox = ({ children }) => {
    return (
        <div
            sx={{
                border: '1px solid',
                borderRadius: '4px',
                borderColor: 'lightgrey',
                padding: '4px',
                m: 2,
            }}
        >
            {children}
        </div>
    );
    }

  // Method to reset timer back to 0
  const reset = () => {
    setTime(0);


    
  };
  return (
    <Box>
      <Typography sx={'text-align: center, color: #fff, font-size: 120px;'}
      fontSize={72}>
        {hours}:{minutes.toString().padStart(2, "0")}:
        {seconds.toString().padStart(2, "0")}:
        {milliseconds.toString().padStart(2, "0")}
      </Typography>
      <Box direction="column"
      alignItems="center"
      justify="center">
        <Button onClick={startAndStop} sx={'margin: 20px, border: none,  padding: 10px 30px, cursor: pointer, color: green;'}
        variant = "contained">
          {isRunning ? "Stop" : "Start"}
        </Button>
        <Button 
        variant="contained"
        color="error"
        onClick={reset}>
          Reset
        </Button>
      </Box>
    </Box>
  );
};