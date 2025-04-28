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
        </div>
      </header>

      <div v-if="showCompleteProfilePopup" class="login-popup">
        <div class="popup-content">
            Please complete your profile!
            <br><br>
            <button @click="goToCompleteProfileForm">Fill Profile</button>
        </div>
      </div>

      <div class="main-content left-margin">
        <br>
        <br>
        <br>
        <p>
          This is
          <img src="/icons/Terrier.png" alt="Boston University Terrier" class="icon" />
          territory!
          Welcome to
          <img src="/icons/FocusHub_Logo.png" alt="FocusHub Logo" class="inline-logo" @click="navigateTo('/')"/>,
        </p>
        <p> a platform designed by we <span class="emoji">🂤</span> students </p>
        <p> for all you <span class="emoji">🎓</span>s. </p>
        <p> Scouting for good <span class="emoji">📚</span> spots? </p>
        <p> We've got you covered. </p>
        <p> Take a gander and <span class="emoji">👀</span> how your </p>
        <p> classmates <span class="emoji">🎼</span> 'em. </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { loginWithGoogle } from '@/services/authService';
import { useAuthStatus } from '@/store/authStatus';
import { auth } from '@/firebase';
import { signOut } from 'firebase/auth';
import router from "@/router";
const { isLoggedIn, setLoggedIn } = useAuthStatus();
import axios from 'axios';

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

function goToCompleteProfileForm() {
  showCompleteProfilePopup.value = false;
  router.push('/profile');  // or wherever you want them to fill in their profile
}

const goToProfile = () => {
  showDropdown.value = false;
  router.push(isLoggedIn.value ? '/profile' : '/unavailable');
};

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
</script>

<style>

p {
  font-family: 'Rubik Doodle Shadow', serif;
  font-size: 57px;
  line-height: 0.9;
  word-spacing: 4px;
  letter-spacing: 1px;
}

.icon {
  width: 75px;
  height: auto;
}

.inline-logo {
  height: 65px;
  vertical-align: middle;
  margin: -20px 6px;
  cursor: pointer;
}

.emoji {
  font-size: 3.5rem;
  vertical-align: middle;
}

</style>
