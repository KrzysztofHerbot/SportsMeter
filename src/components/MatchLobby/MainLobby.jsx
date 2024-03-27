import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, useParams } from 'react-router-dom';

import AddIcon from '@mui/icons-material/Add';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Divider from '@mui/material/Divider';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import ButtonIcons, { FunctionsOutlined } from '@mui/icons-material'
import DeleteIcon from '@mui/icons-material/Delete';
import SportsGolf from '@mui/icons-material/SportsGolf';
import AddCircle from '@mui/icons-material/AddCircle';
import RemoveCircle from '@mui/icons-material/RemoveCircle';
import InsertDriveFile from '@mui/icons-material/InsertDriveFile';
import CheckCircle from '@mui/icons-material/CheckCircle';
import Cancel from '@mui/icons-material/Cancel';

import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';

import Popper from '@mui/material/Popper';
import Fade from '@mui/material/Fade';

import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

import Stopwatch from './Stopwatch';

/*import MatchForm from './MatchForm';*/

import parseDate from '../../utils/parseDate';
import parseTime from '../../utils/parseTime';
import MatchDetails from '../MatchDetails/MatchDetails';

export default function MainLobby() {
    const { match_id } = useParams();
    const [isEditing, setIsEditing] = useState(false);
    const [matchDetails, setMatchDetails] = useState(
        {
            "match_id": 0, "team_a_name": "", "team_a_points": 0,
            "team_b_name": "", "team_b_points": 0, "match_date": "",
            "match_start_time": "", "match_end_time": ""
        }
    );
    const [MatchPlayers, setMatchPlayers] = useState([]);

    const [MatchPlayersStats, setMatchPlayersStats] = useState([])
    const [team_a_score, setTeam_a_score] = useState(0);
    const [team_b_score, setTeam_b_score] = useState(0);

    // List to select players
    const [sub, setSub] = React.useState('');
    const [subFor, setSubFor] = React.useState('');
    //substitutions
    const [Substitutions, setSubstitutions] = useState([]);

    const handleSub = (event) => {
        setSub(event.target.value);
    };
    const handleSubFor = (event) => {
        setSubFor(event.target.value);
    };

    const fetchMatchDetails = async () => {
        try {
            const result = await axios(`/api/matches/${match_id}`);
            setMatchDetails(result?.data);
        }
        catch (error) {
            console.log(error);
            navigate("/");
        }
    }


    const initMatchDetails = () => {
        setTeam_a_score(matchDetails.team_a_points);
        setTeam_b_score(matchDetails.team_b_points);
    }


    const UpdateBackendPoints = () => {
        /* update matchDetails*/
        matchDetails.team_a_points = team_a_score;
        matchDetails.team_a_points = team_a_score;


        /* Put data on backend*/
        try {
            const res = axios.put(`/api/matches/${match_id}`, { "match_id": matchDetails.id, "team_a_points": matchDetails.team_a_points, "team_b_points": matchDetails.team_b_points });
        }
        catch (error) {
            console.log(error);
            navigate("/");
        }


    }

    const fetchMatchPlayers = async () => {
        try {
            const result = await axios.get(`/api/matches/${match_id}/players`);
            setMatchPlayers(result?.data);
            console.log(result?.data)
        }
        catch (error) {
            console.log(error);
        }
    }

    /*function postMatchPlayers(dataPUT){
        try {
            const putData = axios.post(`/api/matches/${match_id}/players`, dataPUT);
        }
        catch (error) {
            console.log(error);
        }
    }*/

    const fetchPlayer = async (player_id) => {
        try {
            const result = await axios.get(`/api/players/${player_id}`);
            return (result?.data);
        }
        catch (error) {
            console.log(error);
        }

    }

    /*const fetchTeams =  async () => {
        try {
            const result = await axios('/api/teams');
            setSeasons(result?.data);
        } catch (error) {
            console.log(error);
        }
    }
    */

    /* DATA FOR STATISTICS: */
    function createData(active, number, name, gender, shotsSuc, shots, passesSuc, passes, tacklesSuc, tackles, defensesSuc, defenses, turnoversSuc, turnovers, beatsSuc, beats, catchesSuc, catches) {
        return { active, number, name, gender, shotsSuc, shots, passesSuc, passes, tacklesSuc, tackles, defensesSuc, defenses, turnoversSuc, turnovers, beatsSuc, beats, catchesSuc, catches };
    }

    async function createTeam(teamArray) {
        teamOutput = [];
        for (let i = 0; i < teamArray.length; i++) {
            await fetchPlayer(teamArray[i].match_player).then((player) => {
                if (player) {
                    teamOutput[i] = createData(teamArray[i].player_active, player.player_id, player.player_name, player.player_gender, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
                    console.log(teamOutput[i]);
                }
            })
        }
        return teamOutput;
    }
    const getTeams = async () => {
        setMatchPlayersStats(await createTeam(MatchPlayers));
    }

    function SnitchCatch(team_snitch) {
        if (team_snitch == "a") {
            setTeam_a_score((prevTeam_a_score) => prevTeam_a_score + 30);
        }
        else if (team_snitch == "b") {
            setTeam_b_score((prevTeam_b_score) => prevTeam_b_score + 30);
        }
        return false;
    }

    function GetPlayer(number) {
        const statIndex = MatchPlayersStats.findIndex(stat => stat.number === number)
        return MatchPlayersStats[statIndex].name;
    }

    const BorderBox = ({ children }) => {
        return (
            <Box
                sx={{
                    border: '1px solid',
                    borderRadius: '4px',
                    borderColor: 'lightgrey',
                    padding: '4px',
                    m: 2,
                }}
            >
                {children}
            </Box>
        );
    }

    const ButtonAction = ({ children, row, type }) => {
        //Popper for statistics
        const [anchorEl, setAnchorEl] = useState();
        const [open, setOpen] = useState(false);
        const [placement, setPlacement] = useState();

        const handlePopperClick = (newPlacement) => (event) => {
            console.log("handlePopperClick ");
            setAnchorEl(event.currentTarget);
            setOpen((prev) => placement !== newPlacement || !prev);
            setPlacement(newPlacement);
        }

        const handlePopperClose = (event) => {
            setAnchorEl(null);
        }

        const HandleClickGood = () => {
            setMatchPlayersStats(prevStats => {
                const updatedStats = [...prevStats];
                const statIndex = updatedStats.findIndex(stat => stat.name === row.name);
                console.log(row);
                console.log(row.name);
                console.log(statIndex);
                console.log(updatedStats[statIndex].shots);
                if (type == "shots") {
                    updatedStats[statIndex].shots += 1;
                    updatedStats[statIndex].shotsSuc += 1;
                }
                else if (type == "passes") {
                    updatedStats[statIndex].passes += 1;
                    updatedStats[statIndex].passesSuc += 1;
                }
                else if (type == "tackles") {
                    updatedStats[statIndex].tackles += 1;
                    updatedStats[statIndex].tacklesSuc += 1;
                }
                else if (type == "defenses") {
                    updatedStats[statIndex].defenses += 1;
                    updatedStats[statIndex].defensesSuc += 1;
                }
                else if (type == "turnovers") {
                    updatedStats[statIndex].turnovers += 1;
                    updatedStats[statIndex].turnoversSuc += 1;
                }
                else if (type == "beats") {
                    updatedStats[statIndex].beats += 1;
                    updatedStats[statIndex].beatsSuc += 1;
                }
                else if (type == "catches") {
                    updatedStats[statIndex].catches += 1;
                    updatedStats[statIndex].catchesSuc += 1;
                }
                return updatedStats;
            });
        };

        const HandleClickBad = () => {
            setMatchPlayersStats(prevStats => {
                const updatedStats = [...prevStats];
                const statIndex = updatedStats.findIndex(stat => stat.name === row.name);
                if (type == "shots") {
                    updatedStats[statIndex].shots += 1;
                }
                else if (type == "passes") {
                    updatedStats[statIndex].passes += 1;
                }
                else if (type == "tackles") {
                    updatedStats[statIndex].tackles += 1;
                }
                else if (type == "defenses") {
                    updatedStats[statIndex].defenses += 1;
                }
                else if (type == "turnovers") {
                    updatedStats[statIndex].turnovers += 1;
                }
                else if (type == "beats") {
                    updatedStats[statIndex].beats += 1;
                }
                else if (type == "catches") {
                    updatedStats[statIndex].catches += 1;
                }

                return updatedStats;
            });
        };

        return (
            <>

                <Popper
                    open={open}
                    anchorEl={anchorEl}
                    placement={placement}
                    modifiers={[
                        {
                            name: 'offset',
                            options: {
                                offset: [0, 8], // Adjust the offset values if needed
                            },
                        },
                    ]}
                    transition
                    onClose={handlePopperClose}
                >
                    <Paper>
                        <IconButton
                            aria-label="fail" sx={{ backgroundColor: 'red', m: 2, '&:hover': { backgroundColor: 'darkRed', }, }}
                            onClick={HandleClickBad}>
                            <Cancel />
                        </IconButton>
                        <IconButton
                            aria-label="success" sx={{ backgroundColor: 'green', m: 2, '&:hover': { backgroundColor: 'darkGreen', }, }}
                            onClick={HandleClickGood}>
                            <CheckCircle />
                        </IconButton>
                    </Paper>
                </Popper>
                <Button onClick={handlePopperClick('top')} variant="outlined">
                    {children}
                </Button>

            </>
        );
    }

    const ExecuteSubstitutions = () => {
        /* update matchPlayers*/
        console.log("hi");
        setMatchPlayersStats((prevMatchPlayersStats) => {
            const updatedMatchPlayerStats = [...prevMatchPlayersStats];
            console.log(updatedMatchPlayerStats);
            for (let index = 0; index < Substitutions.length; index++) {
                const substitution = Substitutions[index];

                const playerIndex = updatedMatchPlayerStats.findIndex(playerIndex => playerIndex.number === substitution.numberPlayer);
                const subIndex = updatedMatchPlayerStats.findIndex(subIndex => subIndex.number === substitution.numberSub);
                

                console.log(playerIndex,substitution.numberPlayer);
                console.log(subIndex,substitution.numberSub);
                updatedMatchPlayerStats[playerIndex].active = !updatedMatchPlayerStats[playerIndex].active;
                updatedMatchPlayerStats[subIndex].active = !updatedMatchPlayerStats[subIndex].active;
                
                console.log(updatedMatchPlayerStats);
            }
            return updatedMatchPlayerStats;
        });


        setSubstitutions((prevSubs) => {
            const updatedSubs = [...prevSubs];
        
            for (let index = updatedSubs.length - 1; index >= 0; index--) {
              updatedSubs.splice(index, 1);
            }
        
            return updatedSubs;
          });
        /* Put data on backend - No put call for matchplayers on the backend*/

    }

    const RemoveFromSubstitutions = (Player) => {
        setSubstitutions(prevSubs => {
            const updatedSubs = [...prevSubs];
            const subIndex = updatedSubs.findIndex(sub => sub.namePlayer === Player);
            updatedSubs.splice(subIndex, 1);
            return updatedSubs;
        })
    }

    const SubstitutionElement = ({ SubPlayer, Player }) => {
        return (
            <Grid container spacing={4} sx={{ paddingLeft: "16px" }}>
                <Grid item xs={3} sx={{ display: 'flex', alignItems: 'center' }}>
                    {console.log("is it me you're looking for?")}
                    {console.log(SubPlayer)}
                    <Typography>
                        {SubPlayer}
                    </Typography>

                </Grid>
                <Grid item xs={3} sx={{ display: 'flex', alignItems: 'center' }}>
                    -
                </Grid>
                <Grid item xs={3} sx={{ display: 'flex', alignItems: 'center' }}>
                    <Typography>
                        {Player}
                    </Typography>
                </Grid>
                <Grid item xs={3}>
                    <Button sx={{ color: 'blue', fontSize: 10 }}
                        onClick={() => RemoveFromSubstitutions(Player)}>
                        cancel substitution
                    </Button>
                </Grid>
            </Grid>
        )
    }

    const navigate = useNavigate();

    useEffect(() => {
        SnitchCatch();
        fetchMatchDetails();
        fetchMatchPlayers();
        initMatchDetails();
        getTeams();
    }, []);

    return (
        <>
            {/************************************************ Users in the lobby *****************************************************************************/}
            <BorderBox>
                <List>
                    <ListItem>
                        <Grid container spacing={2}>
                            <Grid item xs={11}>
                                <Typography sx={{ textAlign: 'left', m: 0, fontSize: 18 }}>
                                    Users in the Lobby:
                                </Typography>
                            </Grid>
                            <Grid item xs={1} sx={{ display: 'flex', justifyContent: 'right' }}>
                                <Button
                                    variant="contained"
                                    color="neutral"
                                    onClick={() => navigate("/")}
                                >
                                    Exit
                                </Button>
                            </Grid>
                        </Grid>
                    </ListItem>
                    <Divider />
                    {/*************  Users: ***************/}
                    <Grid>
                        <ListItem>
                            <Grid container spacing={2} sx={{ display: 'flex', alignItems: 'center' }}>
                                <Grid item xs={3}>
                                    <Typography sx={{ textAlign: 'left', m: 0, fontSize: 12 }}>
                                        Admin1
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>
                                    <SportsGolf />
                                </Grid>
                            </Grid>
                        </ListItem>
                        <ListItem>
                            <Grid container spacing={2} sx={{ display: 'flex', alignItems: 'center' }}>
                                <Grid item xs={3}>
                                    <Typography sx={{ textAlign: 'left', m: 0, fontSize: 12 }}>
                                        User1
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>

                                </Grid>
                            </Grid>
                        </ListItem>
                        <ListItem>
                            <Grid container spacing={2} sx={{ display: 'flex', alignItems: 'center' }}>
                                <Grid item xs={3}>
                                    <Typography sx={{ textAlign: 'left', m: 0, fontSize: 12 }}>
                                        User2
                                    </Typography>
                                </Grid>
                                <Grid item xs={2}>

                                </Grid>
                            </Grid>
                        </ListItem>
                    </Grid>
                </List>
            </BorderBox>

            {/******************************************************************** Score ***************************************************************/}
            <BorderBox>
                <Grid container spacing={3}>
                    {/* Team A name, logo and color */}
                    <Grid item xs={3}>
                        <Typography sx={{ textAlign: 'left', m: 2 }}>
                            {matchDetails.team_a_name}
                        </Typography>
                    </Grid>
                    {/* Score in the middle */}
                    <Grid item xs={6}>
                        <Grid container spacing={5}>
                            {/* Team A snitch catch */}
                            <Grid item xs={2} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <IconButton onClick={() => SnitchCatch("a")}
                                    aria-label="snitch_catch_A" sx={{ backgroundColor: 'gold', m: 2, '&:hover': { backgroundColor: 'yellow', }, }}>
                                    <SportsGolf />
                                </IconButton>
                            </Grid>
                            {/* Team A score buttons */}
                            <Grid item xs={2}>
                                <List spacing={0}>
                                    <ListItem>
                                        <IconButton onClick={() => setTeam_a_score((prevTeam_a_score) => prevTeam_a_score + 10)}
                                            aria-label="add_points_A"
                                            sx={{ backgroundColor: 'green', m: 1, '&:hover': { backgroundColor: 'darkGreen', }, }}>
                                            <AddCircle />
                                        </IconButton>
                                    </ListItem>
                                    <ListItem>
                                        <IconButton onClick={() => {
                                            if (team_a_score != 0) { setTeam_a_score((prevTeam_a_score) => prevTeam_a_score - 10) }
                                        }}
                                            aria-label="remove_points_A"
                                            sx={{ backgroundColor: 'red', m: 1, '&:hover': { backgroundColor: 'darkRed', }, }}>
                                            <RemoveCircle />
                                        </IconButton>
                                    </ListItem>
                                </List>
                            </Grid>
                            {/* SCORE (maybe change to MatchDetails.team_a_points) TODO*/}
                            <Grid item xs={4} sx={{ fontSize: 72 }} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                {team_a_score}:{team_b_score}
                            </Grid>
                            {/* Team B score buttons */}
                            <Grid item xs={2}>
                                <List spacing={0}>
                                    <ListItem>
                                        <IconButton onClick={() => setTeam_b_score((prevTeam_b_score) => prevTeam_b_score + 10)}
                                            aria-label="add_points_A"
                                            sx={{ backgroundColor: 'green', m: 1, '&:hover': { backgroundColor: 'darkGreen', }, }}>
                                            <AddCircle />
                                        </IconButton>
                                    </ListItem>
                                    <ListItem>
                                        <IconButton onClick={() => {
                                            if (team_b_score != 0) { setTeam_b_score((prevTeam_b_score) => prevTeam_b_score - 10) }
                                        }}
                                            aria-label="remove_points_A"
                                            sx={{ backgroundColor: 'red', m: 1, '&:hover': { backgroundColor: 'darkRed', }, }}>
                                            <RemoveCircle />
                                        </IconButton>
                                    </ListItem>
                                </List>
                            </Grid>
                            {/* Team B snitch catch */}
                            <Grid item xs={2} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                                <IconButton onClick={() => SnitchCatch("b")}
                                    aria-label="snitch_catch_B" sx={{ backgroundColor: 'gold', m: 2, '&:hover': { backgroundColor: 'yellow', }, }}>
                                    <SportsGolf />
                                </IconButton>
                            </Grid>
                        </Grid>
                    </Grid>
                    <Grid item xs={3}>
                        {/* Team B name, logo and color */}
                        <Typography sx={{ textAlign: 'right', m: 2 }}>
                            {matchDetails.team_b_name}
                        </Typography>
                    </Grid>
                </Grid>
                <Button
                    onClick={initMatchDetails}>
                    Refresh
                </Button>
                <Button
                    onClick={UpdateBackendPoints}>
                    Update
                </Button>
            </BorderBox>

            {/************************************************** Timer ***************************************************************/}
            <BorderBox justifyContent="center" alignItems="center">
                <Grid container spacing={3}>
                    <Grid item xs={4}>

                    </Grid>
                    <Grid item xs={6} justifyContent="center" alignItems="center">
                    <Stopwatch />
                    </Grid>
                    <Grid item xs={3}>

                    </Grid>
                </Grid>
                
            </BorderBox>

            {/*********************************************** Statistics ***********************************************************************/}
            <BorderBox>
                <BorderBox>
                    <Button
                        onClick={getTeams}>
                        Reset Squad
                    </Button>
                </BorderBox>
                <TableContainer component={Paper}>
                    <Table sx={{ minWidth: 650 }} aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell>Name</TableCell>
                                <TableCell align="center">Shots</TableCell>
                                <TableCell align="center">Passes</TableCell>
                                <TableCell align="center">Tackles</TableCell>
                                <TableCell align="center">Defenses</TableCell>
                                <TableCell align="center">Turnovers</TableCell>
                                <TableCell align="center">Beats</TableCell>
                                <TableCell align="center">Catches</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {MatchPlayersStats.map((row) => (
                                row.active !== false &&
                                <TableRow
                                    key={row.name}
                                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                                >
                                    <TableCell component="th" scope="row">
                                        {row.number}
                                        {" | "}
                                        {row.name}
                                        {" | "}
                                        {row.gender}
                                    </TableCell>
                                    <TableCell align="center">
                                        <ButtonAction
                                            row={row}
                                            type="shots">
                                            {row.shotsSuc}
                                            {" / "}
                                            {row.shots}
                                        </ButtonAction>
                                    </TableCell>
                                    <TableCell align="center">
                                        <ButtonAction
                                            row={row}
                                            type="passes">
                                            {row.passesSuc}
                                            {" / "}
                                            {row.passes}
                                        </ButtonAction>
                                    </TableCell>
                                    <TableCell align="center">
                                        <ButtonAction
                                            row={row}
                                            type="tackles">
                                            {row.tacklesSuc}
                                            {" / "}
                                            {row.tackles}
                                        </ButtonAction>
                                    </TableCell>
                                    <TableCell align="center">
                                        <ButtonAction
                                            row={row}
                                            type="defenses">
                                            {row.defensesSuc}
                                            {" / "}
                                            {row.defenses}
                                        </ButtonAction>
                                    </TableCell>
                                    <TableCell align="center">
                                        <ButtonAction
                                            row={row}
                                            type="turnovers">
                                            {row.turnoversSuc}
                                            {" / "}
                                            {row.turnovers}
                                        </ButtonAction>
                                    </TableCell>
                                    <TableCell align="center">
                                        <ButtonAction
                                            row={row}
                                            type="beats">
                                            {row.beatsSuc}
                                            {" / "}
                                            {row.beats}
                                        </ButtonAction>
                                    </TableCell>
                                    <TableCell align="center">
                                        <ButtonAction
                                            row={row}
                                            type="catches">
                                            {row.catchesSuc}
                                            {" / "}
                                            {row.catches}
                                        </ButtonAction>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </BorderBox>

            <Grid container spacing={3}>
                {/********************************************* Plan substitutions ************************************************************/}
                <Grid item xs={6}>
                    <BorderBox>
                        <Grid container spacing={2} m={0} sx={{ display: 'flex', alignItems: 'center' }}>
                            <Grid item xs={3}>
                                Plan Substitutions:
                            </Grid>
                            <Grid item xs={4} sx={{ padding: '10px' }}>
                                <Button
                                    variant="contained"
                                    color="success"
                                    onClick={() => ExecuteSubstitutions()}>
                                    Execute
                                </Button>
                            </Grid>
                            <Grid item xs={4} sx={{ textAlign: 'right', fontSize: 12, color: 'red' }}>
                                Warning
                            </Grid>
                        </Grid>
                        <Divider />
                        {
                            Substitutions.map((Substitutions, index) => (
                                <SubstitutionElement
                                    SubPlayer={Substitutions?.nameSub}
                                    Player={Substitutions?.namePlayer}>
                                </SubstitutionElement>
                            ))
                        }
                        <Divider />
                        <Grid container spacing={2} m={0}>
                            <Grid item xs={4}>
                                <Box sx={{ minWidth: 80 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="demo-simple-select-label">Substitution</InputLabel>
                                        <Select
                                            labelId="demo-simple-select-label"
                                            id="demo-simple-select"
                                            value={sub}
                                            label="Substitution"
                                            onChange={handleSub}
                                        >
                                            {
                                                MatchPlayersStats.map((MatchPlayersStats, index) => (
                                                    MatchPlayersStats?.active == false &&
                                                    <MenuItem value={MatchPlayersStats?.number}>{MatchPlayersStats?.name}</MenuItem>
                                                ))
                                            }
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                            <Grid item xs={4}>
                                <Box sx={{ minWidth: 80 }}>
                                    <FormControl fullWidth>
                                        <InputLabel id="demo-simple-select-label2">Player</InputLabel>
                                        <Select
                                            labelId="demo-simple-select-label2"
                                            id="demo-simple-select2"
                                            value={subFor}
                                            label="Player"
                                            onChange={handleSubFor}
                                        >
                                            {
                                                MatchPlayersStats.map((MatchPlayersStats, index) => (
                                                    MatchPlayersStats?.active == true &&
                                                    <MenuItem value={MatchPlayersStats?.number}>{MatchPlayersStats?.name}</MenuItem>
                                                ))
                                            }
                                        </Select>
                                    </FormControl>
                                </Box>
                            </Grid>
                            <Grid item xs={4} sx={{ display: 'flex', justifyContent: 'right', paddingRight: '76px' }}>
                                <Button
                                    variant="contained"
                                    color="success"
                                    onClick={() => {
                                        if (sub !== '' && subFor !== '') {
                                            console.log("hello");
                                            setSubstitutions([...Substitutions, {
                                                nameSub: GetPlayer(sub),
                                                numberSub: sub,
                                                namePlayer: GetPlayer(subFor),
                                                numberPlayer: subFor,
                                                //active:sub.active,
                                            },])
                                            setSub('');
                                            setSubFor('');
                                            console.log(Substitutions)
                                        }

                                    }}>
                                    New Substitution
                                </Button>
                            </Grid>
                        </Grid>
                    </BorderBox>
                </Grid>
                {/********************************************* Add cards ************************************************************/}
                <Grid item xs={6}>
                    <BorderBox>
                        <Grid container spacing={2} m={0} sx={{ display: 'flex', alignItems: 'center' }}>
                            <Grid item xs={3}>
                                Add cards:
                            </Grid>
                            <Grid item xs={3}>
                                <IconButton
                                    aria-label="blue_card"
                                    sx={{ backgroundColor: 'lightBlue', m: 1, '&:hover': { backgroundColor: 'Blue', }, }}>
                                    <InsertDriveFile />
                                </IconButton>
                                <IconButton
                                    aria-label="yellow_card"
                                    sx={{ backgroundColor: 'yellow', m: 1, '&:hover': { backgroundColor: 'gold', }, }}>
                                    <InsertDriveFile />
                                </IconButton>
                                <IconButton
                                    aria-label="red_card"
                                    sx={{ backgroundColor: 'red', m: 1, '&:hover': { backgroundColor: 'darkRed', }, }}>
                                    <InsertDriveFile />
                                </IconButton>
                            </Grid>
                        </Grid>
                        <Divider />
                        <Grid container spacing={3} sx={{ display: 'flex', alignItems: 'center' }}>
                            <Grid item xs={6} sx={{ marginLeft: "16px" }}>
                                Player 3
                            </Grid>
                            <Grid item xs={2}>
                                00:23
                            </Grid>
                            <Grid item xs={2} sx={{ padding: "6px" }}>
                                <Button sx={{ marginTop: "6px" }}
                                    variant="contained"
                                    color="success">
                                    Release
                                </Button>
                            </Grid>
                        </Grid>
                    </BorderBox>
                </Grid>
            </Grid>
            {/***************************************************** Add players box ************************************************************/}
            <BorderBox>

            </BorderBox>

        </>
    )
}