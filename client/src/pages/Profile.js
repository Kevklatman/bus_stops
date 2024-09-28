import React, { useContext, useState } from "react";
import { UserContext } from "../contexts/UserContext";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const ProfileSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, "Name must be at least 2 characters long")
    .required("Name is required"),
  email: Yup.string()
    .email("Invalid email format")
    .required("Email is required"),
});

function Profile() {
  const { user, setUser } = useContext(UserContext);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!user) return <div>Please log in to view your profile.</div>;

  return (
    <div className="profile">
      <h2>Your Profile</h2>
      {error && <div className="error">{error}</div>}
      <Formik
        initialValues={{
          name: user.name,
          email: user.email,
        }}
        validationSchema={ProfileSchema}
        onSubmit={async (values, { setSubmitting }) => {
          setIsLoading(true);
          setError(null);
          try {
            const response = await fetch(`/passengers/${user.id}`, {
              method: "PATCH",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify(values),
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
            setSubmitting(false);
          }
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <div>
              <label htmlFor="name">Name</label>
              <Field type="text" name="name" />
              <ErrorMessage name="name" component="div" className="error" />
            </div>
            <div>
              <label htmlFor="email">Email</label>
              <Field type="email" name="email" />
              <ErrorMessage name="email" component="div" className="error" />
            </div>
            <button type="submit" disabled={isSubmitting || isLoading}>
              {isLoading ? "Updating..." : "Update Profile"}
            </button>
          </Form>
        )}
      </Formik>
      <button
        onClick={async () => {
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
        }}
        disabled={isLoading}
      >
        {isLoading ? "Deleting..." : "Delete Account"}
      </button>
    </div>
  );
}

export default Profile;
