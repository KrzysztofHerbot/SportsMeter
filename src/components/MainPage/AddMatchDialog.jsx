import React from 'react';

import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogActions from '@mui/material/DialogActions';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';

import axios from 'axios';

export default function AddMatchDialog({isOpen, handleClose, selectedSeason}) {

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event?.currentTarget);
        axios.post(`/api/seasons/${selectedSeason}/matches`, {
            match_title: data.get('match_title')
        }).then(() => {
            handleClose(true);
        }).catch((error) => {
            console.log(error);
            handleClose(false);
        });
    }

    return (
    <Dialog open={isOpen} onClose={handleClose}>
        <DialogTitle>Add new match</DialogTitle>
        <DialogContent>
            <DialogContentText>
                Please provide match details below and it will be added to selected season.
            </DialogContentText>
            <Box
                component="form"
                noValidate
                autoComplete="off"
                id="addMatchForm"
                onSubmit={handleSubmit}
            >
                <>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="match_title"
                        label="Match title"
                        name="match_title"
                        autoComplete="title"
                        autoFocus
                    />
                </>
            </Box>
        </DialogContent>
        <DialogActions>
            <Button onClick={() => handleClose(false)}>Cancel</Button>
            <Button type="submit" form="addMatchForm">Add</Button>
        </DialogActions>
    </Dialog>
    );
}
