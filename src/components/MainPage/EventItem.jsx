import React from 'react';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';

import { styled } from '@mui/material/styles';

const StyledItem = styled(Card)(({theme}) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#FFF',
    ...theme.typography.body2,
    margin: theme.spacing(1),
    width: '100%',
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));

export default function EventItem({event_title, event_description}) {

    return (
        <StyledItem sx={{ minWidth: 275 }}>
            <CardContent>
                <Typography sx={{ fontSize: 12}} color="text.secondary" gutterBottom>
                    {event_title}
                </Typography>
                <Divider/>
                <Typography sx={{ fontSize: 10}} color="text.secondary" gutterBottom>
                    {event_description}
                </Typography>
            </CardContent>
        </StyledItem>
    );
}
