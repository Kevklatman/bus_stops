import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../contexts/UserContext";

function BusStopList({ busStops, onAddToFavorites }) {
  const { user } = useContext(UserContext);

  if (!Array.isArray(busStops) || busStops.length === 0) {
    return <p>No bus stops available.</p>;
  }

  return (
    <div className="bus-stop-list">
      {busStops.map((stop) => (
        <div key={stop.id} className="bus-stop-card">
          <h3>{stop.name}</h3>
          <p>{stop.location}</p>
          <Link to={`/schedule/${stop.id}`}>View Schedule</Link>
          {user && (
            <button onClick={() => onAddToFavorites(stop.id)}>
              Add to Favorites
            </button>
          )}
        </div>
      ))}
    </div>
  );
}

export default BusStopList;
