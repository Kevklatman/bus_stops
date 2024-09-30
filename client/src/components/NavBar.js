import React from "react";
import { NavLink } from "react-router-dom";
import "./NavBar.css";

function NavBar() {
  return (
    <header className="navbar">
      <NavLink to={"/"} className="button">
        Home
      </NavLink>

      <NavLink to={"/FavoritePage"} className="button">
        Favorite Stops
      </NavLink>

      <NavLink to={"/BustStopManagement "} className="button">
        Bust Stop Management 
      </NavLink>
    </header>
  );
}
export default NavBar;
