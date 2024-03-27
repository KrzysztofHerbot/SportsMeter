import React from 'react';
import { useNavigate } from 'react-router-dom';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';

import { styled } from '@mui/material/styles';

const StyledItem = styled(Paper)(({theme}) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#FFF',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));

export default function MatchItem({match_id, team_a, team_b, team_a_points, team_b_points}) {
    const navigate = useNavigate();

    return (
        <StyledItem 
            onClick={() => navigate(`/matches/${match_id}`)} 
            className="cursor-item"
        >
            <Card sx={{ minWidth: 275 }}>
                <CardContent>
                    <Typography variant="h7" component="div">
                        <b>{team_a}</b> vs <b>{team_b}</b>
                    </Typography>
                    <Typography variant="body2">
                        <b>{team_a_points}</b>pkt-<b>{team_b_points}</b>pkt
                    </Typography>
                </CardContent>
            </Card>
        </StyledItem>
    );
}
