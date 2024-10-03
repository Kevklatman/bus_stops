import React, { useState, useEffect, useContext } from "react";
import { UserContext } from "../contexts/UserContext";
import FavoriteList from "../components/FavoriteList";

function Favorites() {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user } = useContext(UserContext);

  useEffect(() => {
    const fetchFavorites = async () => {
      if (!user) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await fetch(`passenger_favorites/${user.id}`);
        if (!response.ok) {
          throw new Error("Failed to fetch favorites");
        }
        const data = await response.json();
        setFavorites(data.passenger_favorites);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, [user]);

  if (loading) return <div>Loading favorites...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return <div>Please log in to view your favorites.</div>;

  return (
    <div className="favorites">
      <h2>Your Favorite Bus Stops</h2>
      <FavoriteList favorites={favorites} />
    </div>
  );
}

export default Favorites;