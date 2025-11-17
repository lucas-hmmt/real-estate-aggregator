const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

async function request(path, options = {}) {
  const url = `${API_BASE_URL}${path}`;
  const headers = options.headers || {};

  const mergedOptions = {
    credentials: 'include',
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...headers
    }
  };

  const res = await fetch(url, mergedOptions);

  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`API error ${res.status}: ${text || res.statusText}`);
  }

  // For CSV downloads, caller will handle response differently
  const contentType = res.headers.get('Content-Type') || '';
  if (contentType.includes('text/csv')) {
    return res;
  }

  if (contentType.includes('application/json')) {
    return res.json();
  }

  // Fallback: text
  return res.text();
}

export { request };
