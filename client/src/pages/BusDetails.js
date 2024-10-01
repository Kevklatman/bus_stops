// src/pages/BusDetails.js
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function BusDetails() {
  const [bus, setBus] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const { busId } = useParams();

  useEffect(() => {
    // Fetch bus details
    fetch(`/buses/${busId}`)
      .then((res) => res.json())
      .then(setBus);

    // Fetch schedules for this bus
    fetch(`/schedules?bus_id=${busId}`)
      .then((res) => res.json())
      .then(setSchedules);
  }, [busId]);

  if (!bus) return <div>Loading...</div>;

  return (
    <div className="bus-details">
      <h2>Bus {bus.number}</h2>
      <p>Capacity: {bus.capacity}</p>
      <h3>Schedules:</h3>
      <ul>
        {schedules.map((schedule) => (
          <li key={schedule.id}>
            Stop {schedule.bus_stop_id}: Arrives at{" "}
            {new Date(schedule.arrival_time).toLocaleTimeString()}, Departs at{" "}
            {new Date(schedule.departure_time).toLocaleTimeString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default BusDetails;
