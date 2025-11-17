import React from 'react';
import Card from '../ui/Card';

function DescriptionSection({ building }) {
  return (
    <Card className="building-section building-description">
      <h2 className="section-title">Description</h2>
      {building.a_description ? (
        <p className="description-text">{building.a_description}</p>
      ) : (
        <p className="text-secondary">No description available.</p>
      )}
    </Card>
  );
}

export default DescriptionSection;
