import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Schedule() {
  const [schedules, setSchedules] = useState([]);
  const [busStop, setBusStop] = useState(null);
  const { stopId } = useParams();

  useEffect(() => {
    // Fetch bus stop details
    fetch(`/bus_stops/${stopId}`)
      .then((res) => res.json())
      .then(setBusStop);

    // Fetch schedules for this stop
    fetch(`/schedules?bus_stop_id=${stopId}`)
      .then((res) => res.json())
      .then(setSchedules);
  }, [stopId]);

  if (!busStop) return <div>Loading...</div>;

  return (
    <div className="schedule">
      <h2>{busStop.name} Schedule</h2>
      <p>{busStop.location}</p>
      <ul>
        {schedules.map((entry) => (
          <li key={entry.id}>
            Bus {entry.bus_id}: Arrives at{" "}
            {new Date(entry.arrival_time).toLocaleTimeString()}, Departs at{" "}
            {new Date(entry.departure_time).toLocaleTimeString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Schedule;
