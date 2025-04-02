<template>
  <div class="container">
    <!-- Header -->
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

    <!-- Title -->
    <h1 class="title">Profile</h1>

    <!-- Full-Width Profile Card -->
    <div class="card full-width user-card">
      <img src="/images/Anastasia.jpg" alt="Anastasia" class="avatar" />
      <div class="info">
        <h2>Anastasia</h2>
        <p><em>Undergraduate • College of Arts & Sciences • Sociology</em></p>
        <div class="tags">
          <span class="tag peach">pet-friendly</span>
          <span class="tag green">phone booths</span>
          <span class="tag blue">prayer space</span>
          <span class="tag purple">vegan</span>
          <span class="tag yellow">free</span>
        </div>
      </div>
    </div>

    <!-- Grid for Classes + Friends -->
    <div class="grid">
      <!-- LEFT COLUMN -->
      <div class="left">
        <div class="card">
          <h3>classes I’m taking now...</h3>
          <div class="course-tags">
            <span class="course">CAS SO 190</span>
            <span class="course">CAS SO 201</span>
            <span class="course">CAS SO 203</span>
          </div>
        </div>

        <div class="card">
          <h3>my reviews</h3>
          <!-- Content coming soon -->
        </div>
      </div>

      <!-- RIGHT COLUMN: Friends -->
      <div class="right">
        <div class="friend-card" v-for="peer in peers" :key="peer.name">
          <img :src="peer.avatar" :alt="peer.name" class="avatar-small" />
          <div class="peer-info">
            <h4>{{ peer.name }}</h4>
            <p><em>{{ peer.program }}</em></p>
            <span class="course">{{ peer.course }}</span>
            <div class="tags">
              <span class="tag" :class="peer.tagClass">{{ peer.tag }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

const navigateTo = (path) => {
  window.location.href = path;
};

const peers = [
  {
    name: 'Ibrahim',
    program: 'MA • College of Arts & Sciences • Sociology',
    course: 'CAS SO 203',
    tag: 'vegan',
    tagClass: 'purple',
    avatar: '/images/Ibrahim.jpg',
  },
  {
    name: 'Rachel',
    program: 'PhD • Questrom School of Business • Finance',
    course: 'CAS SO 203',
    tag: 'prayer space',
    tagClass: 'blue',
    avatar: '/images/Rachel.jpg',
  },
  {
    name: 'Rinka',
    program: 'Undergrad • College of Engineering • Engineering',
    course: 'CAS SO 190',
    tag: 'phone booths',
    tagClass: 'green',
    avatar: '/images/Rinka.jpg',
  },
];
</script>

<style scoped>
@font-face {
  font-family: 'Sansation Light';
  src: url('@/assets/Sansation_Light.ttf') format('truetype');
}

@import '@fontsource/rubik-doodle-shadow';
@import '@fontsource/rubik-gemstones';

.container {
  background: #fdfde3;
  padding: 120px;
  font-family: 'Sansation Light', sans-serif;
}

.title {
  font-family: 'Rubik Doodle Shadow', cursive;
  font-size: 100px;
  margin-bottom: 40px;
}

/* HEADER */
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
  padding: 60px 40px;
  z-index: 1000;
  box-sizing: border-box;
}

.icon {
  width: 220px;
  height: 170px;
  margin-top: 20px;
  cursor: pointer;
}

.logo-icon {
  width: 120px;
  height: auto;
  margin-top: 20px;
  cursor: pointer;
}

.menu-icon {
  width: 250px;
  height: 300px;
}

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

/* GRID */
.grid {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.left, .right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* PROFILE CARD */
.full-width {
  width: 100%;
  margin-bottom: 40px;
}

.card {
  background: #fdfde3;
  border: 2px solid black;
  border-radius: 20px;
  padding: 30px;
}

.user-card {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.avatar {
  width: 100px;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 20px;
}

.info h2 {
  font-size: 28px;
  margin-bottom: 5px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.tag {
  font-size: 14px;
  border: 1px solid black;
  padding: 6px 12px;
  border-radius: 14px;
}

.pink { background: #fbc4d8; }
.peach { background: #f9dbbd; }
.green { background: #dbf3c2; }
.blue { background: #c3ddf9; }
.purple { background: #e6d5f7; }
.yellow { background: #fdf8c3; }

.course-tags {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.course {
  font-family: 'Rubik Gemstones', cursive;
  background: black;
  color: white;
  padding: 6px 15px;
  border-radius: 18px;
  font-size: 14px;
}

/* FRIENDS */
.friend-card {
  position: relative;
  display: flex;
  align-items: flex-start;
  background: #fdfde3;
  border: 2px solid black;
  border-radius: 20px;
  padding: 20px;
  gap: 20px;
}

.friend-card .course {
  position: absolute;
  top: 20px;
  right: 20px;
}

.avatar-small {
  width: 70px;
  aspect-ratio: 1 / 1;
  object-fit: cover;
  border-radius: 20px;
}

.peer-info h4 {
  margin: 0;
  font-size: 20px;
}
</style>
