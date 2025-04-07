<template>
  <div class="container">
    <header class="header">
      <div class="nav-container">
        <img src="/icons/Menu_Burger.png" alt="Menu" class="icon menu-icon" @click="toggleDropdown" />
        <ul v-if="isDropdownOpen" class="dropdown">
            <li><a href="#" @click="navigateTo('/the_hub')">The Hub</a></li>
            <li><a href="#" @click="navigateTo('/contact_us')">Contact Us</a></li>
            <li><a href="#" @click="navigateTo('/account')">Account</a></li>
        </ul>
      </div>

      <div class="search-bar">
        <input type="text" v-model="searchQuery" placeholder="e.g. Boston Public Library (Copley)" class="search-input" />
        <button class="search-button" @click="searchStudySpots">
            <img src="/icons/Magnifying_Glass.png" alt="Search" class="search-icon" />
        </button>
      </div>

      <div class="account-container">
        <img src="/icons/User_Account.png" alt="Account" style="width: 100px; height: 100px;" @click="goToAccount" />
      </div>
    </header>

    <div class="content-wrapper">
      <aside class="sidebar">
        <div class="filter-item">
          <img src="/filters/Filter_Shhh.png" alt="Quiet" class="filter-icon"/>
        </div>
        <div class="filter-item">
          <img src="/filters/Filter_Wifi.png" alt="WiFi" class="filter-icon"/>
        </div>
        <div class="filter-item">
          <img src="/filters/Filter_Charger.png" alt="Outlets" class="filter-icon"/>
        </div>
        <div class="filter-item">
          <img src="/filters/Filter_Printer.png" alt="Printing" class="filter-icon"/>
        </div>
        <div class="filter-item">
        <img src="/filters/Filter_Clock.png" alt="Late Sesh" class="filter-icon"/>
        </div>

        <div class="filter-item">
          <img src="/filters/Filter_WaterBottle.png" alt="H2O Station" class="filter-icon"/>
        </div>
        <div class="filter-item">
          <img src="/filters/Filter_Proximity.png" alt="Closeby?" class="filter-icon"/>
        </div>
      </aside>

      <main class="main-content">
        <h1 class="hub-title">The Hub</h1>

        <div class="day-selector">
          <div v-for="(day, index) in days" :key="index" class="day-item">
            <img
              :src="`/icons/Calendar_${day}.png`"
              :alt="day"
              style="width: 60px; height: 60px;"
              @click="selectDay(day)"
              :class="{ active: selectedDay === day }"
            />
          </div>
        </div>

        <div class="listings">
          <div v-for="listing in listings" :key="listing.id" class="listing-card">
            <router-link
                :to="{ name: 'reviews', params: { id: listing.id } }"
                class="listing-box"
            >
              <div class="listing-image">
                <img
                    src="/images/library_placeholder.jpg"
                    alt="Library Placeholder"
                    class="listing-image-placeholder"
                />
              </div>
              <div class="listing-info">
                <h3 class="listing-title">{{ listing.name }}</h3>
                <p class="listing-address">{{ listing.address }}</p>
                <div class="listing-rating">
                  <img v-for="star in 5" :key="star" src="/icons/Full_Star.png" alt="Full Star" style="width: 25px; height: 25px;" />
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const isDropdownOpen = ref(false);
const searchQuery = ref('');
const selectedDay = ref('Monday');
const listings = ref([]);

window.listings = listings;

const goToAccount = () => {
  window.location.href = "/account";
};

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const navigateTo = (path) => {
  window.location.href = path;
};

