// src/services/authService.js
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "@/firebase";

export async function loginWithGoogle() {
  const result = await signInWithPopup(auth, provider);
  const idToken = await result.user.getIdToken();

  const email = result.user.email;
  const username = email.split('@')[0];

  localStorage.setItem("username", username);

  // Send to backend to get JWT
  const res = await fetch("http://localhost:8000/auth/google", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: idToken }),
  });

  const data = await res.json();
  localStorage.setItem("jwt", data.access_token);

  return data;
}
