import React from 'react';
import { Routes, Route } from 'react-router-dom';

import BuildingsListPage from './components/buildings/BuildingsListPage';
import BuildingDetailPage from './components/buildings/BuildingDetailPage';
import SettingsPage from './components/settings/SettingsPage';
import CartPage from './components/cart/CartPage';

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<BuildingsListPage />} />
      <Route path="/buildings/:id" element={<BuildingDetailPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="/cart" element={<CartPage />} />
    </Routes>
  );
}

export default AppRoutes;
