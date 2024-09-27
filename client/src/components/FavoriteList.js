import React from "react";
import { Link } from "react-router-dom";

function FavoriteList({ favorites }) {
  return (
    <div className="favorite-list">
      {favorites.map((favorite) => (
        <div key={favorite.id} className="favorite-card">
          <h3>{favorite.busStop.name}</h3>
          <p>{favorite.busStop.address}</p>
          <Link to={`/schedule/${favorite.busStop.id}`}>View Schedule</Link>
        </div>
      ))}
    </div>
  );
}

export default FavoriteList;
