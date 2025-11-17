import React from 'react';
import Card from '../ui/Card';

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

function KeyFactsSection({ building }) {
  const category = building.llm_residential_office;
  const area = building.a_surfaceArea;
  const price = building.a_price;

  const pricePerSq =
    price && area
      ? new Intl.NumberFormat('fr-FR', {
          style: 'currency',
          currency: 'EUR',
          maximumFractionDigits: 0
        }).format(price / area)
      : null;

  return (
    <Card className="building-section building-key-facts">
      <h2 className="section-title">Key facts</h2>
      <div className="two-column">
        <div>
          <h3 className="section-subtitle">General</h3>
          <dl className="definition-list">
            <div className="definition-item">
              <dt>Category</dt>
              <dd>
                {category
                  ? category === 'office'
                    ? 'Offices'
                    : 'Residential'
                  : 'N/A'}
              </dd>
            </div>
            <div className="definition-item">
              <dt>Area</dt>
              <dd>{area ? `${area} m²` : 'N/A'}</dd>
            </div>
            <div className="definition-item">
              <dt>Price</dt>
              <dd>{formatPrice(price)}</dd>
            </div>
            <div className="definition-item">
              <dt>Price per m²</dt>
              <dd>{pricePerSq ? `${pricePerSq} / m²` : 'N/A'}</dd>
            </div>
          </dl>
        </div>

        <div>
          <h3 className="section-subtitle">Location</h3>
          <dl className="definition-list">
            <div className="definition-item">
              <dt>City</dt>
              <dd>{building.a_city || 'N/A'}</dd>
            </div>
            <div className="definition-item">
              <dt>Postal code</dt>
              <dd>{building.a_postalCode || 'N/A'}</dd>
            </div>
            <div className="definition-item">
              <dt>Department</dt>
              <dd>{building.c_dept || 'N/A'}</dd>
            </div>
            <div className="definition-item">
              <dt>Region</dt>
              <dd>{building.c_region || 'N/A'}</dd>
            </div>
          </dl>
        </div>
      </div>
    </Card>
  );
}

export default KeyFactsSection;
