// src/components/FavoriteList.js
import React, { useState } from "react";
import { Link } from "react-router-dom";

function FavoriteList({ favorites }) {
  
  const [search, setSearch] = useState("");
 
  const updateSearch = (newSearch) => setSearch(newSearch);


  
  return (
    <div className="favorite-list">
      {favorites.map((favorite) => (
        <div key={favorite.id} className="favorite-card">
          <h3>{favorite.bus_stop_name}</h3>
          <p>{favorite.bus_stop_location}</p>
          <Link to={`/schedule/${favorite.bus_stop_id}`}>View Schedule</Link>

        <label htmlFor="search">Favrotie Bus Stops</label>
        <input
        value={search}
        type="text"
        id="search"
        placeholder="Search bus stops..."
        onChange={(e) => updateSearch(e.target.value)}
      />
        </div>
      ))}
    </div>
  );
}

export default FavoriteList;
