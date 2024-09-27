// src/pages/Profile.js
import React, { useContext, useState } from "react";
import { UserContext } from "../contexts/UserContext";

function Profile() {
  const { user, setUser } = useContext(UserContext);
  const [name, setName] = useState(user ? user.name : "");
  const [email, setEmail] = useState(user ? user.email : "");

  const handleUpdateProfile = (e) => {
    e.preventDefault();
    fetch(`/api/users/${user.id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email }),
    })
      .then((res) => res.json())
      .then((updatedUser) => setUser(updatedUser));
  };

  const handleDeleteAccount = () => {
    if (window.confirm("Are you sure you want to delete your account?")) {
      fetch(`/api/users/${user.id}`, {
        method: "DELETE",
      }).then(() => setUser(null));
    }
  };

  if (!user) return <div>Please log in to view your profile.</div>;

  return (
    <div className="profile">
      <h2>Your Profile</h2>
      <form onSubmit={handleUpdateProfile}>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
        />
        <button type="submit">Update Profile</button>
      </form>
      <button onClick={handleDeleteAccount}>Delete Account</button>
    </div>
  );
}

export default Profile;
