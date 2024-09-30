// src/pages/BusStops.js
import React, { useState, useEffect } from "react";
import BusStopList from "../components/BusStopList";

function BusStops() {
  const [busStops, setBusStops] = useState([]);
  const [filteredStops, setFilteredStops] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetch("/bus_stops")
      .then((res) => res.json())
      .then((data) => {
        setBusStops(data);
        setFilteredStops(data);
      });
  }, []);

  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    const filtered = busStops.filter(
      (stop) =>
        stop.name.toLowerCase().includes(term) ||
        stop.location.toLowerCase().includes(term)
    );
    setFilteredStops(filtered);
  };

  return (
    <div className="bus-stops">
      <h2>Bus Stops</h2>
      <input
        type="text"
        placeholder="Search bus stops..."
        value={searchTerm}
        onChange={handleSearch}
      />
      <BusStopList busStops={filteredStops} />
    </div>
  );
}

export default BusStops;
