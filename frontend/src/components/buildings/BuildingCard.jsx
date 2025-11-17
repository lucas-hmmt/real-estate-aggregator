import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../ui/Card';
import Tag from '../ui/Tag';

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

function formatPrice(value) {
  if (value == null) return 'N/A';
  const num = Number(value);
  if (Number.isNaN(num)) return 'N/A';
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0
  }).format(num);
}

function BuildingCard({ building }) {
  const images = parseImageUrls(building.a_images);
  const mainImage = images[0] || null;
  const category = building.llm_residential_office;

  return (
    <Card className="building-card">
      <Link to={`/buildings/${building.a_id}`} className="building-card-link">
        <div className="building-card-image-wrapper">
          {mainImage ? (
            <img
              src={mainImage}
              alt={building.a_title || 'Building'}
              className="building-card-image"
            />
          ) : (
            <div className="building-card-image-placeholder">
              No photo
            </div>
          )}
        </div>

        <div className="building-card-body">
          <div className="building-card-header">
            <h2 className="building-card-title">
              {building.a_title || 'Untitled listing'}
            </h2>
            {category && (
              <Tag
                variant={
                  category.toLowerCase() === 'residential' ? 'success' : 'info'
                }
              >
                {category === 'office' ? 'Offices' : 'Residential'}
              </Tag>
            )}
          </div>

          <div className="building-card-price">
            {formatPrice(building.a_price)}
          </div>

          <div className="building-card-footer">
            <span className="building-card-link-text">View details →</span>
          </div>
        </div>
      </Link>
    </Card>
  );
}

export default BuildingCard;
