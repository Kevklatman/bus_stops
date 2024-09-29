import React, { useContext } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import { UserContext } from "../contexts/UserContext";
import { useHistory } from "react-router-dom";

const LoginSchema = Yup.object().shape({
  email: Yup.string().email("Invalid email").required("Required"),
  password: Yup.string().required("Required"),
});

const RegisterSchema = Yup.object().shape({
  name: Yup.string().required("Required"),
  email: Yup.string().email("Invalid email").required("Required"),
  password: Yup.string()
    .min(6, "Password must be at least 6 characters")
    .required("Required"),
});

function LoginAndRegister() {
  const { login } = useContext(UserContext);
  const history = useHistory();

  const handleLogin = async (values, { setSubmitting, setErrors }) => {
    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      });
      if (!response.ok) {
        throw new Error("Login failed");
      }
      const userData = await response.json();
      login(userData);
      history.push("/");
    } catch (error) {
      setErrors({ submit: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  const handleRegister = async (values, { setSubmitting, setErrors }) => {
    try {
      const response = await fetch("/passengers", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(values),
      });
      if (!response.ok) {
        throw new Error("Registration failed");
      }
      const userData = await response.json();
      alert("Registration successful! Please log in.");
      // Optionally, you can automatically log the user in here
      // login(userData);
      // history.push('/');
    } catch (error) {
      setErrors({ submit: error.message });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="login-register">
      <div className="login-form">
        <h2>Login</h2>
        <Formik
          initialValues={{ email: "", password: "" }}
          validationSchema={LoginSchema}
          onSubmit={handleLogin}
        >
          {({ isSubmitting, errors }) => (
            <Form>
              <div>
                <label htmlFor="loginEmail">Email</label>
                <Field type="email" name="email" id="loginEmail" />
                <ErrorMessage name="email" component="div" className="error" />
              </div>
              <div>
                <label htmlFor="loginPassword">Password</label>
                <Field type="password" name="password" id="loginPassword" />
                <ErrorMessage
                  name="password"
                  component="div"
                  className="error"
                />
              </div>
              {errors.submit && <div className="error">{errors.submit}</div>}
              <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Logging in..." : "Login"}
              </button>
            </Form>
          )}
        </Formik>
      </div>

      <div className="register-form">
        <h2>Register New Passenger</h2>
        <Formik
          initialValues={{ name: "", email: "", password: "" }}
          validationSchema={RegisterSchema}
          onSubmit={handleRegister}
        >
          {({ isSubmitting, errors }) => (
            <Form>
              <div>
                <label htmlFor="registerName">Name</label>
                <Field type="text" name="name" id="registerName" />
                <ErrorMessage name="name" component="div" className="error" />
              </div>
              <div>
                <label htmlFor="registerEmail">Email</label>
                <Field type="email" name="email" id="registerEmail" />
                <ErrorMessage name="email" component="div" className="error" />
              </div>
              <div>
                <label htmlFor="registerPassword">Password</label>
                <Field type="password" name="password" id="registerPassword" />
                <ErrorMessage
                  name="password"
                  component="div"
                  className="error"
                />
              </div>
              {errors.submit && <div className="error">{errors.submit}</div>}
              <button type="submit" disabled={isSubmitting}>
                {isSubmitting ? "Registering..." : "Register"}
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
}

export default LoginAndRegister;
