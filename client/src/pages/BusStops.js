import React, { useState, useEffect, useContext } from "react";
import { UserContext } from "../contexts/UserContext";
import BusStopList from "../components/BusStopList";

function BusStops() {
  const [busStops, setBusStops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useContext(UserContext);

  useEffect(() => {
    fetchBusStops();
  }, []);

  const fetchBusStops = async () => {
    try {
      const response = await fetch("/bus_stops");
      if (!response.ok) {
        throw new Error("Failed to fetch bus stops");
      }
      const data = await response.json();
      setBusStops(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleAddToFavorites = async (busStopId) => {
    if (!user) return;

    try {
      const response = await fetch("/favorites", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          passenger_id: user.id,
          bus_stop_id: busStopId,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to add to favorites");
      }

      alert("Added to favorites successfully!");
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="bus-stops">
      <h2>Bus Stops</h2>
      <BusStopList
        busStops={busStops}
        onAddToFavorites={handleAddToFavorites}
      />
    </div>
  );
}

export default BusStops;
