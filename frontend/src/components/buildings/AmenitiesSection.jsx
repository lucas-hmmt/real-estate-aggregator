import React from 'react';
import Card from '../ui/Card';

function formatAmenities(text) {
  if (!text) return null;
  // Very light splitting on commas for readability
  const parts = String(text)
    .split(',')
    .map((p) => p.trim())
    .filter(Boolean);
  if (!parts.length) return null;
  return parts;
}

function AmenitiesSection({ building }) {
  const amenitiesList = formatAmenities(building.llm_other);

  return (
    <Card className="building-section building-amenities">
      <h2 className="section-title">Amenities</h2>
      {amenitiesList ? (
        <ul className="amenities-list">
          {amenitiesList.map((item, idx) => (
            <li key={idx}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="text-secondary">No amenities information.</p>
      )}
    </Card>
  );
}

export default AmenitiesSection;
