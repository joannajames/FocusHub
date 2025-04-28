export async function apiFetch(endpoint, options = {}) {
  const baseUrl = process.env.VUE_APP_API_URL;
  console.log('BASE URL being used:', baseUrl);

  const response = await fetch(`${baseUrl}${endpoint}`, options);

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`API Error: ${response.status} ${errorText}`);
  }

  return response.json();
}