const selectDay = (day) => {
  console.log("Selecting day:", day);
  selectedDay.value = day;
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

const searchStudySpots = async () => {
  try {
    const query = searchQuery.value.trim();

    if (!query) {
      // If search is empty, fall back to all listings
      fetchStudySpots();
      return;
    }

    const response = await fetch(`http://localhost:8000/study_spots/search?q=${encodeURIComponent(query)}`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    listings.value = data.map(spot => ({
      id: spot.id,
      name: spot.name,
      address: spot.address,
      hours: spot.hours,
    }));
  } catch (error) {
    console.error("Error searching study spots:", error);
  }
};


// Fetch data on page load
onMounted(fetchStudySpots);
</script>

<style scoped>
@import '@fontsource/rubik-doodle-shadow';
@import url('https://fonts.googleapis.com/css2?family=Monofett&display=swap');

.container {
  background: #fdfde3;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Header styles */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 150px;
  background: #fdfde3;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.nav-container {
  display: flex;
  align-items: center; /* vertically centers contents */
  height: 100%;         /* ensures full height of the header */
}


.icon {
  width: 220px;
  height: 170px;
  margin-top: 0px;
  cursor: pointer;
}

.menu-icon {
  width: 180px;
  height: 180px;
}


.account-container {
  flex: 0 0 200px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.dropdown {
  position: absolute;
  top: 120px;
  left: 0;
  border: 1px solid #000;
  background: #fdfde3;
  padding: 10px;
  border-radius: 5px;
  list-style: none;
  z-index: 1000;
}

.dropdown li {
  padding: 5px 0;
}

.dropdown a {
  text-decoration: none;
  color: #000;
}

/* Search bar */
.search-bar {
  position: relative;
  width: 700px;
  height: 45px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  border: 2px solid #000;
  border-radius: 25px;
  background: #f9fdad;
  overflow: hidden;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 16px;
  padding: 8px 15px;
}
.search-icon {
  width: 30px;
  height: 30px;
}

.search-button {
  background: #f9fdad;
  border: none;
  border-left: 1px solid #ccc;
  padding: 0 15px;
  height: 100%;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
}

.content-wrapper {
  display: flex;
  flex: 1;
  position: fixed;
  top: 150px;
  bottom: 0;
  left: 0;
  right: 0;
  overflow: hidden;
  padding: 0;
}

/* Sidebar */
.sidebar {
  width: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  gap: 30px;
  overflow-y: auto;
  flex-shrink: 0;
}

.filter-item {
  display: flex;
  justify-content: center;
  align-items: center;
}

.filter-icon {
  width: 90px;
  height: 90px;
  object-fit: contain;
  filter: drop-shadow(2px 2px 3px rgba(0,0,0,0.2));
  transition: transform 0.2s ease;
}

.filter-icon:hover {
  transform: scale(1.1);
  filter: drop-shadow(3px 3px 5px rgba(0,0,0,0.3));
}

.filter-icon.active {
  border: 2px solid #000;
  border-radius: 10px;
  background: rgba(0,0,0,0.05);
}


.main-content {
  flex: 1;
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.hub-title {
  font-family: 'Rubik Doodle Shadow', cursive;
  font-size: 90px;
  text-align: center;
  margin: 5px 0 10px 0;
  font-weight: bold;
  letter-spacing: 2px;
  color: #000;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  text-transform: uppercase;
  line-height: 1;
}

.day-selector {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin: 5px 0 15px 0;
}

.day-item {
  cursor: pointer;
  padding: 2px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.day-item img.active {
  border: 3px solid #000;
  border-radius: 5px;
  background-color: rgba(0,0,0,0.05);
}

/* Listings */
.listings {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  overflow-y: auto;
  padding: 0;
}

.listing-card {
  width: 100%;
}

.listing-box {
  border: 2px solid #000;
  border-radius: 15px;
  padding: 15px;
  background: #fdfde3;
  display: flex;
  gap: 15px;
  position: relative;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  width: auto;
  margin-bottom: 5px;
}

.listing-image {
  flex: 0 0 140px;
}

.listing-image-placeholder {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 10px;
}


.listing-info {
  flex: 1;
  padding: 0 15px;
}

.listing-title {
  font-size: 32px;            /* Slightly larger */
  font-weight: normal;        /* 'bold' is redundant with Monofett's style */
  letter-spacing: 1px;        /* Adds breathing room between letters */
  color: #111;                /* Darker text */
  line-height: 1.2;           /* Better vertical spacing */
  text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.1);
  font-family: 'Monofett', cursive;
  text-transform: none;       /* Remove ALL CAPS if it's hurting readability */
}


.listing-address {
  font-size: 18px;
  color: #666;
  margin: 0 0 8px 0;
}

.listing-rating {
  display: flex;
  gap: 3px;
}

/* Responsive styles */
@media (max-width: 1024px) {
  .search-bar {
    width: 500px;
  }
}

@media (max-width: 768px) {
  .header {
    flex-wrap: wrap;
    height: auto;
    padding: 10px;
  }

  .search-bar {
    order: 3;
    width: 100%;
    margin: 10px 0;
  }

  .content-wrapper {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
  }

  .listing-box {
    flex-direction: column;
  }

  .listing-image {
    align-self: center;
  }

  .listing-info {
    padding-right: 0;
  }
}
</style>