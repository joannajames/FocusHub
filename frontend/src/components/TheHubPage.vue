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
          <li><a @click="navigateTo('/the_hub')">The Hub</a></li>
          <li><a @click="navigateTo('/contact_us')">Contact Us</a></li>
          <li><a @click="navigateTo('/account')">Account</a></li>
        </ul>
      </div>
      <img
        src="/icons/FocushubLogo.png"
        alt="FocusHub Logo"
        class="logo-icon"
        @click="navigateTo('/')"
      />
    </header>

    <!-- Search Bar -->
    <div class="search-bar">
      <img src="/icons/Magnifying_Glass.png" alt="Search" class="search-icon" />
      <input
        type="text"
        v-model="searchQuery"
        placeholder="e.g. Boston Public Library (Copley)"
        class="search-input"
      />
    </div>

    <!-- Content -->
    <div class="content-wrapper">
      <!-- Sidebar -->
      <aside class="sidebar">
        <img src="/filters/Filter_Shhh.png" alt="Quiet" class="filter" />
        <img src="/filters/Filter_Wifi.png" alt="WiFi" class="filter" />
        <img src="/filters/Filter_Charger.png" alt="Outlets" class="filter" />
        <img src="/filters/Filter_Printer.png" alt="Printing" class="filter" />
        <img src="/filters/Filter_Clock.png" alt="Late Sesh" class="filter" />
        <img src="/filters/Filter_WaterBottle.png" alt="H2O Station" class="filter" />
        <img src="/filters/Filter_Proximity.png" alt="Closeby?" class="filter" />
      </aside>

      <!-- Main -->
      <main class="main-content">
        <h1 class="hub-title">The Hub</h1>

        <!-- Day Selector -->
        <div class="day-selector">
          <div v-for="(day, index) in days" :key="index" class="day-item">
            <img
              :src="`/icons/Calendar_${day}.png`"
              :alt="day"
              class="calendar-icon"
              @click="selectedDay = day"
              :class="{ active: selectedDay === day }"
            />
          </div>
        </div>

        <!-- Listings -->
        <div class="listings">
          <div v-for="listing in filteredListings" :key="listing.id" class="listing-box">
            <div class="listing-info">
              <h3 class="listing-title">{{ listing.name }}</h3>
              <p class="listing-address">
                {{ listing.address }} • {{ listing.opening_hours[selectedDay] }}
              </p>
              <div class="listing-tags">
                <span v-for="(tag, i) in listing.attributes" :key="i" class="tag" :style="{ backgroundColor: tag.color }">
                  {{ tag.name }}
                </span>
              </div>
              <div class="listing-rating">
                <img
                  v-for="star in getStarsArray(listing.rating)"
                  :key="star.id"
                  :src="star.src"
                  :alt="star.alt"
                  class="star-icon"
                />
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const searchQuery = ref('');
const selectedDay = ref('Monday');
const activeFilter = ref(null);

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
      { name: 'e-accessible', color: '#badafb' },
      { name: 'printing', color: '#c5f3af' },
      { name: 'prayer space', color: '#ffcdae' }
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
      { name: 'free', color: '#c5f3af' },
      { name: 'AC', color: '#ffcdae' },
      { name: 'vegan', color: '#ffbbbc' }
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
      { name: 'e-accessible', color: '#badafb' },
      { name: 'printing', color: '#c5f3af' },
      { name: 'prayer space', color: '#ffcdae' }
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
  const rounded = Math.round(rating * 2) / 2;
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
/* Header + Branding */
@font-face {
  font-family: 'Sansation Light';
  src: url('@/assets/Sansation_Light.ttf') format('truetype');
}

@import '@fontsource/rubik-doodle-shadow';

.menu-icon {
  width: auto;
  height: auto;
  margin-top: 10px;
}

.container {
  background: #fdfde3;
  padding: 180px 60px 40px;
  font-family: 'Sansation Light', sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background: #fdfde3;
  padding: 30px 40px;
  height: 80px;
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

.search-bar {
  position: absolute;
  right: 280px;
  top: 57px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 15px;
  border: 2px solid black;
  border-radius: 25px;
  background: #f9fdad;
}

.search-input {
  background: #f9fdad;
  border: none;
  outline: none;
  font-family: 'Sansation Light';
  font-size: 16px;
  width: 400px;
}

.search-icon {
  width: 40px;
  height: 40px;
}

.content-wrapper {
  display: flex;
  margin-top: 100px;
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-right: 20px;
}

.filter {
  width: 60px;
  height: auto;
  cursor: pointer;
}

.main-content {
  flex-grow: 1;
}

.hub-title {
  font-family: 'Rubik Doodle Shadow', cursive;
  font-size: 100px;
  margin-bottom: 20px;
}

.day-selector {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-bottom: 30px;
}

.calendar-icon {
  width: 60px;
  height: 60px;
  transition: transform 0.4s;
}

.calendar-icon.active {
  transform: scale(1.4);
  filter: brightness(0.6);
}

.listing-box {
  border: 2px solid black;
  border-radius: 30px;
  margin-bottom: 20px;
  background: #fdfde3;
  padding: 20px;
}

.listing-title {
  font-family: 'Monofett', cursive;
  font-size: 32px;
  margin-bottom: 10px;
}

.listing-address {
  font-size: 18px;
  margin-bottom: 12px;
}

.listing-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
}

.tag {
  font-family: 'Rubik Doodle Shadow', cursive;
  font-size: 14px;
  border: 2px solid black;
  border-radius: 15px;
  padding: 4px 10px;
}

.listing-rating {
  display: flex;
  justify-content: flex-end;
  gap: 4px;
}

.star-icon {
  width: 24px;
  height: 24px;
}
</style>
