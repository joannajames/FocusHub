<template>
  <router-view />
</template>

<script>
import { defineComponent, onMounted } from 'vue';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { useAuthStatus } from '@/store/authStatus';

export default defineComponent({
  name: 'App',
  setup() {
    const { setLoggedIn } = useAuthStatus();

    onMounted(() => {
      const auth = getAuth();
      onAuthStateChanged(auth, (user) => {
        if (user && user.email.endsWith("@bu.edu")) {
          setLoggedIn(true);
        } else {
          setLoggedIn(false);
        }
      });
    });
  }
});
</script>
