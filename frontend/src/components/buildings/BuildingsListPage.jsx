import React, { useEffect, useState } from 'react';
import { fetchBuildings } from '../../api/buildings';
import BuildingCard from './BuildingCard';
import EmptyState from '../ui/EmptyState';
import LoadingState from '../ui/LoadingState';
import Card from '../ui/Card';

function BuildingsListPage() {
  const [buildings, setBuildings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        setError('');
        const data = await fetchBuildings();
        setBuildings(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error(err);
        setError('Failed to load buildings.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return <LoadingState message="Loading buildings…" />;
  }

  if (error) {
    return (
      <Card>
        <p className="text-error">{error}</p>
      </Card>
    );
  }

  if (!buildings.length) {
    return (
      <EmptyState
        title="No buildings yet"
        description="Your database is empty. Run the scraping backend to collect listings."
      />
    );
  }

  return (
    <section className="page-section">
      <div className="page-header">
        <div>
          <h1 className="page-title">Buildings</h1>
          <p className="page-subtitle">All buildings in your database.</p>
        </div>
        <div className="page-header-meta">
          <span className="text-secondary">
            {buildings.length} {buildings.length === 1 ? 'building' : 'buildings'}
          </span>
        </div>
      </div>

      <div className="buildings-grid">
        {buildings.map((b) => (
          <BuildingCard key={b.a_id} building={b} />
        ))}
      </div>
    </section>
  );
}

export default BuildingsListPage;
