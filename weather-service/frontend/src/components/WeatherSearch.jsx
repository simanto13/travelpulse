import {useState} from 'react';
import axios from 'axios';
import {TextField,Button,Card,CardContent,Typography,Stack} from '@mui/material';

export default function WeatherSearch(){
 const [city,setCity]=useState('');
 const [weather,setWeather]=useState(null);
 const [loading,setLoading]=useState(false);

 const search=async()=>{
  if(!city) return;
  setLoading(true);
  try{
    const res=await axios.get(`http://localhost:8000/weather/current?city=${encodeURIComponent(city)}`);
    setWeather(res.data);
  }catch(e){alert('Unable to fetch weather');}
  setLoading(false);
 };

 return <>
 <Stack direction="row" spacing={2}>
  <TextField fullWidth label="City" value={city} onChange={e=>setCity(e.target.value)}/>
  <Button variant="contained" onClick={search} disabled={loading}>Search</Button>
 </Stack>
 {weather && <Card sx={{mt:3}}>
   <CardContent>
    <Typography variant="h5">{weather.city}, {weather.country}</Typography>
    <Typography>Temperature: {weather.temperature_c} °C</Typography>
    <Typography>Feels Like: {weather.feels_like_c} °C</Typography>
    <Typography>Humidity: {weather.humidity}%</Typography>
    <Typography>Wind: {weather.wind_kph} km/h</Typography>
    <Typography>Condition: {weather.condition}</Typography>
    <img alt="weather" src={weather.icon?.startsWith('//')?'https:'+weather.icon:weather.icon}/>
   </CardContent>
 </Card>}
 </>;
}