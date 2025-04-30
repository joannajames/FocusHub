// src/services/authService.js
import { signInWithPopup } from "firebase/auth";
import { auth, provider } from "@/firebase";

export async function loginWithGoogle() {
  // 1) sign in via Firebase
  const result  = await signInWithPopup(auth, provider);
  const idToken = await result.user.getIdToken(/* forceRefresh */ true);
  const email   = result.user.email;
  const username= email.split("@")[0];

  // 2) store for later API calls
  localStorage.setItem("username", username);

     // 3) keep only the Firebase ID-token
  localStorage.setItem("idToken", idToken);
  return { email, username };
}
