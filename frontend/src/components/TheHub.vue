<template>
  <div class="page-frame">
    <div class="container">
      <!-- Header Section -->
      <header class="header">
        <div class="nav-container">
          <img src="/icons/Menu_Burger.png" alt="Menu" class="menu-icon" @click="toggleDropdown" />
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
          <img :src="isLoggedIn ? '/icons/Account_Logged_In.png' : '/icons/Account_Signed_Out.png'" alt="Profile Icon" class="login-icon" @click="handleProfileClick" />
          <img src="/icons/FocusHub_Logo.png" alt="FocusHub Logo" class="logo-icon" @click="navigateTo('/')" />
          <div class="search-bar">
            <input type="text" v-model="searchQuery" placeholder="e.g. Life Alive Cafe" class="search-input" />
            <img src="/icons/Magnifying_Glass.png" alt="Search" class="search-icon" />
          </div>
        </div>
      </header>

      <!-- Sidebar Filters -->
      <div class="fixed-left-column">
        <aside class="sidebar">
          <div class="tooltip-wrapper" v-for="filter in filterOptions" :key="filter.key">
            <img :src="filter.icon" :alt="filter.label" class="filter" :class="{ active: activeFilters.includes(filter.key) }" @click="toggleFilter(filter.key)" />
            <span class="custom-tooltip">{{ filter.label }}</span>
          </div>
        </aside>
      </div>

      <!-- Main Content -->
      <div class="left-margin">
        <main class="main-content">
          <h1 class="title">the Hub</h1>
          <div class="day-selector">
            <div v-for="(day, index) in days" :key="index" class="day-item">
              <img :src="`/icons/Calendar_${day}.png`" :alt="day" class="calendar-icon" @click="selectedDay = day" :class="{ active: selectedDay === day }" />
            </div>
          </div>

          <div class="listing-box" v-for="listing in filteredListings" :key="listing.id">
            <div class="listing-image-wrapper">
              <img :src="`/images/${listing.default_img_url}`" alt="listing image" class="listing-image" />
            </div>
            <div class="listing-content-wrapper">
              <div class="listing-header">
                <p class="listing-title" @click="goToReviews(listing.id)">{{ listing.name }}</p>
                <img :src="favourites.has(listing.id) ? '/icons/Full_Heart.png' : '/icons/Heart.png'" alt="Favourite" class="favourite-icon" @click="toggleFavourite(listing.id)" />
              </div>
              <p class="listing-address">{{ listing.address }} • {{ listing.opening_hours }}</p>
              <div class="listing-footer-wrapper">
                <div class="listing-tags">
                  <span class="tag pink">courtyard</span>
                  <span class="tag blue">student dealz</span>
                  <span class="tag orange">quiet</span>
                  <span class="tag green">car parking</span>
                </div>
                <div class="listing-rating">
                  <img v-for="(icon, i) in getStarIcons(listing.rating)" :key="i" :src="icon" class="star-icon" alt="rating star" />
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed, watch} from 'vue';
import { useRouter } from 'vue-router';
import '@/assets/global.css';
import { allListings } from '@/store/favourites';
import { loginWithGoogle } from '@/services/authService';
import { useAuthStatus } from '@/store/authStatus';
import { auth } from '@/firebase';
import { signOut } from 'firebase/auth';

const filteredListings = computed(() => {
  return listings.value.filter((listing) => {
    const nameMatches = listing.name?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const filterMatches =
      activeFilters.value.length === 0 ||
      activeFilters.value.every((filter) => listing[filter] !== undefined && listing[filter]);

    return nameMatches && filterMatches;
  });
});

const { isLoggedIn, setLoggedIn } = useAuthStatus();
const listings = ref([]);
const showDropdown = ref(false);
const toggleDropdown = () => (showDropdown.value = !showDropdown.value);
const navigateTo = (path) => (window.location.href = path);
const searchQuery = ref('');
const selectedDay = ref(new Date().toLocaleDateString('en-US', { weekday: 'long' }));
const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const favourites = ref(new Set(JSON.parse(localStorage.getItem('favourites') || '[]')));
const activeFilters = ref([]);
const router = useRouter();

