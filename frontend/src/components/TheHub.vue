<template>
  <div class="page-frame">
    <div class="container">
      <header class="header">
        <div class="nav-container">
          <img src="/icons/Menu_Burger.png"
               alt="Menu"
               class="menu-icon"
               @click="toggleDropdown" />
            <ul class="dropdown"
                v-show="showDropdown">
              <li>
                <a href="#"
                   @click="navigateTo('/the_hub')">
                  -&nbsp;&nbsp;&nbsp;the&nbsp;&nbsp;Hub
                  <img src="/icons/Hub_Stars.png"
                       class="dropdown-icon"
                       alt="the Hub Icon" />
                </a>
              </li>
              <li>
                <a href="#" @click="goToProfile">
                  -&nbsp;&nbsp;&nbsp;profile
                  <img src="/icons/Account_Signed_Out.png"
                       class="dropdown-icon"
                       alt="Profile Icon" />
                </a>
              </li>
              <li>
                <a href="#" @click="navigateTo('/chat_to_us')">
                  -&nbsp;&nbsp;&nbsp;chat&nbsp;&nbsp;to&nbsp;&nbsp;us
                  <img src="/icons/Chat_To_Us.png"
                       class="dropdown-icon"
                       alt="Chat to Us Icon" />
                </a>
              </li>
              <li>
                <a href="#" @click="navigateTo('/our_constitution')">
                  -&nbsp;&nbsp;&nbsp;our&nbsp;&nbsp;constitution
                  <img src="/icons/Scroll.png"
                       class="dropdown-icon"
                       alt="Constitution Icon" />
                </a>
              </li>
            </ul>
        </div>
        <div class="nav-section">
          <img :src="isLoggedIn ? '/icons/Account_Logged_In.png' : '/icons/Account_Signed_Out.png'"
               alt="Profile Icon"
               class="login-icon"
               @click="handleProfileClick" />
          <img src="/icons/FocusHub_Logo.png"
               alt="FocusHub Logo"
               class="logo-icon"
               @click="navigateTo('/')" />
          <div class="search-bar">
            <input type="text"
                   v-model="searchQuery"
                   placeholder="e.g. Life Alive Cafe"
                   class="search-input" />
            <img src="/icons/Magnifying_Glass.png"
                 alt="Search"
                 class="search-icon" />
          </div>
        </div>
      </header>

      <!-- Sidebar Filters -->
      <div class="fixed-left-column">
        <aside class="sidebar">
          <div class="tooltip-wrapper"
               v-for="filter in filterOptions"
               :key="filter.key">
            <img :src="filter.icon"
                 :alt="filter.label"
                 class="filter"
                 :class="{ active: activeFilters?.includes(filter.key) }"
                 @click="toggleFilter(filter.key)" />
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
              <img :src="`/icons/Calendar_${day}.png`"
                   :alt="day"
                   class="calendar-icon"
                   @click="selectedDay = day"
                   :class="{ active: selectedDay === day }" />
            </div>
          </div>

          <div class="listing-box" v-for="listing in filteredListings" :key="listing.id">
            <div class="listing-image-wrapper">
              <img :src="'/images/' + listing.default_img" alt="listing image" class="listing-image" />
            </div>
            <div class="listing-content-wrapper">
              <div class="listing-header">
                <p class="listing-title" @click="goToReviews(listing.id)">{{ listing.name }}</p>
                <img :src="favourites.has(listing.id) ? '/icons/Full_Heart.png' : '/icons/Heart.png'"
                     alt="Favourite"
                     class="favourite-icon"
                     @click="toggleFavourite(listing.id)" />
              </div>
              <p class="listing-address">
                {{ listing.address }} • {{ formatOpeningHours(listing, selectedDay) }}
              </p>
              <p class="listing-status" :class="{ open: getOpenStatus(listing, selectedDay) === 'Open Now', closed: getOpenStatus(listing, selectedDay) === 'Closed Now' }">
                {{ getOpenStatus(listing, selectedDay) }}
              </p>
              <div class="listing-footer-wrapper">
                <div class="listing-tags">
                  <span
                      v-for="tag in (listing.tags || []).slice().sort((a, b) => a.localeCompare(b))"
                      :key="tag"
                      class="tag"
                      :class="tagColors[tag]"
                  >
                    {{ tag }}
                  </span>
                </div>
                <div class="listing-rating">
                  <img v-for="(icon, i) in getStarIcons(listing.rating)"
                       :key="i" :src="icon"
                       class="star-icon"
                       alt="rating star" />
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
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import '@/assets/global.css';
import { tagColors } from '@/constants/Tags.js';
import { loginWithGoogle } from '@/services/authService';
import { useAuthStatus } from '@/store/authStatus';
import { auth } from '@/firebase';
import { signOut } from 'firebase/auth';
import { apiFetch } from '@/services/api';

