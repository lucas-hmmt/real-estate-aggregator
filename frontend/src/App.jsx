import React from 'react';
import Navbar from './components/layout/Navbar';
import PageContainer from './components/layout/PageContainer';
import AppRoutes from './router';

function App() {
  return (
    <div className="app-root">
      <Navbar />
      <PageContainer>
        <AppRoutes />
      </PageContainer>
    </div>
  );
}

export default App;
