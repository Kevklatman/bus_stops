// src/pages/Favorites.js
import React, { useState, useEffect, useContext } from "react";
import { UserContext } from "../contexts/UserContext";
import FavoriteList from "../components/FavoriteList";

function Favorites() {
  const [favorites, setFavorites] = useState([]);
  const { user } = useContext(UserContext);

  useEffect(() => {
    if (user) {
      // Fetch user's favorites from API
      fetch(`/api/users/${user.id}/favorites`)
        .then((res) => res.json())
        .then(setFavorites);
    }
  }, [user]);

  return (
    <div className="favorites">
      <h2>Your Favorite Bus Stops</h2>
      <FavoriteList favorites={favorites} />
    </div>
  );
}

export default Favorites;
