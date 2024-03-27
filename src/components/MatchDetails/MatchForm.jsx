import React from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';

export default function MatchForm({setMatchDetails, setIsEditing}) {
    const navigate = useNavigate();
    const { match_id } = useParams();

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event?.currentTarget);
        axios.put(`/api/matches/${match_id}`, {
            match_title: data.get('match_title')
        }).then((response) => {
            setMatchDetails(response?.data);
            setIsEditing(false);
        }).catch((error) => {
            console.log(error);
            navigate("/");
        });
    }

    return (
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 3 }}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <TextField
                        autoComplete="match_title"
                        name="match_title"
                        required
                        fullWidth
                        id="match-title"
                        label="Match title"
                        autoFocus
                    />
                </Grid>
            </Grid>
            <Button
                type="submit"
                variant="contained"
                color="success"
            >
                Save
            </Button>
            <Button
                variant="outlined"
                color="error"
                onClick={() => setIsEditing(false)}
            >
                Cancel
            </Button>
        </Box>
    )
}
