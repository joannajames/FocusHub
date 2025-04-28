<template>
  <router-view/>
</template>

<script>
import { defineComponent } from 'vue';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '@/firebase';

onAuthStateChanged(auth, (user) => {
  if (user) {
    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('userEmail', user.email); // optional
  } else {
    localStorage.setItem('isLoggedIn', 'false');
    localStorage.removeItem('userEmail');
  }
});

export default defineComponent({
  name: 'App'
});
</script>
