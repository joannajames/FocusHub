<template>
  <div class="container">
    <header class="header">

      <div class="nav-container">
        <img src="/icons/Menu_Burger.png" alt="Menu" class="icon menu-icon" @click="toggleDropdown" />
        <ul v-if="isDropdownOpen" class="dropdown">
          <li><a href="#" @click="navigateTo('/the_hub')">The Hub</a></li>
          <li><a href="#" @click="navigateTo('/contact_us')">Contact Us</a></li>
        </ul>
      </div>

      <img src="/icons/User_Account.png" alt="Account" class="icon account-icon" @click="goToAccount" />
    </header>

    <p> This is&nbsp; <img src="https://a.espncdn.com/guid/c9b15717-b2d4-9e2b-2d8f-e02bc806fcae/logos/secondary_logo_on_white_color.png" alt="boston university terrier" class="emoji">&nbsp; territory! Welcome to <span class="blank">_______</span>, </p>
    <p> a platform designed by we&nbsp; <span class="emoji">🂤 </span>&nbsp; students </p>
    <p> for all you&nbsp; <span class="emoji">🎓</span>s. </p>
    <p> Scouting for good&nbsp; <span class="emoji">📚</span>&nbsp; spots? </p>
    <p> We've got you covered. </p>
    <p> Take a gander and&nbsp; <span class="emoji">👀</span>&nbsp; how your </p>
    <p> classmates&nbsp; <span class="emoji">🎼</span>&nbsp; 'em. </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isDropdownOpen = ref(false);

const goToAccount = () => {
  window.location.href = "/account";
};

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const navigateTo = (path) => {
  window.location.href = path;
};
</script>

@font-face {
  font-family: 'Sansation Light';
  src: url('@/assets/sansation/Sansation-Light.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

<style scoped>
@import '@fontsource/rubik-doodle-shadow';

.container {
  font-family: 'Rubik Doodle Shadow', cursive;
  background: #fdfde3;
  padding: 120px;
  text-align: left;
}

p {
  font-size: 52px;
  line-height: 0.9;
  word-spacing: 4px;
  letter-spacing: 1px;
}

.emoji {
  width: 80px;
  height: 80px;
  vertical-align: middle;
  font-size: 3.5rem;
}

.blank {
  border-bottom: 2px solid black;
  padding: 2px 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 60px;
  background: #fdfde3;
  padding: 60px 20px;
  z-index: 1000;
}

.icon {
  width: 200px;
  height: 150px;
  cursor: pointer;
}

.account-icon {
  width: 200px;
  height: 150px;
}

.menu-icon {
  width: 250px;
  height: 300px;
}

.nav-container {
  position: relative;
}

.dropdown {
  font-family: 'Sansation Light', sans-serif;
  position: absolute;
  top: 150px;
  right: 0;
  background: #fdfde3;
  border: 1px solid black;
  list-style: none;
  padding: 10px;
  font-size: 20px;
}

.dropdown li {
  padding: 30px 30px;
}

.dropdown li a {
  text-decoration: none;
  color: black;
}
</style>
