import { ref } from 'vue';
import { auth } from '@/firebase';
import { onAuthStateChanged } from 'firebase/auth';

const isLoggedIn = ref(false);

const setLoggedIn = (val) => {
  isLoggedIn.value = val;
  localStorage.setItem('isLoggedIn', val.toString());
};

// initialise once
onAuthStateChanged(auth, (user) => {
  isLoggedIn.value = !!user;
  localStorage.setItem('isLoggedIn', isLoggedIn.value.toString());
});

export function useAuthStatus() {
  return { isLoggedIn, setLoggedIn };
}
