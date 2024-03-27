import { createRoot } from 'react-dom/client';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import CssBaseline from '@mui/material/CssBaseline';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';

import MainPage from './components/MainPage/MainPage';
import MatchDetails from './components/MatchDetails/MatchDetails';
import NavigationBar from './components/NavigationBar';
import MainLobby from './components/MatchLobby/MainLobby';
import LobbySetup from './components/MatchLobby/LobbySetup';
//import SignInPage from './components/Login/SignInPage';
//import SignUpPage from './components/Login/SignUpPage';

import './styles.css';

const theme = createTheme({
    palette: {
        neutral: {
            main: '#64748B',
            contrastText: '#fff',
        },
    }
});

const Copyright = () => {
    return (
        <Typography variant="body2" color="text.secondary" align="center">
            {'Copyright Maciej Kleban, Krzysztof Herbot © '}
            <Link color="inherit" href="https://mui.com/">
                SportsMeter
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    )
}
//<Route path="/login" element={<SignInPage/>}/>
//<Route path="/register" element={<SignUpPage/>}/> add after matchDetails element
//<Route path="/setlobby" element={<LobbySetup/>}/>
const App = () => {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline/>
            <BrowserRouter>
                <NavigationBar/>
                <Routes>
                    <Route exact path="/" element={<MainPage/>}/>
                    <Route path="/matches/:match_id" element={<MatchDetails/>}/>
                    <Route path="/lobby/:match_id" element={<MainLobby/>}/>
                    <Route path="/setlobby" element={<LobbySetup/>}/>
                </Routes>
            </BrowserRouter>
            <Copyright/>
        </ThemeProvider>
    );
}

const root = createRoot(document.getElementById('root'));
root.render(
    <App/>
)