const { isLoggedIn, setLoggedIn } = useAuthStatus();
const router = useRouter();
const goToReviews = (id) => router.push(`/reviews/${id}`);
const goToProfile = () => { showDropdown.value = false; router.push(isLoggedIn.value ? '/profile' : '/unavailable'); };

async function handleProfileClick() {
  if (isLoggedIn.value) {
    await signOut(auth);
    setLoggedIn(false);
    return;
  }

  // 1) Sign in with Google
  await loginWithGoogle();

  setLoggedIn(true);

  // 2) Fetch (and auto-create) the user record
  await apiFetch('/users/me');
  router.push('/');
}
const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const currentDay = ref(new Date().toLocaleDateString('en-US', { weekday: 'long' }));
const selectedDay = ref(currentDay.value);

const secondsToHHMM = (seconds) => {
  const date = new Date(seconds * 1000);
  return date.toISOString().substring(11, 16); // "HH:MM"
};


const navigateTo = (path) => (window.location.href = path);
const showDropdown = ref(false);
const toggleDropdown = () => (showDropdown.value = !showDropdown.value);

const searchQuery = ref('');
const favourites = ref(new Set(JSON.parse(localStorage.getItem('favourites') || '[]')));
const topTagsPerSpot = ref({});

const filterOptions = [
  { key: 'has_outlets', icon: '/filters/Filter_Outlet.png', label: 'Outlets?' },
  { key: 'has_food', icon: '/filters/Filter_Food.png', label: 'Food n Bev?' },
  { key: 'on_campus', icon: '/filters/Filter_Proximity.png', label: 'On Campus?' },
  { key: 'has_printing', icon: '/filters/Filter_Printer.png', label: 'Printing?' },
  { key: 'has_prayer_space', icon: '/filters/Filter_Prayer.png', label: 'Interfaith Room?' },
  { key: 'has_spacious_seating', icon: '/filters/Filter_Capacity.png', label: "Plenty'a Space?" },
  { key: 'has_meeting_rooms', icon: '/filters/Filter_Meeting.png', label: 'Meetings?' },
];
const activeFilters = ref([]);

const toggleFilter = (filterKey) => {
  const index = activeFilters.value.indexOf(filterKey);
  index > -1 ? activeFilters.value.splice(index, 1) : activeFilters.value.push(filterKey);
};

const toggleFavourite = (id) => {
  favourites.value.has(id) ? favourites.value.delete(id) : favourites.value.add(id);
  localStorage.setItem('favourites', JSON.stringify([...favourites.value]));
};

function formatOpeningHours(listing, selectedDay) {
  const hours = listing.hours?.[selectedDay];
  if (!hours || !hours.opens || !hours.closes) return 'Hours not available';

  const formatTime = (hhmm) => {
    if (!hhmm || typeof hhmm !== 'string' || !hhmm.includes(':')) return 'Hours not available';
    const [hourString, minuteString] = hhmm.split(':');
    const hour = parseInt(hourString, 10);
    const minute = parseInt(minuteString, 10);
    if (isNaN(hour) || isNaN(minute)) return 'Hours not available';
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const adjustedHour = hour % 12 === 0 ? 12 : hour % 12;
    return `${adjustedHour}:${minute.toString().padStart(2, '0')} ${ampm}`;
  };

  if (hours.opens === 'Closed' || hours.closes === 'Closed') {
    return 'Hours not available';
  }

  const [openHour, openMinute] = hours.opens.split(':').map(Number);
  const [closeHour, closeMinute] = hours.closes.split(':').map(Number);

  if (isNaN(openHour) || isNaN(closeHour) || isNaN(openMinute) || isNaN(closeMinute)) {
    return 'Hours not available';
  }

  const openTotalMinutes = openHour * 60 + openMinute;
  const closeTotalMinutes = closeHour * 60 + closeMinute;

  const openFormatted = formatTime(hours.opens);
  const closeFormatted = formatTime(hours.closes);

  if (closeTotalMinutes < openTotalMinutes) {
    return `${openFormatted} - ${closeFormatted}`;
  } else {
    return `${openFormatted} - ${closeFormatted}`;
  }
}