const filterOptions = [
  { key: 'has_outlets', icon: '/filters/Filter_Outlet.png', label: 'Outlets?' },
  { key: 'has_food', icon: '/filters/Filter_Food.png', label: 'Food n Bev?' },
  { key: 'on_campus', icon: '/filters/Filter_Proximity.png', label: 'On Campus?' },
  { key: 'has_printing', icon: '/filters/Filter_Printer.png', label: 'Printing?' },
  { key: 'has_prayer_space', icon: '/filters/Filter_Prayer.png', label: 'Interfaith Room?' },
  { key: 'has_spacious_seating', icon: '/filters/Filter_Capacity.png', label: "Plenty'a Space?" },
  { key: 'has_meeting_rooms', icon: '/filters/Filter_Meeting.png', label: 'Meetings?' },
];

const goToReviews = (id) => router.push(`/reviews/${id}`);
const goToProfile = () => { showDropdown.value = false; router.push(isLoggedIn.value ? '/profile' : '/unavailable'); };
const toggleFilter = (filterKey) => {
  const index = activeFilters.value.indexOf(filterKey);
  index > -1 ? activeFilters.value.splice(index, 1) : activeFilters.value.push(filterKey);
};
const toggleFavourite = (id) => {
  favourites.value.has(id) ? favourites.value.delete(id) : favourites.value.add(id);
  localStorage.setItem('favourites', JSON.stringify([...favourites.value]));
};

const weekdayToIndex = { Sunday: 0, Monday: 1, Tuesday: 2, Wednesday: 3, Thursday: 4, Friday: 5, Saturday: 6 };

const dayChanged = computed(() => selectedDay.value);
const fetchStudySpots = () => {
  const dayIndex = weekdayToIndex[selectedDay.value];
  console.log(`Fetching spots for day: ${selectedDay.value} (index: ${dayIndex})`);
  listings.value = [];
  fetch(`http://127.0.0.1:8090/study_spots/day/${dayIndex}`)
    .then(res => {
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
      return res.json();
    })
    .then(rawData => {
      console.log('API Response:', rawData);

      if (!rawData.data || !Array.isArray(rawData.data) || rawData.data.length === 0) {
        console.warn('No study spots data returned or empty array');
        return;
      }

      const mapped = rawData.data.map((spot) => {
        console.log('Raw spot data:', spot);

        let imgUrl = 'default.jpg';
        if (spot.default_img_url) imgUrl = spot.default_img_url;
        else if (spot.default_img) imgUrl = spot.default_img;

        let rating = 0;
        if (spot.average_rating) rating = parseFloat(spot.average_rating);
        else if (spot.avg_rating) rating = parseFloat(spot.avg_rating);

        let hours = 'Hours unavailable';
        if (spot.open_time && spot.close_time) {
          let openTime = String(spot.open_time).slice(0, 5);
          let closeTime = String(spot.close_time).slice(0, 5);
          hours = `${openTime}–${closeTime}`;
        }

        return {
          id: spot.spot_id,
          name: spot.spot_name,
          address: spot.address || 'Address unavailable',
          rating: rating,
          default_img_url: imgUrl,
          opening_hours: hours,
          has_outlets: spot.has_outlets === 'Yes',
          has_food: spot.has_food === 'Yes',
          has_printing: spot.has_printing === 'Yes',
          has_prayer_space: spot.has_prayer_space === 'Yes',
          has_spacious_seating: spot.has_spacious_seating === 'Yes',
          has_meeting_rooms: spot.has_meeting_rooms === 'Yes',
          on_campus: spot.on_campus === 'Yes',
        };
      });

      console.log(`Successfully mapped ${mapped.length} listings:`, mapped);
      listings.value = mapped;
      allListings.value = mapped;
    })
    .catch(err => {
      console.error('Error fetching study spots:', err);
    });
};

watch(dayChanged, () => {
  fetchStudySpots();
});

onMounted(() => {
  fetchStudySpots();
});

