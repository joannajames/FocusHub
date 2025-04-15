<template>
  <div class="page-frame">
    <div class="container">
      <header class="header">
        <div class="nav-container">
          <img src="/icons/Menu_Burger.png"
               alt="Menu"
               class="menu-icon"
               @click="toggleDropdown" />
          <ul class="dropdown" v-show="showDropdown">
            <li>
              <a href="#" @click="navigateTo('/the_hub')">
                -&nbsp;&nbsp;&nbsp;the&nbsp;&nbsp;Hub
                <img
                    src="/icons/Hub_Stars.png"
                    class="dropdown-icon"
                    alt="the Hub Icon"/>
              </a>
            </li>
            <li>
              <a href="#" @click="navigateTo('/profile')">
                -&nbsp;&nbsp;&nbsp;profile
                <img
                    src="/icons/Account.png"
                    alt="Profile"
                    class="dropdown-icon"
                />
              </a>
            </li>
            <li>
              <a href="#" @click="navigateTo('/chat_to_us')">
                -&nbsp;&nbsp;&nbsp;chat&nbsp;&nbsp;to&nbsp;&nbsp;us
                <img
                    src="/icons/Chat_To_Us.png"
                    alt="Chat"
                    class="dropdown-icon"
                />
              </a>
            </li>
            <li>
              <a href="#" @click="navigateTo('/our_constitution')">
                -&nbsp;&nbsp;&nbsp;our&nbsp;&nbsp;constitution
                <img src="/icons/Scroll.png"
                     alt="Constitution"
                     class="dropdown-icon"
                />
              </a>
            </li>
          </ul>
        </div>
        <div class="nav-section">
          <img src="/icons/Account.png"
               alt="Profile Icon"
               class="login-icon"
               @click="navigateTo('/profile')" />
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

      <div class="fixed-left-column">
        <aside class="sidebar">
          <div class="tooltip-wrapper">
            <img src="/filters/Filter_Outlet.png"
                alt="Outlets"
                class="filter"
                :class="{ active: activeFilters.includes('has_outlets') }"
                @click="toggleFilter('has_outlets')"
            />
            <span class="custom-tooltip">Outlets?</span>
          </div>
          <div class="tooltip-wrapper">
            <img src="/filters/Filter_Food.png"
               alt="Food n Bev"
               class="filter"
               :class="{ active: activeFilters.includes('has_food') }"
               @click="toggleFilter('has_food')"
            />
            <span class="custom-tooltip">Food n Bev?</span>
          </div>
          <div class="tooltip-wrapper">
            <img src="/filters/Filter_Proximity.png"
               alt="On-Campus?"
               class="filter"
               :class="{ active: activeFilters.includes('on_campus') }"
               @click="toggleFilter('on_campus')"
            />
            <span class="custom-tooltip">On Campus?</span>
          </div>
          <div class="tooltip-wrapper">
            <img src="/filters/Filter_Printer.png"
               alt="Printing"
               class="filter"
               :class="{ active: activeFilters.includes('has_printing') }"
               @click="toggleFilter('has_printing')"
            />
            <span class="custom-tooltip">Printing?</span>
          </div>
          <div class="tooltip-wrapper">
            <img src="/filters/Filter_Prayer.png"
               alt="Prayer"
               class="filter"
               :class="{ active: activeFilters.includes('has_prayer_space') }"
               @click="toggleFilter('has_prayer_space')"
            />
            <span class="custom-tooltip">Interfaith Room?</span>
          </div>
          <div class="tooltip-wrapper">
            <img src="/filters/Filter_Capacity.png"
               alt="Plenty'a Space"
               class="filter"
               :class="{ active: activeFilters.includes('has_spacious_seating') }"
               @click="toggleFilter('has_spacious_seating')"
            />
            <span class="custom-tooltip">Plenty'a Space?</span>
          </div>
          <div class="tooltip-wrapper">
            <img src="/filters/Filter_Meeting.png"
               alt="Meetings"
               class="filter"
               :class="{ active: activeFilters.includes('has_meeting_rooms') }"
               @click="toggleFilter('has_meeting_rooms')"
            />
            <span class="custom-tooltip">Meetings?</span>
          </div>
        </aside>
      </div>

      <div class="left-margin">
        <main class="main-content">
          <h1 class="title">the Hub</h1>
          <div class="day-selector">
            <div v-for="(day, index) in days" :key="index" class="day-item">
              <img :src="`/icons/Calendar_${day}.png`"
                   :alt="day" class="calendar-icon"
                   @click="selectedDay = day"
                   :class="{ active: selectedDay === day }" />
            </div>
          </div>

          <div class="listing-box" v-for="listing in filteredListings" :key="listing.id">
            <div class="listing-image-wrapper">
              <img :src="`/images/${listing.default_img_url}`"
                   :alt="listing.image"
                    class="listing-image" />
            </div>
              <div class="listing-content-wrapper">
                <div class="listing-header">
                  <p class="listing-title" @click="goToReviews(listing.id)">
                    {{ listing.name }}
                  </p>
                  <img
                    :src="favourites.has(listing.id) ? '/icons/Full_Heart.png' : '/icons/Heart.png'"
                    alt="Favourite"
                    class="favourite-icon"
                    @click="toggleFavourite(listing.id)"
                  />
                </div>
                <p class="listing-address">{{ listing.address }} • {{ listing.opening_hours[selectedDay] }}</p>
                <div class="listing-footer-wrapper">
                  <div class="listing-tags">
                    <span class="tag pink">courtyard</span>
                    <span class="tag blue">student dealz</span>
                    <span class="tag orange">quiet</span>
                    <span class="tag green">car parking</span>
                  </div>
                  <div class="listing-rating">
                    <img v-for="(i) in getStarIcons(listing.rating)"
                       :key="i"
                       src="/icons/Star.png"
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

