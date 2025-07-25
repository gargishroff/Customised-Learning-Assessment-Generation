import React from "react";
import "./navbar.css";

function Navbar() {
  return (
    <div className="navbar">
      <ul className="navbar-menu">
        <li>
          <a href="/">Generate New Assessment</a>
        </li>
        <li>
          <a href="/get_history">View Existing Assessments</a>
        </li>
      </ul>
    </div>
  );
}

export default Navbar;
