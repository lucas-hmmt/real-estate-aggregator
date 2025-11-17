import React from 'react';
import Card from '../ui/Card';

function formatPercent(value) {
  if (value == null) return 'N/A';
  const num = Number(value);
  if (Number.isNaN(num)) return 'N/A';
  return `${(num * 100).toFixed(1)} %`;
}

function formatCurrency(value) {
  if (value == null) return 'N/A';
  const num = Number(value);
  if (Number.isNaN(num)) return 'N/A';
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0
  }).format(num);
}

function MetricCard({ title, main, score }) {
  return (
    <div className="metric-card">
      <div className="metric-title">{title}</div>
      <div className="metric-main">{main}</div>
      {score != null && (
        <div className="metric-score">Score: {score} / 10</div>
      )}
    </div>
  );
}

function MetricsSection({ building }) {
  const councilTax = building.c_taxHab;
  const propertyTax = building.c_taxFonc;
  const vacancy = building.c_vacancy;
  const vacancyCat = building.c_vacancyCat;
  const revenue = building.c_revenue;
  const revenueCat = building.c_revenueCat;

  return (
    <Card className="building-section building-metrics">
      <h2 className="section-title">Rental & tax metrics</h2>
      <div className="metric-grid">
        <MetricCard
          title="Council tax"
          main={
            councilTax != null ? `Council tax: ${formatPercent(councilTax)}` : 'N/A'
          }
          score={null} // can add category later if you derive one
        />

        <MetricCard
          title="Property tax"
          main={
            propertyTax != null ? `Property tax: ${formatPercent(propertyTax)}` : 'N/A'
          }
          score={null}
        />

        <MetricCard
          title="Vacancy rate"
          main={
            vacancy != null ? `Vacancy rate: ${formatPercent(vacancy)}` : 'N/A'
          }
          score={vacancyCat}
        />

        <MetricCard
          title="Median city income"
          main={
            revenue != null ? `Median income: ${formatCurrency(revenue)}` : 'N/A'
          }
          score={revenueCat}
        />
      </div>
    </Card>
  );
}

export default MetricsSection;
