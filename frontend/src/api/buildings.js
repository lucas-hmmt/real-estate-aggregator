import { request } from './client';

export async function fetchBuildings() {
  return request('/buildings');
}

export async function fetchBuildingById(id) {
  return request(`/buildings/${id}`);
}

export async function exportAllBuildingsCsv() {
  const res = await request('/export/buildings', {
    method: 'GET'
  });

  // res is a Response (CSV); trigger download
  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'buildings.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
