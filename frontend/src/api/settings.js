import { request } from './client';

export async function fetchSearchLinks() {
  return request('/settings/search-links');
}

export async function fetchSources() {
  return request('/settings/sources');
}

export async function addSearchLink({ url, source }) {
  return request('/settings/search-links', {
    method: 'POST',
    body: JSON.stringify({ url, source })
  });
}