const getStarIcons = (rating) => {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5;
  const empty = 5 - full - (half ? 1 : 0);
  return [
    ...Array(full).fill('/icons/Full_Star.png'),
    ...(half ? ['/icons/Half_Star.png'] : []),
    ...Array(empty).fill('/icons/Star.png')
  ];
};

function handleProfileClick() {
  isLoggedIn.value ? signOut(auth).then(() => setLoggedIn(false)) : loginWithGoogle().then(() => setLoggedIn(true));
}
</script>

<style>

.search-bar {
  display: flex;
  position: absolute;
  align-items: center;
  width: 55%;
  min-width: 0;
  top: 40px;
  left: 53%;
  gap: 10px;
  padding: 5px 10px;
  transform: translateX(-50%);
  background: #f9fdad;
  border: 2px solid black;
  border-radius: 128px;
}

.search-input {
  align-items: center;
  width: 900px;
  height: 25px;
  padding: 0 20px;
  margin-bottom: 5px;
  font-family: 'Sansation Light', serif;
  font-size: 18px;
  font-style: italic;
  background: #f9fdad;
  outline: none;
  border: none;
  border-radius: 124px;
}

.search-icon {
  width: 40px;
  height: 40px;
}

.sidebar {
  display: flex;
  flex-direction: column;
}

.tooltip-wrapper {
  position: relative;
  display: inline-block;
}

.custom-tooltip {
  position: absolute;
  text-align: center;
  visibility: hidden;
  padding: 6px 6px;
  font-family: 'Sansation Light', serif;
  font-size: 13px;
  color: black;
  background-color: #fdfde3;
  border: 1px solid black;
  border-radius: 12px;
  bottom: 45%;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.1s ease;
  pointer-events: none;
}

.tooltip-wrapper:hover .custom-tooltip {
  visibility: visible;
  opacity: 1;
}

.fixed-left-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: fixed;
  top: 170px; /* just below header */
  left: 60px;
  gap: 25px;
}

.filter {
  width: 78px;
  height: 78px;
  object-fit: contain;
  cursor: pointer;
  margin-bottom: 15px;
}

.filter.active {
  padding: 5px;
  transform: scale(1.03);
  filter: brightness(1.2) contrast(1.2);
  border: 1.5px solid black;
  border-radius: 20px;
}

.day-selector {
  display: flex;
  justify-content: flex-end;
  gap: 5px;
  margin-top: -80px;
  margin-right: 30px;
}

.calendar-icon {
  width: 80px;
  height: 80px;
  transition: transform 0.4s;
  cursor: pointer;
}

.calendar-icon.active {
  transform: scale(1.3);
  filter: brightness(0.6);
}

.listing-box {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding: 20px;
  margin: 20px 0;
  background: #fdfde3;
  border: 1.5px solid black;
  border-radius: 30px;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.listing-image-wrapper {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  justify-content: center;
}

.listing-image {
  width: auto;
  height: 135px;
  object-fit: cover;
  border: 1px solid black;
  border-radius: 20px;
}

.listing-content-wrapper {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: flex-start;
}

.listing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  line-height: 10%;
}

.listing-title {
  margin: 15px 25px;
  font-family: 'Rubik One', serif;
  font-size: 27px;
  cursor: pointer;
}

.listing-address {
  margin: 6px 25px;
  font-size: 18px;
  font-family: 'Sansation Light', serif;
  letter-spacing: 1px;
}

.listing-tags {
  display: flex;
  flex-shrink: 0;
  width: fit-content;
  margin: 5px 22px;
  gap: 7px;
}

.listing-rating {
  display: flex;
  flex-shrink: 0;
  width: fit-content;
  margin-right: -5px;
}

.listing-footer-wrapper{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-top: 10px;
}

.star-icon {
  object-fit: contain;
  width: 45px;
  height: 45px;
  padding: 0;
  margin: 0 2px;
  cursor: auto;
}

.favourite-icon {
  display: flex;
  justify-content: flex-end;
  width: 40px;
  height: auto;
  margin-top: -2.5px;
  cursor: pointer;
}

.tag{
  cursor: auto;
}

</style>
