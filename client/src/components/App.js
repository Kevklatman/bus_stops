// src/components/App.js
import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import { UserProvider } from "../contexts/UserContext";
import Footer from "./Footer";
import NavBar from "./NavBar";
import Header from "./Header";
import Home from "../pages/Home";
import BusStops from "../pages/BusStops";
import Favorites from "../pages/Favorites";
import Schedule from "../pages/Schedule";
import Profile from "../pages/Profile";
import BusDetails from "../pages/BusDetails";
import "../index.css";

function App() {
  return (
    <UserProvider>
      <Router>
        <div className="App">
          <Header />
          <NavBar />
          <Switch>
            <Route exact path="/" component={Home} />
            <Route path="/bus-stops" component={BusStops} />
            <Route path="/favorites" component={Favorites} />
            <Route path="/schedule/:stopId" component={Schedule} />
            <Route path="/profile" component={Profile} />
            <Route path="/bus/:busId" component={BusDetails} />
          </Switch>
          <Footer />
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
