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
                <p class="listing-address">{{ listing.address }} • {{ listing.hours }}</p>
                <div class="listing-rating">
                  <img v-for="star in 5" :key="star" src="/icons/Full_Star.png" alt="Full Star" class="icon star-icon" />
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
import { ref, computed, onMounted } from "vue";

const isDropdownOpen = ref(false);
const searchQuery = ref('');
const selectedDay = ref('Monday');
const listings = ref([]);

window.listings=listings;

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

// Fetch study spots from FastAPI backend
const fetchStudySpots = async () => {
  try {
    console.log("Fetching study spots...");
    const response = await fetch("http://localhost:8000/study_spots");

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Fetched Data:", data);

    // Update listings with API data
    listings.value = data.map(spot => ({
      id: spot.id,
      name: spot.name,
      address: spot.address,
      hours: spot.hours,
    }));
  } catch (error) {
    console.error("Error fetching study spots:", error);
  }
};

// Fetch data on page load
onMounted(fetchStudySpots);

// Ensure listings are displayed correctly
const filteredListings = computed(() => listings.value);
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

img {
  object-fit: contain; /* ✅ Prevent distortion */
  display: block;
}

.container {
  background: #fdfde3;
  padding: 120px;
}

.content-wrapper {
  display: flex;
}

.main-content {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  align-items: center;  /* ✅ Center listings */
  overflow: hidden;  /* ✅ Prevent unwanted scrolling */
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



.dropdown {
  font-family: 'Sansation Light', serif;
  font-size: 20px;
  position: absolute;
  top: 150px;
  right: 0;
  border: 1px solid black;
  background: #fdfde3;
  padding: 10px 45px;
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

.listings {
  display: flex;
  flex-direction: column;
  gap: 25px;
  max-height: calc(100vh - 150px); /* ✅ Use available space */
  overflow-y: auto;
  width: 80%; /* ✅ Make it take up more space */
  align-items: center;
}


.listing-box {
  border: 2px solid black;
  border-radius: 25px;
  padding: 35px; /* ✅ More padding inside */
  background: #fdfde3;
  width: 90%;
  max-width: 900px; /* ✅ Wider for readability */
  min-height: 220px; /* ✅ More vertical space */
  font-size: 22px; /* ✅ Increase font size for readability */
  display: flex;
  flex-direction: column; /* ✅ Stack elements inside */
  align-items: flex-start; /* ✅ Align content to left */
  justify-content: space-between;
  box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2);
}


.listing-title {
  font-family: 'Monofett', cursive;
  font-size: 28px; /* ✅ Bigger title */
  font-weight: bold;
  color: black;
  margin-bottom: 8px;
}

.listing-address {
  font-family: 'Sansation Light', sans-serif;
  font-size: 20px; /* ✅ More readable */
  color: black;
  margin-bottom: 15px;
}



.listing-rating {
  display: flex;
  justify-content: flex-start; /* ✅ Align stars to the left */
  gap: 3px; /* ✅ Reduce spacing between stars */
}

.sidebar {
  width: 180px; /* ✅ Make sidebar wider */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 35px; /* ✅ More space between icons */
}

.search-bar {
  width: 80%; /* ✅ Matches sidebar width */
  height: 60px; /* ✅ Taller for visibility */
  border: 3px solid black;
  border-radius: 30px;
  background: #f9fdad;
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
}

.search-input {
  font-size: 22px; /* ✅ Bigger text for easier typing */
  width: 100%;
  border: none;
  outline: none;
  background: #f9fdad;
}



.icon {
  width: auto; /* ✅ Prevent forced scaling */
  height: auto;
  max-width: 100px; /* ✅ Set a reasonable max size */
  max-height: 100px;
}

.menu-icon {
  width: 50px;
  height: 50px;
}

.star-icon {
  width: 20px; /* ✅ Reduce star size */
  height: 20px;
}


.search-icon {
  width: 25px;
  height: 25px;
}

.account-icon {
  width: 250px;
  height: 250px;
}

.star-icon {
  width: 20px;
  height: 20px;
}

.shhh-filter,
.wifi-filter,
.charger-filter,
.printer-filter,
.openlate-filter,
.waterbottle-filter,
.proximity-filter {
  width: 80px; /* ✅ Bigger icons */
  height: 80px;
}


.calendar-icon {
  width: 60px;
  height: 60px;
}


.day-selector {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 40px;  /* ✅ Increase margin to push down */
}


</style>
