import React from 'react';

function Card({ className = '', children }) {
  const fullClassName = `card ${className}`.trim();
  return <div className={fullClassName}>{children}</div>;
}

export default Card;
