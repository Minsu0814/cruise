import "mapbox-gl/dist/mapbox-gl.css";
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

import Splash from "./components/Splash";
import Trip from "./components/Trip";
import "./css/app.css";

// const fetchData = (fileName) => {
//   const baseURL = process.env.NODE_ENV === "production"
//     ? `https://raw.githubusercontent.com/1023sherry/cruise/main/cruise/src/data/`
//     : `${process.env.PUBLIC_URL}/data/`;
  
//   return axios.get(`${baseURL}${fileName}.json`).then((r) => r.data);
// };

const fetchData = (FilE_NAME) => {
  const res = axios.get(
    `https://raw.githubusercontent.com/1023sherry/cruise/main/cruise/src/data/${FilE_NAME}.json`
  );
  const data = res.then((r) => r.data);
  return data;
};

const App = () => {

  const [trip, setTrip] = useState([]);
  const [trip_20, setTrip20] = useState([]);
  const [trip_40, setTrip40] = useState([]);
  const [icon, setIcon] = useState([]);
  const [line, setLine] = useState([]);


  const [isloaded, setIsLoaded] = useState(false);

  const getData = useCallback(async () => {

    const ICON = await fetchData("stop_icon_data");

    const TRIP = await Promise.all([
      fetchData("trip"),
      fetchData("trip2"),
      fetchData("trip3"),
    ]);

    const TRIP_20 = await Promise.all([
      fetchData("trip4_20"),
      fetchData("trip5_20"),
    ]);

    const TRIP_40 = await Promise.all([
      fetchData("trip4_40"),
      fetchData("trip5_40"),
    ]);

    const LINE = await Promise.all([
      fetchData("path_data"),
      fetchData("path_data_y"),
    ]);


    setTrip((prev) => TRIP.flat());
    setTrip20((prev) => TRIP_20.flat());
    setTrip40((prev) => TRIP_40.flat());

    setIcon((prev) => ICON);
    setLine((prev) => LINE.flat());

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
              trip_20={trip_20}
              trip_40={trip_40}

              icon={icon}
              line={line}
              />
      )}
    </div>
  );
};

export default App;
