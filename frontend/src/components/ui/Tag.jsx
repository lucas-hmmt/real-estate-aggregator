import React from 'react';

function Tag({ variant = 'default', children }) {
  let variantClass = 'tag-default';
  if (variant === 'success') variantClass = 'tag-success';
  else if (variant === 'info') variantClass = 'tag-info';

  return <span className={`tag ${variantClass}`}>{children}</span>;
}

export default Tag;
