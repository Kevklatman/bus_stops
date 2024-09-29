// src/components/FavoriteList.js
import React, { useState } from "react";
import { Link } from "react-router-dom";

function FavoriteList({ favorites }) {
  return (
    <div className="favorite-list">
      {favorites.map((favorite) => (
        <div key={favorite.id} className="favorite-card">
          <h3>{favorite.bus_stop_name}</h3>
          <p>{favorite.bus_stop_location}</p>
          <Link to={`/schedule/${favorite.bus_stop_id}`}>View Schedule</Link>
        </div>
      ))}
    </div>
  );
}


export default FavoriteList;
