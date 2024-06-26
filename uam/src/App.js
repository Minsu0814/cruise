import "mapbox-gl/dist/mapbox-gl.css";
import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";

import Splash from "./components/Splash";
import Trip from "./components/Trip";
import "./css/app.css";

const fetchData = (FilE_NAME) => {
  const res = axios.get(
    `https://raw.githubusercontent.com/1023sherry/UAM_NEW/main/uam/src/data/${FilE_NAME}.json`
  );
  const data = res.then((r) => r.data);
  return data;
};

const App = () => {
  // const [icon, setIcon] = useState([]);

  const [trip, setTrip] = useState([]);


  const [building, setBuilding] = useState([]);
  const [building_vertiport, setBuildingVertiport] = useState([]);

  const [nodes, setNodes] = useState([]);
  const [links, setLinks] = useState([]);

  const [isloaded, setIsLoaded] = useState(false);

  const getData = useCallback(async () => {
    // const ICON = await fetchData("icon_data");
    const TRIP = await fetchData("trip");
    const BUILDING = await fetchData("buildings");
    const BUILDING_VERTIPORT = await fetchData("building_vertiport");

    const NODES = await Promise.all([
      fetchData("node_ar"),
      fetchData("node_tc"),
      fetchData("node_hg"),
    ]);

    const LINKS = await Promise.all([
      fetchData("link_ar"),
      fetchData("link_tc"),
      fetchData("link_hg"),
    ]);

    // setIcon((prev) => ICON);
    setTrip((prev) => TRIP);

    setBuilding((prev) => BUILDING);
    setBuildingVertiport((prev) => BUILDING_VERTIPORT);

    setNodes((prev) => NODES.flat());
    setLinks((prev) => LINKS.flat());

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
              nodes={nodes}
              links={links} 
              building={building}
              building_vertiport={building_vertiport}

              // icon={icon}

              />
      )}
    </div>
  );
};

export default App;
