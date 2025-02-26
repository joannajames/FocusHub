<template>
  <div class="container">
    <header class="header">

      <div class="nav-container">
        <img src="/icons/Menu_Burger.png" alt="Menu" class="icon menu-icon" @click="toggleDropdown" />
        <ul v-if="isDropdownOpen" class="dropdown">
          <li><a href="#" @click="navigateTo('/contact_us')">Contact Us</a></li>
        </ul>
      </div>

      <div class="search-bar">
        <img src="/icons/Search_Magnifying_Glass.png" alt="Search" class="icon search-icon" />
        <input type="text" v-model="searchQuery" placeholder="e.g. Boston Public Library (Copley)" class="search-input" />
      </div>

      <img src="/icons/User_Account.png" alt="Account" class="icon account-icon" @click="goToAccount" />
    </header>

    <div class="content-wrapper">
      <aside class="sidebar">
        <img src="/filters/Filter_Shhh.png" alt="Quiet" class="filter shhh-filter"/>
        <img src="/filters/Filter_Wifi.png" alt="WiFi" class="filter wifi-filter"/>
        <img src="/filters/Filter_Charger.png" alt="Outlets" class="filter charger-filter"/>
        <img src="/filters/Filter_Printer.png" alt="Printing" class="filter printer-filter"/>
        <img src="/filters/Filter_OpenLate.png" alt="Late Sesh" class="filter openlate-filter"/>
        <img src="/filters/Filter_WaterBottle.png" alt="H2O Station" class="filter waterbottle-filter"/>
        <img src="/filters/Filter_Proximity.png" alt="Closeby?" class="filter proximity-filter"/>
      </aside>

    <main class="main-content">
      <h1 class="hub-title">The Hub</h1>

      <div class="day-selector">
        <div v-for="(day, index) in days" :key="index" class="day-item">
          <img
            :src="`/icons/Calendar_${day}.png`"
            :alt="day"
            class="icon calendar-icon"
            @click="selectedDay = day"
            :class="{ active: selectedDay === day }"
          />
        </div>
      </div>

        <div class="listings">
          <div v-for="listing in filteredListings" :key="listing.id" class="listing-card">
            <div class="listing-box">
              <div class="listing-image-placeholder"></div>
              <div class="listing-info">
                <h3 class="listing-title">{{ listing.name }}</h3>
                <p class="listing-address">{{ listing.address }} • {{ listing.opening_hours[selectedDay] }}</p>
                <div class="listing-tags">
                  <span v-for="(tag, i) in listing.attributes" :key="i" class="tag" :style="{ backgroundColor: tag.color }">
                    {{ tag.name }}
                  </span>
                </div>
                <div class="listing-rating">
                    <img v-for="star in getStarsArray(listing.rating)" :key="star.id" :src="star.src" :alt="star.alt" class="icon star-icon" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from 'vue';

const isDropdownOpen = ref(false);
const searchQuery = ref('');
const selectedDay = ref('Monday');
const activeFilter = ref(null);

const goToAccount = () => {
  window.location.href = "/account";
};
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};
const navigateTo = (path) => {
  window.location.href = path;
};

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

const listings = ref([
  {
    id: 1,
    name: 'Mugar Memorial Library',
    address: '771 Commonwealth Avenue',
    opening_hours: {
      Monday: '07:00-02:00', Tuesday: '07:00-02:00', Wednesday: '07:00-02:00',
      Thursday: '07:00-02:00', Friday: '07:00-23:00', Saturday: '10:00-23:00',
      Sunday: '10:00-02:00'
    },
    rating: 3.2,
    attributes: [
      {name: 'e-accessible', color: '#badafb'},
      {name: 'printing', color: '#c5f3af'},
      {name: 'prayer space', color: '#ffcdae'}
    ]
  },
  {
    id: 2,
    name: 'BU Faculty of Computing & Data Sciences',
    address: '665 Commonwealth Avenue',
    opening_hours: {
      Monday: '07:00-17:00', Tuesday: '07:00-17:00', Wednesday: '07:00-17:00',
      Thursday: '07:00-17:00', Friday: '07:00-17:00', Saturday: 'Closed',
      Sunday: 'Closed'
    },
    rating: 4.6,
    attributes: [
      {name: 'free', color: '#c5f3af'},
      {name: 'AC', color: '#ffcdae'},
      {name: 'vegan', color: '#ffbbbc'}
    ]
  },
  {
    id: 3,
    name: 'Boston Public Library (Copley)',
    address: '700 Boylston Street',
    opening_hours: {
      Monday: '09:00-20:00', Tuesday: '09:00-20:00', Wednesday: '09:00-20:00',
      Thursday: '09:00-20:00', Friday: '09:00-17:00', Saturday: '09:00-17:00',
      Sunday: '11:00-17:00'
    },
    rating: 4.8,
    attributes: [
      {name: 'e-accessible', color: '#badafb'},
      {name: 'printing', color: '#c5f3af'},
      {name: 'prayer space', color: '#ffcdae'}
    ]
  },
]);

