import React from 'react';

function PageContainer({ children }) {
  return (
    <main className="page-container">
      {children}
    </main>
  );
}

export default PageContainer;
