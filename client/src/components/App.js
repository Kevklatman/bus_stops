import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Header from "./Header";
import NavBar from "./NavBar";
import Footer from "./Footer";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Profile from "../pages/Profile";
import Favorites from "../pages/Favorites";
import BusStops from "../pages/BusStops";
import Schedule from "../pages/Schedule";
import AdminDashboard from "../pages/AdminDashboard";
import { UserProvider } from "../contexts/UserContext";

function App() {
  return (
    <UserProvider>
      <Router>
        <div className="App">
          <Header />
          <NavBar />
          <main>
            <Switch>
              <Route exact path="/" component={Home} />
              <Route path="/login" component={Login} />
              <Route path="/profile" component={Profile} />
              <Route path="/favorites" component={Favorites} />
              <Route path="/bus-stops" component={BusStops} />
              <Route path="/schedule/:stopId" component={Schedule} />
              <Route path="/admin" component={AdminDashboard} />
            </Switch>
          </main>
          <Footer />
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
