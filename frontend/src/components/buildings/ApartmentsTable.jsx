import React from 'react';
import Card from '../ui/Card';
import Table, { TableHead, TableBody, TableRow, TableHeaderCell, TableCell } from '../ui/Table';

function parseFlatSizes(llm_flatSizes) {
  if (!llm_flatSizes || llm_flatSizes === '0') return [];
  if (Array.isArray(llm_flatSizes)) return llm_flatSizes;

  const trimmed = String(llm_flatSizes).trim();
  if (!trimmed) return [];

  return trimmed
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
    .map((s) => Number(s))
    .filter((n) => !Number.isNaN(n) && n > 0);
}

function ApartmentsTable({ building }) {
  const category = (building.llm_residential_office || '').toLowerCase();
  if (category !== 'residential') return null;

  const sizes = parseFlatSizes(building.llm_flatSizes);
  if (!sizes.length) return null;

  return (
    <Card className="building-section building-apartments">
      <h2 className="section-title">Apartments in this building</h2>
      <Table>
        <TableHead>
          <TableRow>
            <TableHeaderCell>#</TableHeaderCell>
            <TableHeaderCell>Size (m²)</TableHeaderCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {sizes.map((size, index) => (
            <TableRow key={index}>
              <TableCell>{index + 1}</TableCell>
              <TableCell>{size}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );
}

export default ApartmentsTable;
