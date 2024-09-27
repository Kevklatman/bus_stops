// src/pages/Schedule.js
import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import { UserContext } from "../contexts/UserContext";

function Schedule() {
  const [busStop, setBusStop] = useState(null);
  const [schedule, setSchedule] = useState([]);
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);
  const { stopId } = useParams();
  const { user } = useContext(UserContext);

  useEffect(() => {
    // Fetch bus stop details
    fetch(`/api/bus-stops/${stopId}`)
      .then((res) => res.json())
      .then(setBusStop);

    // Fetch schedule for this stop
    fetch(`/api/bus-stops/${stopId}/schedule`)
      .then((res) => res.json())
      .then(setSchedule);

    // Fetch comments for this stop
    fetch(`/api/bus-stops/${stopId}/comments`)
      .then((res) => res.json())
      .then(setComments);
  }, [stopId]);

  const handleAddComment = (e) => {
    e.preventDefault();
    fetch(`/api/bus-stops/${stopId}/comments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ userId: user.id, content: comment }),
    })
      .then((res) => res.json())
      .then((newComment) => {
        setComments([...comments, newComment]);
        setComment("");
      });
  };

  if (!busStop) return <div>Loading...</div>;

  return (
    <div className="schedule">
      <h2>{busStop.name} Schedule</h2>
      <p>{busStop.address}</p>
      <ul>
        {schedule.map((entry) => (
          <li key={entry.id}>
            Bus {entry.busNumber}: {entry.arrivalTime}
          </li>
        ))}
      </ul>
      <h3>Comments</h3>
      <ul>
        {comments.map((c) => (
          <li key={c.id}>{c.content}</li>
        ))}
      </ul>
      {user && (
        <form onSubmit={handleAddComment}>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Add a comment..."
          />
          <button type="submit">Post Comment</button>
        </form>
      )}
    </div>
  );
}

export default Schedule;
