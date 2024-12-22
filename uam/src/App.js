import "mapbox-gl/dist/mapbox-gl.css";
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

import Splash from "./components/Splash";
import Trip from "./components/Trip";
import "./css/app.css";


const fetchData = (fileName) => {
  const baseURL = process.env.NODE_ENV === "production"
    ? `https://raw.githubusercontent.com/1023sherry/UAM_NEW/main/uam/src/data/`
    : `${process.env.PUBLIC_URL}/data/`;
  
  return axios.get(`${baseURL}${fileName}.json`).then((r) => r.data);
};

const App = () => {

  const [trip, setTrip] = useState([]);

  const [isloaded, setIsLoaded] = useState(false);

  const getData = useCallback(async () => {

    const TRIP = await fetchData("trip");

    setTrip((prev) => TRIP);

    setIsLoaded(true);
  }, []);

  useEffect(() => {
    getData();
  }, [getData]);

  return (
    <div className="container">
      {!isloaded && <Splash />}
      {isloaded && (
        <Trip 

              trip={trip}

              />
      )}
    </div>
  );
};

export default App;
