// src/components/App.js
import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Footer from "./Footer";
import NavBar from "./NavBar";
import Header from "./Header";
import Home from "../pages/Home";
import BusStops from "../pages/BusStops";
import Favorites from "../pages/Favorites";
import Schedule from "../pages/Schedule";
import Profile from "../pages/Profile";
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
            <Route path="/schedule" component={Schedule} />
            <Route path="/profile" component={Profile} />
          </Switch>
          <Footer />
        </div>
      </Router>
    </UserProvider>
  );
  // <h1>Project Client</h1>;
}

export default App;
