// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics , logEvent} from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDXikgKK8cKs-5WzKQuPgxESR0EWNgayG8",
  authDomain: "focushub-450719.firebaseapp.com",
  projectId: "focushub-450719",
  storageBucket: "focushub-450719.firebasestorage.app",
  messagingSenderId: "780726687923",
  appId: "1:780726687923:web:16fabd1e2bcfe6bb1ff8c6",
  measurementId: "G-KBZ4F2WCH3"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
logEvent(analytics, "notification_received");


const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider };