import React, { useState, useEffect } from "react";
import BusStopList from "../components/BusStopList";

function BusStops() {
  const [busStops, setBusStops] = useState([]);
  const [filteredStops, setFilteredStops] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5555";

  useEffect(() => {
    setIsLoading(true);
    fetch(`${API_URL}/bus_stops`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch bus stops");
        }
        return res.json();
      })
      .then((data) => {
        setBusStops(data);
        setFilteredStops(data);
        setIsLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setIsLoading(false);
      });
  }, [API_URL]);

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

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="bus-stops">
      <h2>Bus Stops</h2>
      <input
        type="text"
        placeholder="Search bus stops..."
        value={searchTerm}
        onChange={handleSearch}
      />
      {filteredStops.length > 0 ? (
        <BusStopList busStops={filteredStops} />
      ) : (
        <p>No bus stops found.</p>
      )}
    </div>
  );
}

export default BusStops;
