<template>
  <div class="container">
    <!-- Header with hamburger and account icons -->
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

      <!-- Logo navigates home -->
      <img
        src="/icons/FocushubLogo.png"
        alt="FocusHub Logo"
        class="logo-icon"
        @click="navigateTo('/')"
      />
    </header>

    <!-- Title aligned with form box -->
    <div class="form-container">
      <h1 class="title">Contact Us</h1>

      <form class="contact-form">
        <div class="field">
          <label for="name">name:</label>
          <input id="name" type="text" placeholder="......" />
        </div>

        <div class="field">
          <label for="email">email:</label>
          <input id="email" type="email" placeholder="......" />
        </div>

        <div class="field">
          <label>what's your query about?</label>
          <div class="tags">
            <span class="tag yellow">add study spot</span>
            <span class="tag peach">remove spot</span>
            <span class="tag pink">inaccurate info</span>
            <span class="tag green">report bug</span>
            <span class="tag blue">feedback</span>
            <span class="tag purple">partnerships</span>
          </div>
        </div>

        <div class="field">
          <label for="message">your message:</label>
          <textarea id="message" placeholder="type your message..."></textarea>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>

const navigateTo = (path) => {
  window.location.href = path;
};
</script>

<style scoped>
@font-face {
  font-family: 'Sansation Light';
  src: url('@/assets/Sansation_Light.ttf') format('truetype');
}

@import '@fontsource/rubik-doodle-shadow';

.container {
  background: #fdfde3;
  padding: 120px;
  font-family: 'Rubik Doodle Shadow', cursive;
}

/* Header */
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
  padding: 60px 40px; /* was 60px 20px */
  z-index: 1000;
  box-sizing: border-box;
}

/* Generic icon styling */
.icon {
  width: 220px;
  height: 170px;
  margin-top: 20px;
  cursor: pointer;
}

/* Specific size override for the logo */
.logo-icon {
  width: 120px;
  height: auto;
  margin-top: 20px;
  cursor: pointer;
}

/* Menu icon */
.menu-icon {
  width: 250px;
  height: 300px;
}

.nav-container {
  position: relative;
}

/* Dropdown menu */
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

/* Centered Title + Form Container */
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Contact Us Title aligned to box */
.title {
  font-size: 100px;
  margin-bottom: 40px;
  text-align: left;
  width: 100%;
  max-width: 900px;
}

/* Contact Form */
.contact-form {
  background: #fdfde3;
  border: 2px solid black;
  border-radius: 30px;
  padding: 60px 70px;
  font-family: 'Sansation Light', sans-serif;
  font-size: 20px;
  display: flex;
  flex-direction: column;
  gap: 40px;
  width: 100%;
  max-width: 900px;
}

/* Fields: label above input */
.field {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* Input & Textarea Styling */
input,
textarea {
  width: 100%;
  background-color: #f9fdad;
  border: 1px solid black;
  font-family: 'Sansation Light', sans-serif;
  padding: 14px 18px;
  font-size: 18px;
  border-radius: 12px;
}

textarea {
  height: 200px;
  resize: none;
}

/* Tags */
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.tag {
  font-size: 14px;
  border: 1px solid black;
  padding: 8px 14px;
  border-radius: 16px;
  font-family: 'Sansation Light', sans-serif;
}

.yellow { background: #ffffcc; }
.peach { background: #ffe2bb; }
.pink { background: #fcdce2; }
.green { background: #dcf7d3; }
.blue { background: #ddeeff; }
.purple { background: #f4dcf7; }
</style>