// src/components/BusStopList.js
import React from "react";
import { Link } from "react-router-dom";

function BusStopList({ busStops }) {
  return (
    <div className="bus-stop-list">
      {busStops.map((stop) => (
        <div key={stop.id} className="bus-stop-card">
          <h3>{stop.name}</h3>
          <p>{stop.location}</p>
          <Link to={`/schedule/${stop.id}`}>View Schedule</Link>
        </div>
      ))}
    </div>
  );   
}

export default BusStopList;
