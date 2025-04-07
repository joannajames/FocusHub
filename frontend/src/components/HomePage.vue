<template>
  <div class="container">
    <header class="header">
      <div class="nav-container">
        <img
          src="/icons/Menu_Burger.png"
          alt="Menu"
          class="icon menu-icon"
        />
        <ul class="dropdown">
          <li><a href="#" @click="navigateTo('/the_hub')">The Hub</a></li>
          <li><a href="#" @click="navigateTo('/contact_us')">Contact Us</a></li>
          <li><a href="#" @click="navigateTo('/account')">Account</a></li>
        </ul>
      </div>

    </header>

    <p>
      This is&nbsp;
      <img
        src="https://a.espncdn.com/guid/c9b15717-b2d4-9e2b-2d8f-e02bc806fcae/logos/secondary_logo_on_white_color.png"
        alt="Boston University Terrier"
        class="emoji"
      />&nbsp;territory!
      Welcome to
      <img
        src="/icons/FocushubLogo.png"
        alt="FocusHub Logo"
        class="inline-logo"
        @click="navigateTo('/')"
      />,
    </p>

    <p> a platform designed by we <span class="emoji">🂤</span> students </p>
    <p> for all you <span class="emoji">🎓</span>s. </p>
    <p> Scouting for good <span class="emoji">📚</span> spots? </p>
    <p> We've got you covered. </p>
    <p> Take a gander and <span class="emoji">👀</span> how your </p>
    <p> classmates <span class="emoji">🎼</span> 'em. </p>
  </div>
</template>

<script setup>

const navigateTo = (path) => {
  window.location.href = path;
};
</script>

@font-face {
  font-family: 'Sansation Light';
  src: url('@/assets/Sansation_Light.ttf') format('truetype');
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

/* Paragraph text */
p {
  font-size: 52px;
  line-height: 0.9;
  word-spacing: 4px;
  letter-spacing: 1px;
}

/* Emojis and inline icons */
.emoji {
  width: 80px;
  height: 80px;
  vertical-align: middle;
  font-size: 3.5rem;
}

.inline-logo {
  height: 65px;
  vertical-align: middle;
  cursor: pointer;
  margin: 0 6px;
}

/* Header Styles */
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

/* Icons */
.icon {
  width: 220px;
  height: 170px;
  margin-top: 20px;
  cursor: pointer;
}

.menu-icon {
  width: 250px;
  height: 300px;
}

/* Navigation dropdown */
.nav-container {
  position: relative;
}

.dropdown {
  display: none;
  position: absolute;
  top: 150px;
  right: 0;
  background: #fdfde3;
  border: 1px solid black;
  list-style: none;
  padding: 10px;
  font-size: 20px;
  font-family: 'Sansation Light', sans-serif;
}

/* SHOW on hover */
.nav-container:hover .dropdown {
  display: block;
}

.dropdown li {
  padding: 30px 30px;
}

.dropdown li a {
  text-decoration: none;
  color: black;
}
</style>