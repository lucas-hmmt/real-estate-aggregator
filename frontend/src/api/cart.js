import { request } from './client';

export async function fetchCart() {
  return request('/cart');
}

export async function addToCart(buildingId) {
  return request(`/cart/${buildingId}`, {
    method: 'POST'
  });
}

export async function removeFromCart(buildingId) {
  return request(`/cart/${buildingId}`, {
    method: 'DELETE'
  });
}

export async function exportCartCsv() {
  const res = await request('/export/cart', {
    method: 'GET'
  });

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'cart.csv';
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
}
