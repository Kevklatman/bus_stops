// src/pages/AdminDashboard.js
import React, { useState, useEffect, useContext } from "react";
import { UserContext } from "../contexts/UserContext";

function AdminDashboard() {
  const [buses, setBuses] = useState([]);
  const [busStops, setBusStops] = useState([]);
  const { user } = useContext(UserContext);

  useEffect(() => {
    if (user && user.isAdmin) {
      // Fetch buses
      fetch("/buses")
        .then((res) => res.json())
        .then(setBuses);

      // Fetch bus stops
      fetch("/bus_stops")
        .then((res) => res.json())
        .then(setBusStops);
    }
  }, [user]);

  const handleUpdateBus = (busId, updates) => {
    fetch(`/buses/${busId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updates),
    })
      .then((res) => res.json())
      .then((updatedBus) => {
        setBuses(buses.map((bus) => (bus.id === busId ? updatedBus : bus)));
      });
  };

  const handleUpdateBusStop = (stopId, updates) => {
    fetch(`/bus_stops/${stopId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updates),
    })
      .then((res) => res.json())
      .then((updatedStop) => {
        setBusStops(
          busStops.map((stop) => (stop.id === stopId ? updatedStop : stop))
        );
      });
  };

  if (!user || !user.isAdmin) return <div>Access denied.</div>;

  return (
    <div className="admin-dashboard">
      <h2>Admin Dashboard</h2>
      <h3>Buses</h3>
      <ul>
        {buses.map((bus) => (
          <li key={bus.id}>
            Bus {bus.number}
            <button
              onClick={() =>
                handleUpdateBus(bus.id, {
                  /* updates */
                })
              }
            >
              Edit
            </button>
          </li>
        ))}
      </ul>
      <h3>Bus Stops</h3>
      <ul>
        {busStops.map((stop) => (
          <li key={stop.id}>
            {stop.name}
            <button
              onClick={() =>
                handleUpdateBusStop(stop.id, {
                  /* updates */
                })
              }
            >
              Edit
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AdminDashboard;
