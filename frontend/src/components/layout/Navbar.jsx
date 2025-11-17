import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import Button from '../ui/Button';
import './Navbar.css'; // optional if you want extra styles, but not required

import { exportAllBuildingsCsv } from '../../api/buildings';

function Navbar() {
  const handleExportClick = async () => {
    try {
      await exportAllBuildingsCsv();
    } catch (err) {
      console.error(err);
      alert('Failed to export CSV.');
    }
  };

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="navbar-left">
          <Link to="/" className="navbar-logo">
            <span className="navbar-logo-mark">🏢</span>
            <span className="navbar-logo-text">Real Estate Aggregator</span>
          </Link>
        </div>
        <nav className="navbar-nav">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `navbar-link ${isActive ? 'navbar-link-active' : ''}`
            }
          >
            Buildings
          </NavLink>
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              `navbar-link ${isActive ? 'navbar-link-active' : ''}`
            }
          >
            Settings
          </NavLink>
        </nav>
        <div className="navbar-actions">
          <Button variant="secondary" onClick={handleExportClick}>
            Export all (CSV)
          </Button>
          <NavLink
            to="/cart"
            className={({ isActive }) =>
              `navbar-cart-link ${isActive ? 'navbar-link-active' : ''}`
            }
          >
            Cart
          </NavLink>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
