// src/pages/Profile.js
import React, { useContext, useState } from "react";
import { UserContext } from "../contexts/UserContext";
import { useFormik } from 'formik';
import * as Yup from "yup";

function Profile() {
  const { user, setUser } = useContext(UserContext);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const ItemSchema = Yup.object().shape({
    name: Yup.string()
      .min(1, "Item name must be at least 1 character long")
      .required("Item name is required"),
    email: Yup.email("Invalid email format").required("email is required"),
  });
  

  const formik = useFormik({
    initialValues: {
      name: user ? user.name : "",
      email: user ? user.email : "",
    },
    validationSchema: ItemSchema,
    onSubmit: async (values) => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await fetch(`/passengers/${user.id}`, {
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(values), // Use Formik's values
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
    },
  });

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
      {error && <h2 className="error">{error}</h2>}
      {formik.errors&& Object.values(formik.errors).map(error => <h2>{error}</h2>)}
      <form onSubmit={formik.handleSubmit}>
        <input
          type="text"
          name="name"
          onChange={formik.handleChange}
          value={formik.values.name}
          placeholder="Name"
          disabled={isLoading}
        />
        <input
          type="email"
          name="email"
          onChange={formik.handleChange}
          value={formik.values.email}
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
