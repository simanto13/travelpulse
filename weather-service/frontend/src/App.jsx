import {Container,Typography} from '@mui/material';
import WeatherSearch from './components/WeatherSearch';
export default function App(){
 return <Container maxWidth="sm">
 <Typography variant="h4" sx={{my:3}}>TravelPulse Weather</Typography>
 <WeatherSearch/>
 </Container>;
}