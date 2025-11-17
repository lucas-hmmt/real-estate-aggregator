import React from 'react';

function Button({ variant = 'primary', className = '', children, ...props }) {
  const base = 'btn';
  const variantClass =
    variant === 'secondary'
      ? 'btn-secondary'
      : variant === 'ghost'
      ? 'btn-ghost'
      : 'btn-primary';

  const fullClassName = `${base} ${variantClass} ${className}`.trim();

  return (
    <button className={fullClassName} {...props}>
      {children}
    </button>
  );
}

export default Button;