function getOpenStatus(listing, selectedDay) {
  const todayHours = listing.hours?.[selectedDay];
  if (!todayHours || !todayHours.opens || !todayHours.closes) {
    return 'Closed Now';
  }

  const now = new Date();
  const currentMinutes = now.getHours() * 60 + now.getMinutes();

  const [openHour, openMinute] = todayHours.opens.split(':').map(Number);
  const [closeHour, closeMinute] = todayHours.closes.split(':').map(Number);

  if (isNaN(openHour) || isNaN(openMinute) || isNaN(closeHour) || isNaN(closeMinute)) {
    return 'Closed Now';
  }

  const openTotalMinutes = openHour * 60 + openMinute;
  const closeTotalMinutes = closeHour * 60 + closeMinute;

  if (closeTotalMinutes < openTotalMinutes) {
    // Spot closes after midnight
    if (currentMinutes >= openTotalMinutes || currentMinutes <= closeTotalMinutes) {
      return 'Open Now';
    } else {
      return 'Closed Now';
    }
  } else {
    // Normal same-day closing
    if (currentMinutes >= openTotalMinutes && currentMinutes <= closeTotalMinutes) {
      return 'Open Now';
    } else {
      return 'Closed Now';
    }
  }
}

onMounted(async () => {
  try {
    const spotsData = await apiFetch(`/study_spots?weekday=${selectedDay.value}`);

    const spotMap = {};

    for (const row of spotsData.data) {
      const spot_id = row.spot_id;

      if (!spotMap[spot_id]) {
        spotMap[spot_id] = {
          id: spot_id,
          name: row.spot_name,
          address: row.address,
          default_img: row.default_img,
          rating: parseFloat(row.avg_rating) || 0,
          has_outlets: row.has_outlets === 1 || row.has_outlets === "Yes",
          has_food: row.has_food === 1 || row.has_food === "Yes",
          has_printing: row.has_printing === 1 || row.has_printing === "Yes",
          has_prayer_space: row.has_prayer_space === 1 || row.has_prayer_space === "Yes",
          has_spacious_seating: row.has_spacious_seating === 1 || row.has_spacious_seating === "Yes",
          has_meeting_rooms: row.has_meeting_rooms === 1 || row.has_meeting_rooms === "Yes",
          on_campus: row.on_campus === 1 || row.on_campus === "Yes",
          hours: {}
        };
      }

      // Add each day's hours
      if (row.day !== null && row.open_time  && row.close_time) {
        spotMap[spot_id].hours[row.day] = {
            opens: secondsToHHMM(row.open_time),
            closes: secondsToHHMM(row.close_time),
        };
      }
    }

    allListings.value = Object.values(spotMap);

    const topTagsData = await apiFetch('/study_spots/top_tags');
    topTagsPerSpot.value = topTagsData.data;

    allListings.value = allListings.value.map(listing => ({
      ...listing,
      tags: topTagsPerSpot.value[listing.id] || []
    }));

  } catch (err) {
    console.error("Data fetch failed:", err);
  }
});

const allListings = ref([]);
const filteredListings = computed(() => {
  return allListings.value
    .filter((spot) => {
      const dayHours = spot.hours[selectedDay.value];
      return dayHours && dayHours.opens !== '00:00:00' && dayHours.closes !== '00:00:00';
    })
    .filter((listing) => {
      const nameMatches = listing.name?.toLowerCase().includes(searchQuery.value.toLowerCase());
      const filterMatches =
        activeFilters.value.length === 0 ||
        activeFilters.value.every((filter) => listing[filter]);
      return nameMatches && filterMatches;
    });
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

.listing-status {
  margin: 5px 25px;
  font-size: 16px;
  font-family: 'Sansation Light', serif;
}

.listing-status.open {
  color: green;
  font-weight: bold;
}

.listing-status.closed {
  color: red;
  font-weight: bold;
}

.star-icon {
  object-fit: contain;
  width: 35px;
  height: 35px;
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