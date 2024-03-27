import React from 'react';

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Toolbar from '@mui/material/Toolbar';

import { useNavigate } from 'react-router-dom';

export default function NavigationBar() {
    const navigate = useNavigate();

    return (
        <AppBar position="static">
            <Toolbar>
                <Box sx={{ flexGrow: 1}}>
                    <Typography variant="h6" sx={{ width: '10%'}} onClick={() => navigate("/")} className="cursor-item">
                        Sports Meter
                    </Typography>
                </Box>
                <Button color="inherit">Login</Button>
            </Toolbar>
        </AppBar>
    )
}