import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import '@/assets/global.css';
import {allListings} from "@/store/favourites";
const listings = ref([]);
const showDropdown = ref(false);
const toggleDropdown = () => (showDropdown.value = !showDropdown.value);
const navigateTo = (path) => (window.location.href = path);
const searchQuery = ref('');
const selectedDay = ref(new Date().toLocaleDateString('en-US', { weekday: 'long' }));
const favourites = ref(new Set(JSON.parse(localStorage.getItem('favourites') || '[]')));
const activeFilters = ref([]);
const router = useRouter();
const goToReviews = (id) => {
  router.push(`/reviews/${id}`);
};

const toggleFilter = (filterKey) => {
  const index = activeFilters.value.indexOf(filterKey);
  if (index > -1) {
    activeFilters.value.splice(index, 1);
  } else {
    activeFilters.value.push(filterKey);
  }
};

const filteredListings = computed(() => {
  return listings.value.filter((listing) => {
    const nameMatches = listing.name?.toLowerCase().includes(searchQuery.value.toLowerCase());
    const filterMatches =
      activeFilters.value.length === 0 ||
      activeFilters.value.every((filter) => listing[filter] === 'Yes');
    return nameMatches && filterMatches;
  });
});

const toggleFavourite = (id) => {
  if (favourites.value.has(id)) {
    favourites.value.delete(id);
  } else {
    favourites.value.add(id);
  }
  localStorage.setItem('favourites', JSON.stringify([...favourites.value]));
};

const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/spots');
    const rawData = await res.json();
    const mapped = rawData.map((spot) => ({
      id: spot.spot_id,
      name: spot.spot_name,
      address: spot.address,
      rating: parseFloat(spot.average_rating) || 0,
      default_img_url: spot.default_img_url,
      opening_hours: {
        Monday: '07:00–20:00',
        Tuesday: '07:00–20:00',
        Wednesday: '07:00–20:00',
        Thursday: '07:00–20:00',
        Friday: '07:00–17:00',
        Saturday: '10:00–16:00',
        Sunday: '10:00–16:00',
      },
      has_outlets: spot.has_outlets,
      has_food: spot.has_food,
      has_printing: spot.has_printing,
      has_prayer_space: spot.has_prayer_space,
      has_spacious_seating: spot.has_spacious_seating,
      has_meeting_rooms: spot.has_meeting_rooms,
      on_campus: spot.on_campus,
    }));

    listings.value = mapped;
    allListings.value = mapped;
  } catch (err) {
    console.error('Failed to fetch listings:', err);
  }
});

const getStarIcons = (rating) => {
  const stars = [];
  const fullStar = '/icons/star_full.png';
  const halfStar = '/icons/star_half.png';
  const emptyStar = '/icons/star_empty.png';

  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5;
  const empty = 5 - full - (half ? 1 : 0);

  for (let i = 0; i < full; i++) stars.push(fullStar);
  if (half) stars.push(halfStar);
  for (let i = 0; i < empty; i++) stars.push(emptyStar);

  return stars;
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
  margin-bottom: 18px;
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
