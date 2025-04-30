import { getAuth } from "firebase/auth";

export async function apiFetch(endpoint, options = {}) {
  const baseUrl = process.env.VUE_APP_API_URL;

  // Get Firebase ID token
  const auth = getAuth();
  const waitForUser = () =>
    new Promise((resolve, reject) => {
      const unsub = auth.onAuthStateChanged((user) => {
        unsub();
        if (user) resolve(user);
        else reject(new Error("User not authenticated."));
      });
    });

  const user = auth.currentUser || await waitForUser();
  const idToken = await user.getIdToken();

  const headers = {
    "Content-Type": "application/json",
    ...(idToken ? { Authorization: `Bearer ${idToken}` } : {}),
    ...options.headers,
  };

  console.log("About to fetch:", `${baseUrl}${endpoint}`);
  const resp = await fetch(`${baseUrl}${endpoint}`, {
    ...options,
    headers,
  });

  let responseBody;
  try {
    responseBody = await resp.clone().json();
  } catch (e) {
    responseBody = await resp.text();
  }

  if (!resp.ok) {
    const message = typeof responseBody === "string"
      ? responseBody
      : responseBody.detail || "Unknown error";
    throw new Error(`API Error ${resp.status}: ${message}`);
  }

  return responseBody;
}