import React from "react";
import { NavLink } from "react-router-dom";
import "./NavBar.css";

function NavBar() {
  return (
    <nav className="navbar">
    <ul>
      <li><NavLink to="/">Home</NavLink></li>
      <li><NavLink to="/bus-stops">Bus Stops</NavLink></li>
      {user ? (
        <>
          <li><NavLink to="/favorites">Favorites</NavLink></li>
          <li><NavLink to="/profile">Profile</NavLink></li>
          <li><button onClick={logout}>Logout</button></li>
        </>
      ) : (
        <li><NavLink to="/login">Login</NavLink></li>
      )}
    </ul>
  </nav>
  );
}
export default NavBar;
