import React, { useState } from 'react';
import Card from '../ui/Card';
import Button from '../ui/Button';

function AddSourceForm({ sources, onAdd }) {
  const [url, setUrl] = useState('');
  const [source, setSource] = useState('');
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!url.trim()) {
      setError('Source URL is required.');
      return;
    }
    if (!source) {
      setError('Source website is required.');
      return;
    }

    try {
      setSubmitting(true);
      await onAdd({ url: url.trim(), source });
      setUrl('');
      setSource('');
    } catch (err) {
      console.error(err);
      setError('Failed to add source.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card className="settings-add-source">
      <h2 className="section-title">Add new source</h2>

      {error && <p className="text-error">{error}</p>}

      <form className="form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label className="form-label" htmlFor="source-url">
            Source URL
          </label>
          <input
            id="source-url"
            type="url"
            className="form-input"
            placeholder="https://example.com/listings/..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>

        <div className="form-field">
          <label className="form-label" htmlFor="source-select">
            Source website
          </label>
          <select
            id="source-select"
            className="form-input"
            value={source}
            onChange={(e) => setSource(e.target.value)}
          >
            <option value="">Select a source…</option>
            {sources.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>

        <div className="form-actions">
          <Button variant="primary" type="submit" disabled={submitting}>
            {submitting ? 'Adding…' : 'Add source'}
          </Button>
        </div>
      </form>
    </Card>
  );
}

export default AddSourceForm;
