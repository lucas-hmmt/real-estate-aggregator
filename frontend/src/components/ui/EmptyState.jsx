import React from 'react';
import { Link } from 'react-router-dom';
import Card from './Card';
import Button from './Button';

function EmptyState({ title, description, actionLabel, actionHref }) {
  return (
    <Card className="empty-state">
      <h2 className="empty-state-title">{title}</h2>
      {description && (
        <p className="empty-state-description">{description}</p>
      )}
      {actionLabel && actionHref && (
        <Link to={actionHref}>
          <Button variant="primary">{actionLabel}</Button>
        </Link>
      )}
    </Card>
  );
}

export default EmptyState;
