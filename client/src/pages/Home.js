import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../contexts/UserContext";

function Home() {
  const [busStops, setBusStops] = useState([]);
  const [filteredBusStops, setFilteredBusStops] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");
  const { user } = useContext(UserContext);

  useEffect(() => {
    fetchBusStops();
  }, []);

  useEffect(() => {
    setFilteredBusStops(
      busStops.filter((stop) =>
        stop.name.toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [search, busStops]);

  const fetchBusStops = async () => {
    try {
      const response = await fetch("/bus_stops");
      if (!response.ok) {
        throw new Error("Failed to fetch bus stops");
      }
      const data = await response.json();
      setBusStops(data);
      setFilteredBusStops(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const addComment = async (stopId, comment) => {
    try {
      const response = await fetch(`/bus_stops/${stopId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ comments: comment }),
      });
      if (!response.ok) {
        throw new Error("Failed to add comment");
      }
      fetchBusStops();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="home">
      <h2>Welcome to NYC Bus Stop</h2>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search bus stops..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      <p>Manage your bus routes and stops efficiently</p>
      <div className="bus-stops-list">
        {filteredBusStops.map((stop) => (
          <div key={stop.id} className="bus-stop-card">
            <h3>{stop.name}</h3>
            <p>{stop.location}</p>
            <Link to={`/schedule/${stop.id}`}>View Schedule</Link>
            <div className="comments-section">
              <h4>Comments:</h4>
              <p>{stop.comments || "No comments yet."}</p>
              {user && (
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    const comment = e.target.comment.value;
                    addComment(stop.id, comment);
                    e.target.comment.value = "";
                  }}
                >
                  <textarea name="comment" required></textarea>
                  <button type="submit">Add Comment</button>
                </form>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Home;
