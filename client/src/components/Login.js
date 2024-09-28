import React, { useContext } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { UserContext } from "../contexts/UserContext";

const LoginSchema = Yup.object().shape({
  email: Yup.string().email("Invalid email").required("Required"),
  password: Yup.string().required("Required"),
});

function Login() {
  const { login } = useContext(UserContext);
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

  return (
    <div className="login">
      <h2>Login</h2>
      <Formik
        initialValues={{ email: "", password: "" }}
        validationSchema={LoginSchema}
        onSubmit={(values, { setSubmitting, setErrors }) => {
          fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(values),
          })
            .then((res) => {
              if (!res.ok) {
                throw new Error("Login failed");
              }
              return res.json();
            })
            .then((data) => {
              login(data);
              setSubmitting(false);
            })
            .catch((error) => {
              console.error("Error:", error);
              setErrors({ submit: error.message });
              setSubmitting(false);
            });
        }}
      >
        {({ isSubmitting, errors }) => (
          <Form>
            <div>
              <label htmlFor="email">Email</label>
              <Field type="email" name="email" />
              <ErrorMessage name="email" component="div" className="error" />
            </div>
            <div>
              <label htmlFor="password">Password</label>
              <Field type="password" name="password" />
              <ErrorMessage name="password" component="div" className="error" />
            </div>
            {errors.submit && <div className="error">{errors.submit}</div>}
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Logging in..." : "Login"}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
}

export default Login;
