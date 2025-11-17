import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../ui/Card';
import Button from '../ui/Button';

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

function CartItemCard({ building, onRemove }) {
  const images = parseImageUrls(building.a_images);
  const mainImage = images[0] || null;

  const handleRemove = () => {
    onRemove(building.a_id);
  };

  return (
    <Card className="cart-item-card">
      <div className="cart-item-inner">
        <Link to={`/buildings/${building.a_id}`} className="cart-item-main">
          <div className="cart-item-image-wrapper">
            {mainImage ? (
              <img
                src={mainImage}
                alt={building.a_title || 'Building'}
                className="cart-item-image"
              />
            ) : (
              <div className="cart-item-image-placeholder">No photo</div>
            )}
          </div>
          <div className="cart-item-body">
            <h2 className="cart-item-title">
              {building.a_title || 'Untitled listing'}
            </h2>
            <div className="cart-item-price">
              {formatPrice(building.a_price)}
            </div>
            <div className="cart-item-link">View details →</div>
          </div>
        </Link>
        <div className="cart-item-actions">
          <Button variant="secondary" onClick={handleRemove}>
            Remove from cart
          </Button>
        </div>
      </div>
    </Card>
  );
}

export default CartItemCard;
