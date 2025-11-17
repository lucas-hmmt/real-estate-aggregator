import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import { fetchBuildingById } from '../../api/buildings';
import { addToCart } from '../../api/cart';

import Card from '../ui/Card';
import Button from '../ui/Button';
import Tag from '../ui/Tag';
import LoadingState from '../ui/LoadingState';
import EmptyState from '../ui/EmptyState';

import Gallery from './Gallery';
import KeyFactsSection from './KeyFactsSection';
import MetricsSection from './MetricsSection';
import ApartmentsTable from './ApartmentsTable';
import AmenitiesSection from './AmenitiesSection';
import DescriptionSection from './DescriptionSection';

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

function formatPricePerSqMeter(price, surface) {
  const p = Number(price);
  const s = Number(surface);
  if (!p || !s || s <= 0) return null;
  const perSq = p / s;
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0
  }).format(perSq);
}

function BuildingDetailPage() {
  const { id } = useParams();
  const [building, setBuilding] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [addingToCart, setAddingToCart] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError('');
        const data = await fetchBuildingById(id);
        setBuilding(data || null);
      } catch (err) {
        console.error(err);
        setError('Failed to load building.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  const handleAddToCart = async () => {
    if (!building) return;
    try {
      setAddingToCart(true);
      await addToCart(building.a_id);
      alert('Added to cart.');
    } catch (err) {
      console.error(err);
      alert('Failed to add to cart.');
    } finally {
      setAddingToCart(false);
    }
  };

  const handleViewOriginal = () => {
    if (building && building.a_url) {
      window.open(building.a_url, '_blank', 'noopener,noreferrer');
    }
  };

  if (loading) {
    return <LoadingState message="Loading building…" />;
  }

  if (error || !building) {
    return (
      <EmptyState
        title="Building not found"
        description={error || 'This building could not be loaded.'}
      />
    );
  }

  const category = building.llm_residential_office;
  const pricePerSq = formatPricePerSqMeter(
    building.a_price,
    building.a_surfaceArea
  );

  const locationLineParts = [];
  if (building.a_city) locationLineParts.push(building.a_city);
  if (building.a_postalCode) locationLineParts.push(building.a_postalCode);
  const cityLine = locationLineParts.join(' ');

  const regionParts = [];
  if (building.c_dept) regionParts.push(`Département ${building.c_dept}`);
  if (building.c_region) regionParts.push(building.c_region);
  const regionLine = regionParts.join(', ');

  return (
    <section className="page-section">
      {/* Header / hero */}
      <div className="building-detail-header">
        <div className="building-detail-header-left">
          <div className="building-detail-title-row">
            <h1 className="page-title">
              {building.a_title || 'Untitled listing'}
            </h1>
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
          {cityLine && (
            <p className="building-detail-location">
              {cityLine}
              {regionLine ? `, ${regionLine}` : ''}
            </p>
          )}
        </div>
        <div className="building-detail-header-right">
          <div className="building-detail-price">
            {formatPrice(building.a_price)}
          </div>
          {pricePerSq && (
            <div className="building-detail-price-per-sqm">
              {pricePerSq} / m²
            </div>
          )}
          <div className="building-detail-actions">
            <Button variant="secondary" onClick={handleViewOriginal}>
              View original listing
            </Button>
            <Button
              variant="primary"
              onClick={handleAddToCart}
              disabled={addingToCart}
            >
              {addingToCart ? 'Adding…' : 'Add to cart'}
            </Button>
          </div>
        </div>
      </div>

      {/* Gallery */}
      <Gallery building={building} />

      {/* Key facts + metrics */}
      <div className="building-detail-main">
        <KeyFactsSection building={building} />
        <MetricsSection building={building} />
      </div>

      {/* Apartments (residential only) */}
      <ApartmentsTable building={building} />

      {/* Amenities & description */}
      <div className="building-detail-bottom">
        <AmenitiesSection building={building} />
        <DescriptionSection building={building} />
      </div>
    </section>
  );
}

export default BuildingDetailPage;
