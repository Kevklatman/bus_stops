import React, { useContext } from "react";
import {
  BrowserRouter as Router,
  Route,
  Switch,
  Redirect,
} from "react-router-dom";
import { UserProvider, UserContext } from "./contexts/UserContext";
import NavBar from "./components/NavBar";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";
import Favorites from "./pages/Favorites";
import BusStops from "./pages/BusStops";
import Schedule from "./pages/Schedule";
import AdminDashboard from "./pages/AdminDashboard";

function PrivateRoute({ children, ...rest }) {
  const { user } = useContext(UserContext);
  return (
    <Route
      {...rest}
      render={({ location }) =>
        user ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/login",
              state: { from: location },
            }}
          />
        )
      }
    />
  );
}

function AdminRoute({ children, ...rest }) {
  const { user } = useContext(UserContext);
  return (
    <Route
      {...rest}
      render={({ location }) =>
        user && user.isAdmin ? (
          children
        ) : (
          <Redirect
            to={{
              pathname: "/",
              state: { from: location },
            }}
          />
        )
      }
    />
  );
}

function App() {
  return (
    <UserProvider>
      <Router>
        <NavBar />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/login" component={Login} />
          <Route path="/register" component={Register} />
          <PrivateRoute path="/profile">
            <Profile />
          </PrivateRoute>
          <PrivateRoute path="/favorites">
            <Favorites />
          </PrivateRoute>
          <Route path="/bus-stops" component={BusStops} />
          <Route path="/schedule/:stopId" component={Schedule} />
          <AdminRoute path="/admin">
            <AdminDashboard />
          </AdminRoute>
        </Switch>
        <Footer />
      </Router>
    </UserProvider>
  );
}

export default App;
