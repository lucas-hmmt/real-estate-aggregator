import React from 'react';
import Card from './Card';

function LoadingState({ message = 'Loading…' }) {
  return (
    <Card className="loading-state">
      <div className="spinner" />
      <div className="loading-message">{message}</div>
    </Card>
  );
}

export default LoadingState;
