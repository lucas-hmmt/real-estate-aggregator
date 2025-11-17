import React from 'react';
import Card from '../ui/Card';

function parseImageUrls(a_images) {
  if (!a_images) return [];
  if (Array.isArray(a_images)) return a_images;

  const trimmed = String(a_images).trim();
  if (!trimmed) return [];

  if (trimmed.startsWith('[') || trimmed.startsWith('{')) {
    try {
      const parsed = JSON.parse(trimmed);
      if (Array.isArray(parsed)) return parsed;
    } catch (e) {}
  }

  return trimmed
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean);
}

function Gallery({ building }) {
  const images = parseImageUrls(building.a_images);
  const mainImage = images[0] || null;

  if (!images.length) {
    return (
      <Card className="building-gallery">
        <div className="building-gallery-placeholder">
          No photos available
        </div>
      </Card>
    );
  }

  return (
    <Card className="building-gallery">
      <div className="building-gallery-main">
        {mainImage && (
          <img
            src={mainImage}
            alt={building.a_title || 'Building'}
            className="building-gallery-main-image"
          />
        )}
      </div>
      {images.length > 1 && (
        <div className="building-gallery-thumbs">
          {images.slice(1).map((url, idx) => (
            <div key={idx} className="building-gallery-thumb">
              <img src={url} alt={`Photo ${idx + 2}`} />
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

export default Gallery;