const filteredListings = computed(() => {
  return listings.value.filter(listing =>
      listing.opening_hours[selectedDay.value] &&
      (!activeFilter.value || listing.attributes.some(tag => tag.name === activeFilter.value))
  );
});

const getStarsArray = (rating) => {
  const rounded = Math.round(rating * 2) / 2; // Round to nearest 0.5
  let starsArray = [];

  for (let i = 1; i <= 5; i++) {
    if (i <= Math.floor(rounded)) {
      starsArray.push({ id: i, src: '/icons/Full_Star.png', alt: 'Full Star' });
    } else if (i - 0.5 === rounded) {
      starsArray.push({ id: i, src: '/icons/Half_Star.png', alt: 'Half Star' });
    } else {
      starsArray.push({ id: i, src: '/icons/Star.png', alt: 'Empty Star' });
    }
  }
  return starsArray;
};
</script>

<style scoped>
@import '@fontsource/rubik-doodle-shadow';
@import url('https://fonts.googleapis.com/css2?family=Monofett&display=swap');

@font-face {
  font-family: 'Sansation Light';
  src: url('@/assets/Sansation_Light.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

.container {
  background: #fdfde3;
  padding: 120px;
}

.content-wrapper {
  display: flex;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 90px;
  position: fixed;
  top: 0;
  left: 0;
  background: #fdfde3;
  padding: 32px 2px;
}

.menu-icon {
  width: 250px;
  height: 350px;
}

.dropdown {
  font-family: 'Sansation Light',serif;
  font-size: 20px;
  position: absolute;
  top: 150px;
  right: 0;
  border: 1px solid black;
  background: #fdfde3;
  padding: 10px 45px;
}

.dropdown li {
  padding: 30px 30px;
}

.dropdown li a {
  color: black;
  text-decoration: none;
}

.search-bar {
  width: 1100px;
  height: 35px;
  position: absolute;
  right: 280px;
  top: 57px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px;
  border: 2px solid black;
  border-radius: 25px;
  background: #f9fdad;
}

.search-input {
  font-family: 'Sansation Light',serif;
  font-size: 16px;
  width: 1000px;
  position: absolute;
  right: 80px;
  top: 13px;
  border: none;
  outline: none;
  background: #f9fdad;
}

.search-icon {
  cursor: pointer;
  width: 250px;
  height: 200px;
  position: absolute;
  left: 1100px;
  top: -110px;
}

.account-icon {
  width: 200px;
  height: 150px;
}

.sidebar {
  width: 55px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-right: 10px;
}

.shhh-filter {
  cursor: pointer;
  width: 100px;
  height: 50px;
  position: absolute;
  left: 70px;
  top: 175px;
}

.wifi-filter {
  cursor: pointer;
  width: 80px;
  height: 60px;
  position: absolute;
  left: 75px;
  top: 260px;
}

.charger-filter {
  cursor: pointer;
  width: 100px;
  height: 80px;
  position: absolute;
  left: 65px;
  top: 355px;
}

.printer-filter {
  cursor: pointer;
  width: 95px;
  height: 105px;
  position: absolute;
  left: 65px;
  top: 460px;
}

.openlate-filter {
  cursor: pointer;
  width: 350px;
  height: 270px;
  position: absolute;
  left: -40px;
  top: 435px;
}

.waterbottle-filter {
  cursor: pointer;
  width: 65px;
  height: 130px;
  position: absolute;
  left: 80px;
  top: 690px;
}

.proximity-filter {
  cursor: pointer;
  width: 55px;
  height: 75px;
  position: absolute;
  left: 85px;
  top: 850px;
}

.icon {
  cursor: pointer;
  width: 250px;
  height: 200px;
}

.day-selector {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 15px;
  margin-top: -20px;
}

.day-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
}

.calendar-icon {
  width: 60px;
  height: 60px;
  transition: transform 0.4s ease-in-out;
}

.calendar-icon.active {
  transform: scale(1.4);
  filter: brightness(0.6);
}

.main-content {
  flex-grow: 1;
  margin-left: 40px;
}

.hub-title {
  font-family: 'Rubik Doodle Shadow', cursive;
  font-size: 120px;
  margin-bottom: 5px;
}

.listing-box {
  border: 2px solid black;
  border-radius: 30px;
  margin-bottom: 15px; /* distance between boxes */
  background: #fdfde3;
}

.listing-title {
  font-family: 'Monofett', cursive;
  font-weight: lighter;
  font-size: 38px;
  color: black;
  margin-bottom: 3px;
}

.listing-address {
  font-family: 'Sansation Light', sans-serif;
  font-size: 20px;
  color: black;
  margin-bottom: 20px; /* distance between what follows, i.e. tags */
}

.listing-tags {
  display: flex;
  gap: 8px;
}

.tag {
  font-family: 'Rubik Doodle Shadow', cursive;
  font-size: 14px;
  color: black;
  padding: 5px 10px; /* tag size */
  border: 2px solid black;
  border-radius: 15px;
}

.listing-rating {
  display: flex;
  justify-content: flex-end;
  gap: 2px;
}

.star-icon {
  width: 30px;
  height: 30px;
}
</style>
