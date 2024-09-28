// src/pages/Profile.js
import React, { useContext, useState } from "react";
import { UserContext } from "../contexts/UserContext";

function Profile() {
  const { user, setUser } = useContext(UserContext);
  const [name, setName] = useState(user ? user.name : "");
  const [email, setEmail] = useState(user ? user.email : "");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`/passengers/${user.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name, email }),
      });
      if (!response.ok) {
        throw new Error("Failed to update profile");
      }
      const updatedUser = await response.json();
      setUser(updatedUser);
      alert("Profile updated successfully!");
    } catch (error) {
      console.error("Error updating profile:", error);
      setError("Failed to update profile. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteAccount = async () => {
    if (window.confirm("Are you sure you want to delete your account?")) {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`/passengers/${user.id}`, {
          method: "DELETE",
        });
        if (!response.ok) {
          throw new Error("Failed to delete account");
        }
        setUser(null);
        alert("Account deleted successfully");
      } catch (error) {
        console.error("Error deleting account:", error);
        setError("Failed to delete account. Please try again.");
      } finally {
        setIsLoading(false);
      }
    }
  };

  if (!user) return <div>Please log in to view your profile.</div>;

  return (
    <div className="profile">
      <h2>Your Profile</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          disabled={isLoading}
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Updating..." : "Update Profile"}
        </button>
      </form>
      <button onClick={handleDeleteAccount} disabled={isLoading}>
        {isLoading ? "Deleting..." : "Delete Account"}
      </button>
    </div>
  );
}

export default Profile;
