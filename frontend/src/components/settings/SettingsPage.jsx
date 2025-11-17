import React, { useEffect, useState } from 'react';
import { fetchSearchLinks, fetchSources, addSearchLink } from '../../api/settings';
import Card from '../ui/Card';
import LoadingState from '../ui/LoadingState';
import SourcesTable from './SourcesTable';
import AddSourceForm from './AddSourceForm';

function SettingsPage() {
  const [links, setLinks] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const reload = async () => {
    try {
      setLoading(true);
      setError('');
      const [linksData, sourcesData] = await Promise.all([
        fetchSearchLinks(),
        fetchSources()
      ]);
      setLinks(Array.isArray(linksData) ? linksData : []);
      setSources(Array.isArray(sourcesData) ? sourcesData : []);
    } catch (err) {
      console.error(err);
      setError('Failed to load settings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    reload();
  }, []);

  const handleAdd = async (payload) => {
    await addSearchLink(payload);
    await reload();
  };

  if (loading) {
    return <LoadingState message="Loading settings…" />;
  }

  return (
    <section className="page-section">
      <div className="page-header">
        <div>
          <h1 className="page-title">Settings</h1>
          <p className="page-subtitle">Listing sources</p>
        </div>
      </div>

      {error && (
        <Card>
          <p className="text-error">{error}</p>
        </Card>
      )}

      <SourcesTable links={links} />

      <AddSourceForm sources={sources} onAdd={handleAdd} />
    </section>
  );
}

export default SettingsPage;
