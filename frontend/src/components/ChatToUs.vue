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
               div v-if="showCompleteProfilePopup" class="login-popup">
                <div class="popup-content">
                    Please complete your profile!
                    <br><br>
                    <button @click="goToCompleteProfileForm">Fill Profile</button>
                </div>
              </div>
              <div class="main-content">
                <h1 class="title">chat to us</h1>

                <div class="form-wrapper">
                  <form class="contact-form">
                    <div class="submit-icon-wrapper">
                      <img src="/icons/Send.png" alt="Submit" class="submit-icon" @click="submitForm" />
                    </div>

                    <div class="field">
                      <label for="name">name:</label>
                      <input id="name" type="text" placeholder="  . . . . . . . . . . . . . . ." />
                    </div>

                    <div class="field">
                      <label for="email">email:</label>
                      <input id="email" type="email" placeholder="  . . . . . . . . . . . . . . ." />
                    </div>

                    <div class="field">
                      <label>subject:</label>
                    <div class="tags">
                      <span
                        v-for="tag in queryOptions"
                        :key="tag"
                        :class="{ tag: true, active: selectedTag === tag, [tagClasses[tag]]: true }"
                        @click="selectedTag = tag"
                      >
                        {{ tag }}
                      </span>
                    </div>
                  </div>

                    <div class="field">
                      <label for="message">your message:</label>
                      <textarea id="message" placeholder="  . . . . . . . . . . . . . . ."></textarea>
                    </div>
                  </form>
                </div>
              </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { contactTags, tagColors } from '@/constants/Tags';
import '@/assets/global.css';

import { loginWithGoogle } from '@/services/authService';
import { useAuthStatus } from '@/store/authStatus';
import { auth } from '@/firebase';
import { signOut } from 'firebase/auth';
import router from "@/router";
import axios from 'axios';
const { isLoggedIn, setLoggedIn } = useAuthStatus();


const showDropdown = ref(false);

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const navigateTo = (path) => {
  window.location.href = path;
  showDropdown.value = false; // hide after click
};

const goToProfile = () => {
  showDropdown.value = false;
  router.push(isLoggedIn.value ? '/profile' : '/unavailable');
};

const selectedTag = ref('');

const queryOptions = contactTags;

const tagClasses = tagColors;

const submitForm = () => {
  const name = document.getElementById('name').value || 'N/A';
  const email = document.getElementById('email').value || 'N/A';
  const message = document.getElementById('message').value || 'N/A';
  const tag = selectedTag.value || 'General';

  const subject = encodeURIComponent(tag);
  const body = encodeURIComponent(`Hi FocusHub,\n\n${message}\n\n\nThank you,\n\n${name}\n${email}`);
  window.location.href = `mailto:hi.focushub@gmail.com?subject=${subject}&body=${body}`;
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

<style scoped>

.title {
  text-align: center;
}

.form-wrapper {
  position: relative;
  display: flex;
  justify-content: center; /* centre horizontally */
  align-items: center;
  margin-top: 25px;
}

.contact-form {
  display: flex;
  flex-direction: column;
  position: relative;
  width: 50%;
  max-width: 900px;
  gap: 40px;
  padding: 40px 40px;
  font-family: 'Sansation Light', serif;
  font-style: italic;
  font-size: 20px;
  background: #fdfde3;
  border: 2px solid black;
  border-radius: 30px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

input{
  width: 97%;
  height: 25px;
  padding: 10px;
  font-family: 'Sansation Light', serif;
  font-size: 18px;
  color: gray;
  background-color: #f9fdad;
  border: 1.5px solid black;
  border-radius: 22px;
}

textarea {
  width: 97%;
  height: 90px;
  padding: 10px;
  font-family: 'Sansation Light', serif;
  font-size: 18px;
  color: gray;
  background-color: #f9fdad;
  border: 1.5px solid black;
  border-radius: 22px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag.active {
  border: 2px solid black;
  box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

</style>
