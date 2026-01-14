import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1>
          <span className="header-icon">🛠️</span>
          Tool Hub
        </h1>
        <p className="header-subtitle">Centralized development tools</p>
      </div>
    </header>
  );
}

export default Header;
