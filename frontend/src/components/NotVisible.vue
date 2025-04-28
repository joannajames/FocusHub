<template>
  <div class="page-frame">
    <div class="container">
      <header class="header">
          <div class="nav-container">
          <img src="/icons/Menu_Burger.png" alt="Menu" class="menu-icon" @click="toggleDropdown"/>
            <ul class="dropdown" v-show="showDropdown">
              <li>
                <a href="#" @click="navigateTo('/the_hub')">
                  -&nbsp;&nbsp;&nbsp;the&nbsp;&nbsp;Hub
                  <img src="/icons/Hub_Stars.png" class="dropdown-icon" alt="the Hub Icon" />
                </a>
              </li>
              <li>
                <a href="#" @click="goToProfile">
                  -&nbsp;&nbsp;&nbsp;profile
                  <img src="/icons/Account_Signed_Out.png" class="dropdown-icon" alt="Profile Icon" />
                </a>
              </li>
              <li>
                <a href="#" @click="navigateTo('/chat_to_us')">
                  -&nbsp;&nbsp;&nbsp;chat&nbsp;&nbsp;to&nbsp;&nbsp;us
                  <img src="/icons/Chat_To_Us.png" class="dropdown-icon" alt="Chat to Us Icon" />
                </a>
              </li>
              <li>
                <a href="#" @click="navigateTo('/our_constitution')">
                  -&nbsp;&nbsp;&nbsp;our&nbsp;&nbsp;constitution
                  <img src="/icons/Scroll.png" class="dropdown-icon" alt="Constitution Icon" />
                </a>
              </li>
            </ul>
          </div>
        <div class="nav-section">
          <img :src="isLoggedIn ? '/icons/Account_Logged_In.png' : '/icons/Account_Signed_Out.png'"
               alt="Profile Icon" class="login-icon" @click="handleProfileClick"/>
          <img src="/icons/FocusHub_Logo.png" alt="FocusHub Logo" class="logo-icon" @click="navigateTo('/')" />
        </div>
      </header>

      <div class="main-content left-margin">
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <p> Error: login with your BU email to </p>
        <p> access this page </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import '@/assets/global.css';
import {ref, watch} from 'vue';
import { loginWithGoogle } from '@/services/authService';
import { useAuthStatus } from '@/store/authStatus';
import { auth } from '@/firebase';
import { signOut } from 'firebase/auth';
import router from "@/router";
import axios from 'axios';

const { isLoggedIn, setLoggedIn } = useAuthStatus();

const goToProfile = () => {
  showDropdown.value = false;
  router.push(isLoggedIn.value ? '/profile' : '/unavailable');
};

const showDropdown = ref(false);

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const navigateTo = (path) => {
  window.location.href = path;
  showDropdown.value = false;
};

const showCompleteProfilePopup = ref(false);
const completeProfileUserId = ref(null);

function openCompleteProfilePopup(userId) {
  showCompleteProfilePopup.value = true;
  completeProfileUserId.value = userId;
}

async function handleProfileClick() {
  if (isLoggedIn.value) {
    await signOut(auth);
    setLoggedIn(false);
  } else {
    const userCredential = await loginWithGoogle();
    const email = userCredential.user.email;

    const tokenResponse = await axios.post('/token', { email: email });
    const token = tokenResponse.data.access_token;
    localStorage.setItem('token', token);
    setLoggedIn(true);

    const profileResponse = await axios.get('/users/me', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (profileResponse.data.is_new_user) {
      openCompleteProfilePopup(profileResponse.data.user_id);
    } else {
      router.push('/');
    }
  }
}


watch(isLoggedIn, (newVal) => {
  if (newVal) {
    router.push('/profile');
  }
});
</script>

<style scoped>

p {
  font-size: 50px;
  line-height: 0.9;
  word-spacing: 4px;
  letter-spacing: 1px;
  font-family: 'Victor Mono', serif;
}

</style>
