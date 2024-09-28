import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";

function BusStopList({ busStops, isLoading }) {
  if (isLoading) {
    return <p>Loading bus stops...</p>;
  }

  if (!Array.isArray(busStops) || busStops.length === 0) {
    return <p>No bus stops available.</p>;
  }

  return (
    <div className="bus-stop-list">
      {busStops.map((stop) => (
        <div key={stop.id} className="bus-stop-card">
          <h3>{stop.name}</h3>
          <p>{stop.location}</p>
          {stop.nextBus && <p>Next bus: {stop.nextBus}</p>}
          <Link to={`/schedule/${stop.id}`}>View Schedule</Link>
        </div>
      ))}
    </div>
  );
}

BusStopList.propTypes = {
  busStops: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      name: PropTypes.string.isRequired,
      location: PropTypes.string.isRequired,
      nextBus: PropTypes.string,
    })
  ),
  isLoading: PropTypes.bool,
};

export default BusStopList;
