<template>
  <div class="page-frame">
    <div class="container">
      <header class="header">
        <div class="nav-container">
          <img src="/icons/Menu_Burger.png"
               alt="Menu"
               class="menu-icon"
               @click="toggleDropdown"
          />
          <ul class="dropdown" v-show="showDropdown">
            <li>
              <a href="#"
                   @click="navigateTo('/the_hub')">-&nbsp;&nbsp;&nbsp;the&nbsp;&nbsp;Hub
              <img src="/icons/Hub_Stars.png"
                   class="dropdown-icon"
                   alt="the Hub Icon"
              />
              </a>
            </li>
            <li>
              <a href="#"
                 @click="goToProfile">
                 -&nbsp;&nbsp;&nbsp;profile
                 <img src="/icons/Account_Signed_Out.png" class="dropdown-icon" alt="Profile Icon" />
              </a>
            </li>
            <li>
              <a href="#"
                 @click="navigateTo('/chat_to_us')">-&nbsp;&nbsp;&nbsp;chat&nbsp;&nbsp;to&nbsp;&nbsp;us
              <img src="/icons/Chat_To_Us.png"
                   alt="Chat"
                   class="dropdown-icon"
              />
              </a>
            </li>
            <li>
              <a href="#"
                 @click="navigateTo('/our_constitution')">-&nbsp;&nbsp;&nbsp;our&nbsp;&nbsp;constitution
                <img
                    src="/icons/Scroll.png"
                    alt="Constitution"
                    class="dropdown-icon"
                />
              </a>
            </li>
          </ul>
        </div>
        <div class="nav-section">
          <img :src="isLoggedIn ? '/icons/Account_Logged_In.png' : '/icons/Account_Signed_Out.png'"
               alt="Profile Icon" class="login-icon" @click="handleProfileClick"/>
          <img src="/icons/FocusHub_Logo.png" alt="FocusHub Logo" class="logo-icon" @click="navigateTo('/')" />
        </div>
      </header>

      <div class="left-margin">
        <main class="main-content">
          <h1 class="title">
            reviews
            <img
              src="/icons/Plus_Sign.png"
              alt="Plus"
              class="plus-icon"
              :class="{ rotated: isPlusRotated }"
              @click="checkIfCanSubmit"
            />
          </h1>
          <div v-if="showLoginPopup" class="login-popup">
            <div class="popup-content">
              Error: login with your BU email to access this feature
            </div>
          </div>
          <div v-if="alreadyReviewedPopup" class="already-reviewed-popup">
            <div class="popup-content">
              Error: you've already posted a review for this spot
            </div>
          </div>

          <div v-if="showCompleteProfilePopup" class="login-popup">
            <div class="popup-content">
                Please complete your profile!
                <br><br>
                <button @click="goToCompleteProfileForm">Fill Profile</button>
            </div>
          </div>


          <div v-if="showForm" class="form-popup">
            <form class="attributes-form" @submit.prevent>
              <div class="submit-icon-wrapper">
                <img src="/icons/Send.png"
                     alt="Submit"
                     class="submit-icon"
                     @click="submitForm" />
              </div>

              <div class="field">
                <span class="pop-up-listing-title">{{ listing.name }}</span>
                <br>
                <br>
                <span class="pop-up-user-name">{{ username }}</span>
                <div class="stars">
                  <div
                    v-for="i in 5"
                    :key="i"
                    class="star-container"
                    @mousemove="handleHover($event, i)"
                    @mouseleave="hoverRating = rating"
                    @click="handleClick($event, i)"
                  >
                    <img :src="getStarIcon(i)"
                         class="star-icon"
                         alt="Stars" />
                  </div>
                </div>
              </div>
                <div class="tags user-tags-row">
                  <span v-if="selectedReviewTags.length === 0"
                        class="tag orange">add
                  </span>
                  <span v-if="selectedReviewTags.length === 0"
                        class="tag green">some
                  </span>
                  <span v-if="selectedReviewTags.length === 0"
                        class="tag blue">tags
                  </span>
                  <span v-else v-for="(tag, i) in selectedReviewTags"
                        :key="i"
                        :class="['tag', tagClasses[tag]]">
                    {{ tag }}
                  </span>
                  <img src="/icons/Pen.png"
                       alt="Pen"
                       class="pen-icon"
                       @click="showPreferenceCard = !showPreferenceCard" />
                </div>

                <div v-if="showPreferenceCard" class="preferences-card">
                  <div class="preferences-header">
                    <div class="pop-up-tag-grid">
                      <span v-for="tag in spotPreferences"
                            :key="tag" :class="['tag', tagClasses[tag], { active: tempSelectedReviewTags.includes(tag) } ]"
                            @click="toggleTempTag(tag)">
                        {{ tag }}
                      </span>
                    </div>
                    <img src="/icons/Save.png"
                         alt="Save Preferences"
                         class="save-icon-small"
                         @click="updateReviewTags" />
                  </div>
                </div>

              <div class="field">
                <textarea v-model="reviewText" placeholder="share your thoughts..."></textarea>
              </div>
              <div class="camera-wrapper" @click="triggerFileInput">
                <img src="/icons/Camera.png"
                     alt="Upload Image"
                     class="camera-icon" />
                <br />
                <span class="optional-text">(optional)</span>
              </div>
              <input type="file" accept="image/*" ref="fileInput" @change="handleImageUpload" style="display: none;" />
            </form>
          </div>

          <div v-if="listing" class="listing-box">
            <div class="listing-image-wrapper">
              <img :src="'/images/' + listing.default_img" alt="listing image" class="listing-image" />
            </div>
              <div class="listing-content-wrapper">
                <div class="listing-header">
                  <p class="listing-title">{{ listing.name }}</p> <!-- No click event needed here -->
                  <img :src="favourites.has(listing.id) ? '/icons/Full_Heart.png' : '/icons/Heart.png'"
                       alt="Favourite"
                       class="favourite-icon"
                       @click="toggleFavourite(listing.id)" />
                </div>
                <p class="listing-address">
                  {{ listing.address }} • {{ formatOpeningHours(listing, selectedDay) }}
                </p>
                <p class="listing-status" :class="{ open: getOpenStatus(listing, selectedDay) === 'Open Now', closed: getOpenStatus(listing, currentDay) === 'Closed Now' }">
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

          <div class="reviews-section">
            <div v-for="review in reviews" :key="review.id" class="review-card">
              <div :class="['listing-image-wrapper', { 'has-image': review.image }]" v-if="review.image">
                <img :src="review.image" alt="Review Image" class="review-image" />
              </div>

              <div class="review-left">
                <div class="listing-header">
                  <div class="user-info">
                    <p class="review-user-name">{{ review.userName }}</p>
                  <p class="review-degree-info">{{ review.academicLevel }} • {{ review.college }} • {{ review.degree }}</p>
                  </div>
                  <div class="review-stars">
                    <img v-for="(icon, j) in getStarIcons(review.rating)"
                         :key="j"
                         :src="icon"
                         alt="Star"
                         class="star-icon"
                    />
                  </div>
                </div>
                <div class="review-content-wrapper">
                  <p class="review-content">{{ review.content }}</p>
                </div>
              </div>

              <div class="review-right">
                <div class="flag-date-wrapper">
                  <p class="review-date">({{ formatTimeAgo(review.timestamp) }})</p>
                  <img :src="flags.has(review.id) ? '/icons/Full_Flag.png' : '/icons/Flag.png'"
                       alt="Flag Post"
                       class="flag-icon"
                       @click="() => { toggleFlag(review.id); toggleFlagPopup(); }" />
                </div>
                <div class="review-tags">
                  <span v-for="(tag, j) in review.tags" :key="j" :class="['tag', tagClasses[tag]]">
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </div>

           <div v-if="showFlagPopup" class="flag-popup">
             <form class="attributes-form" @submit.prevent>
              <div class="submit-icon-wrapper">
                <img src="/icons/Send.png"
                     alt="Submit"
                     class="submit-icon"
                     @click="submitFlagForm"/>
              </div>
              <div class="field">
                <span class="pop-up-user-name">{{ username }}</span>
              </div>
                    <div class="tags">
                      <span
                        v-for="tag in flagOptions"
                        :key="tag"
                        :class="{ tag: true, active: selectedTag === tag, [tagClasses[tag]]: true }"
                        @click="selectedTag = tag"
                      >
                        {{ tag }}
                      </span>
                    </div>
              <div class="field">
                <textarea v-model="reviewText" placeholder="share your thoughts..."></textarea>
              </div>
            </form>
           </div>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
const route = useRoute();
const spot_id = parseInt(route.params.id);
import { onMounted, ref } from "vue";
import '@/assets/global.css';
import { favourites, toggleFavourite } from '@/store/favourites';
import { attributeTags, flagTags, tagColors } from "@/constants/Tags";
import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
import { loginWithGoogle } from "@/services/authService";
import { useAuthStatus } from "@/store/authStatus";
import { apiFetch } from '@/services/api';
import router from "@/router";
import { formatDistanceToNow } from 'date-fns';


const username = ref('Name');
const selectedTag = ref('');
const flagOptions = flagTags;
const { isLoggedIn, setLoggedIn } = useAuthStatus();
const listing = ref();
const topTagsPerSpot = ref({});
const selectedDay = ref(''); // Added selectedDay ref
const currentDayHours = ref(null); // Added currentDayHours ref
const currentDay = ref(''); // Added currentDay ref
const reviews = ref([]); // Added missing reviews ref

const auth = getAuth();
const firebaseUser = ref(null);
const showError = () => { /* your toast/toastr call */ };
const showReviewForm = () => { /* flip a boolean to render the form */ };

const reviewForm = ref({ user_id: null, spot_id: spot_id, rating: null, content: "" });

function formatTimeAgo(dateString) {
  return formatDistanceToNow(new Date(dateString), { addSuffix: true });
}

function secondsToHHMM(seconds) {
  const date = new Date(seconds * 1000);
  return date.toISOString().substring(11, 16); // "HH:MM"
}

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
  const storedUsername = localStorage.getItem('username');
  if (storedUsername) {
    username.value = storedUsername;
    console.log(username.value);
  }

  const storedUserId = localStorage.getItem('user_id');
  if (storedUserId) {
    user_id.value = storedUserId;
  }

  try {
    // Get the current day of the week
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    currentDay.value = daysOfWeek[new Date().getDay()];
    selectedDay.value = currentDay.value; // Set the selected day to current day

    // Fetch specific study spot by ID
    const spotsData = await apiFetch(`/study_spots/${spot_id}`);

    if (!spotsData.data || spotsData.data.length === 0) {
      console.error('No spot found for this spot_id');
      return;
    }

    // Find the data for the current day
    let currentDayData = spotsData.data.find(dayInfo => dayInfo.day === selectedDay.value);

    if (!currentDayData) {
      console.error(`No data found for ${selectedDay.value}`);
      // Fallback to the first entry if current day not found
      currentDayData = spotsData.data[0];
    }

    // Create the listing object with the current day's information
    listing.value = {
      id: currentDayData.spot_id,
      name: currentDayData.spot_name,
      address: currentDayData.address,
      default_img: currentDayData.default_img,
      rating: parseFloat(currentDayData.avg_rating) || 0,
      has_outlets: currentDayData.has_outlets === 1 || currentDayData.has_outlets === "Yes",
      has_food: currentDayData.has_food === 1 || currentDayData.has_food === "Yes",
      has_printing: currentDayData.has_printing === 1 || currentDayData.has_printing === "Yes",
      has_prayer_space: currentDayData.has_prayer_space === 1 || currentDayData.has_prayer_space === "Yes",
      has_spacious_seating: currentDayData.has_spacious_seating === 1 || currentDayData.has_spacious_seating === "Yes",
      has_meeting_rooms: currentDayData.has_meeting_rooms === 1 || currentDayData.has_meeting_rooms === "Yes",
      on_campus: currentDayData.on_campus === 1 || currentDayData.on_campus === "Yes",
      hours: {}
    };

    // Process hours for all days from the response
    spotsData.data.forEach(dayInfo => {
      if (dayInfo.day && dayInfo.open_time && dayInfo.close_time) {
        listing.value.hours[dayInfo.day] = {
          opens: secondsToHHMM(dayInfo.open_time),
          closes: secondsToHHMM(dayInfo.close_time)
        };
      }
    });

    // Highlight the current day's hours for easy access
    const currentHours = listing.value.hours[selectedDay.value];
    if (currentHours) {
      // You could store these separately if needed
      currentDayHours.value = currentHours;
    }

    const topTagsData = await apiFetch('/study_spots/top_tags');
    topTagsPerSpot.value = topTagsData.data;
    listing.value.tags = topTagsPerSpot.value[listing.value.id] || [];

    const reviewsData = await apiFetch(`/reviews/${spot_id}`);

    reviews.value = reviewsData.data.map(review => ({
      id: review.review_id,
      user_id: review.user_id,
      userName: review.user_name || "Name",
      degree: review.degree || '',
      academicLevel: review.academic_level || '',
      college: review.bu_college || '',
      content: review.review_content,
      rating: review.rating,
      image: review.review_img ? `/images/${review.review_img}` : null,
      tags: review.review_tags ? review.review_tags.split(',').map(tag => tag.trim()) : [],
      timestamp: review.timestamp,
    }));

    onAuthStateChanged(auth, async (user) => {
      firebaseUser.value = user;
      console.log("Authenticated user email:", user?.email);


      // only BU addresses allowed
      if (!user || !user.email.endsWith('@bu.edu')) {
        showError('Please sign in with your BU email.');
        return;
      }
      setLoggedIn(true);
      try {
        const { user_id } = await apiFetch('/users/me');
        reviewForm.value.user_id = user_id;
        showReviewForm();
      } catch (err) {
        showError('Could not fetch your profile; try again.');
      }
    });
  } catch (error) {
    console.error('Error loading spot data:', error);
  }
});

const goToProfile = () => {
  showDropdown.value = false;
  router.push(isLoggedIn.value ? '/profile' : '/unavailable');
};

const showDropdown = ref(false);
const toggleDropdown = () => {showDropdown.value = !showDropdown.value;};
const navigateTo = (path) => {window.location.href = path; showDropdown.value = false;};

const showForm = ref(false);

const showFlagPopup = ref(false);
const toggleFlagPopup = () => {
  showFlagPopup.value = !showFlagPopup.value;
};
const submitFlagForm = () => {
  console.log("Flag submitted with reason:", selectedTag.value, reviewText.value);
  selectedTag.value = '';
  reviewText.value = '';
  showFlagPopup.value = false;
};

const showLoginPopup = ref(false);
const alreadyReviewedPopup = ref(false);

const user_id = ref(localStorage.getItem('user_id') || null);

const showCompleteProfilePopup = ref(false);


function goToCompleteProfileForm() {
  showCompleteProfilePopup.value = false;
  router.push(`/profile`);
}

const checkIfCanSubmit = async () => {
  isPlusRotated.value = !isPlusRotated.value;

  // Reset any visible popups or form
  showLoginPopup.value = false;
  alreadyReviewedPopup.value = false;
  showForm.value = false;

  const token = localStorage.getItem('idToken'); // <- use consistent key
  if (!isLoggedIn.value || !token) {
    showLoginPopup.value = true;
    return;
  }

  try {
    const { review_exists } = await apiFetch(`/reviews/${spot_id}/exists`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (review_exists) {
      alreadyReviewedPopup.value = true;
    } else {
      showForm.value = true;
    }
  } catch (err) {
    console.error('Error checking review exists:', err);
  }
};

const rating = ref(0);
const hoverRating = ref(0);

const handleHover = (e, index) => {
  const { offsetX, target } = e;
  const width = target.clientWidth;
  const percent = offsetX / width;

  if (percent <= 0.5) hoverRating.value = index - 0.5;
  else hoverRating.value = index;
};

const handleClick = (e, index) => {
  const { offsetX, target } = e;
  const width = target.clientWidth;
  const percent = offsetX / width;

  rating.value = percent <= 0.5 ? index - 0.5 : index;
};

const getStarIcon = (i) => {
  const value = hoverRating.value || rating.value;
  if (value >= i) return '/icons/Full_Star.png';
  if (value >= i - 0.5) return '/icons/Half_Star.png';
  return '/icons/Star.png';
};

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

const isPlusRotated = ref(false);
const reviewText = ref('');
const uploadedImage = ref('');
const fileInput = ref();
const triggerFileInput = () => {fileInput.value?.click();};
const handleImageUpload = (e) => {
  const file = e.target.files[0];
  if (file && file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        uploadedImage.value = reader.result;
      }
    };
    reader.readAsDataURL(file);
  }
};

const flags = ref(new Set(JSON.parse(localStorage.getItem('flags') || '[]')));
const toggleFlag = (reviewId) => {
  if (flags.value.has(reviewId)) {
    flags.value.delete(reviewId);
  } else {
    flags.value.add(reviewId);
  }
  localStorage.setItem('flags', JSON.stringify([...flags.value]));
};

const spotPreferences = attributeTags;
const tagClasses = tagColors;
const showPreferenceCard = ref(false);

const reviewTagsKey = `reviewTags-${spot_id}`;

const selectedReviewTags = ref(JSON.parse(localStorage.getItem(reviewTagsKey) || '[]'));
const tempSelectedReviewTags = ref([...selectedReviewTags.value]);

const toggleTempTag = (tag) => {
  const index = tempSelectedReviewTags.value.indexOf(tag);
  if (index > -1) tempSelectedReviewTags.value.splice(index, 1);
  else tempSelectedReviewTags.value.push(tag);
};

const updateReviewTags = () => {
  selectedReviewTags.value = [...tempSelectedReviewTags.value];
  showPreferenceCard.value = false;
};

const submitForm = async () => {
  const user = getAuth().currentUser;
  const token = user ? await user.getIdToken() : null;

  if (!token) {
    showLoginPopup.value = true;
    return;
  }

  try {
    await apiFetch('/reviews', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        spot_id: spot_id,
        rating: rating.value,
        review_content: reviewText.value,
        review_tags: selectedReviewTags.value.join(',')
      })
    });

    // Refresh reviews
    const reviewsData = await apiFetch(`/reviews/${spot_id}`);
    if (Array.isArray(reviewsData.data)) {
      reviews.value = reviewsData.data.map(review => ({
        id: review.review_id,
        user_id: review.user_id,
        userName: review.user_name || "Name",
        degree: review.degree || '',
        academicLevel: review.academic_level || '',
        college: review.bu_college || '',
        content: review.review_content,
        rating: review.rating,
        image: review.review_img ? `/images/${review.review_img}` : null,
        tags: review.review_tags ? review.review_tags.split(',').map(tag => tag.trim()) : [],
        timestamp: review.timestamp,
      }));
    } else {
      console.error("reviewsData.data is not an array:", reviewsData);
      reviews.value = []; // fallback
    }
    // Reset form
    reviewText.value = '';
    uploadedImage.value = '';
    rating.value = 0;
    hoverRating.value = 0;
    showForm.value = false;
    isPlusRotated.value = false;

  } catch (err) {
    console.error('Failed to submit review:', err);
  }
};



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

</script>

<style>

.form-popup {
  margin-top: 100px;
  width: 455px;
  position: absolute;
  top: 180px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999;
  background: #f9fdad;
  border: 2px solid black;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.flag-popup {
  margin-top: 120px;
  width: 455px;
  position: absolute;
  top: 380px;
  left: 75%;
  transform: translateX(-50%);
  z-index: 998;
  background: #f9fdad;
  border: 2px solid black;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.pop-up-listing-title{
  cursor: none;
  font-size: 22px;
  font-family: 'Rubik One', serif;
}

.submit-icon{
  margin-right: -5px;
}

.save-icon-small{
  width: 35px;
  padding: 0 5px 5px 10px;
  cursor: pointer;
}

input,
textarea {
  display: block;
  justify-content: center;
  margin-top: 10px;
  width: 91%;
  height: 80px;
  background-color: #fdfde3;
  border: 1.5px solid black;
  font-family: 'Sansation Light', serif;
  padding: 15px;
  font-size: 17px;
  font-style: italic;
  border-radius: 22px;
  color: gray;
}

.listing-box {
  display: flex;
  align-items: flex-start;
  border: 1.5px solid black;
  border-radius: 30px;
  background: #fdfde3;
  padding: 15px;
  margin: 20px 0;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
}

.review-card{
  display: flex;
  align-items: stretch;
  grid-template-columns: 1fr 160px;
  height: fit-content;
  border: 1.5px solid black;
  border-radius: 30px;
  background: #fdfde3;
  padding: 15px;
  margin: 20px 0;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
}

.review-left {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 82%;
  margin-left: 5px;
  /*border: 2px dashed darkblue;*/
}

.review-right {
  display: flex;
  width: 18%;
  margin-right: 5px;
  flex-direction: column;
  gap: 10px;
  justify-content: space-between;
  /*border: 2px dashed rebeccapurple;*/
}


.pop-up-listing-title{
  font-size: 24px;
}

.pop-up-user-name{
  font-family: 'Sansation Regular', serif;
  font-size: 19px;
}

.camera-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 10px;
  cursor: pointer;
}

.pen-icon {
  width: 35px;
  height: auto;
  align-items: center;
  cursor: pointer;
}

.camera-icon {
  width: 75px;
  height: auto;
  align-items: center;
}

/*.review-image-preview {
  width: 120px;
  aspect-ratio: 1 / 1;
  border: 1px solid black;
  display: block;
  margin: 10px auto 0;
  border-radius: 12px;
  object-fit: cover;
}*/

.preferences-card {
  background: #fdfde3;
  border: 1.5px solid black;
  padding: 10px;
  margin: 15px 0;
  border-radius: 15px;
  position: relative;
}

.preferences-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.pop-up-tag-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  flex-grow: 1;
}

.tag{
  width: fit-content;
}

.plus-icon {
  width: 35px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.plus-icon.rotated {
  transform: rotate(45deg);
}

.flag-icon {
  display: block;
  justify-content: flex-end;
  width: 40px;
  height: auto;
  margin-left: 70px;
  margin-top: -10px;
  cursor: pointer;
  /*border: 2px dashed pink;*/
}

.optional-text{
  font-family: 'Sansation Light', serif;
  font-size: 13px;
  align-items: center;
}

.stars {
  margin-top: 10px;
  display: flex;
  gap: 4px;
}

.star-icon {
  cursor: pointer;
  transition: transform 0.15s ease;
}

.listing-box {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  border: 1.5px solid black;
  border-radius: 30px;
  background: #fdfde3;
  padding: 20px;
  margin: 20px 0;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
  position: relative;
}

.review-card .listing-image-wrapper,
.listing-box .listing-image-wrapper {
  width: 155px;
  height: 135px;
  /*border: 2px dashed red;*/
}

.review-card .listing-image-wrapper {
  align-self: center; /* <-- add this */
}

.listing-image-wrapper.has-image {
  margin-right: 35px;
}

.review-card .review-image,
.listing-box .listing-image {
  width: 155px;
  height: 135px;
  margin-left: 10px;
  object-fit: cover;
  border-radius: 20px;
  border: 1px solid black;
}

.listing-content-wrapper {
  display: grid;
  grid-template-columns: auto auto;
  grid-template-areas:
    "name date"
    "degree degree"
    "message message";
  gap: 5px 20px;
  /*border: 2px dashed yellow;*/
}

.listing-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  line-height: 10%;
  /*border: 2px dashed deeppink;*/
}

.listing-title {
  font-family: 'Rubik One', serif;
  font-size: 27px;
  margin: 15px 25px;
}

.listing-address {
  font-size: 18px;
  font-family: 'Sansation Light', serif;
  letter-spacing: 1px;
  margin: 6px 25px;
}

.listing-tags {
  display: flex;
  gap: 7px;
  flex-shrink: 0;
  width: fit-content;
  margin: 5px 22px;
}

.listing-rating {
  display: flex;
  margin-right: -5px;
  flex-shrink: 0;
  width: fit-content;
}

.listing-footer-wrapper{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 10px;
}

.favourite-icon {
  display: flex;
  justify-content: flex-end;
  width: 40px;
  height: auto;
  margin-top: -2.5px;
  cursor: pointer;
}

.review-user-name{
  display: flex;
  margin: 10px;
  justify-content: space-between;
  align-items: center;
  font-family: 'Sansation Regular', serif;
  font-size: 27px;
  /*border: 2px dashed brown;*/
}

.review-degree-info{
  width: fit-content;
  letter-spacing: 0.5px;
  font-family: 'Sansation Light', serif;
  font-size: 17px;
  font-style: italic;
  /*border: 2px dashed green;*/
}

.review-date{
  font-family: 'Sansation Light', serif;
  width: fit-content;
  font-size: 13px;
  letter-spacing: normal;
  word-spacing: normal;
  margin-top: -5px;
  /*border: 2px dashed orangered;*/
}

.flag-date-wrapper {
  display: flex;
  height: 55px;
  align-items: center;
  justify-content: center;
  /*border: 2px dashed darkslategray;*/
}

.review-degree-info,
.review-content {
  margin: 7px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.review-content {
  flex: 1;
  line-height: 135%;
  font-family: 'Sansation Light', serif;
  font-size: 16.5px;
  letter-spacing: 0.5px;
  word-spacing: 1px;
  /*border: 2px dashed orange;*/
}

.review-content-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  /*border: 2px dashed chartreuse;*/
}

.review-stars{
  display: flex;
  margin-top: -20px;
  margin-right: 120px;
  flex-shrink: 0;
  /*border: 2px dashed purple;*/
}

.review-tags {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  /*border: 2px dashed greenyellow;*/
}

.login-popup, .already-reviewed-popup {
  position: absolute;
  top: 270px;
  left: 50%;
  transform: translateX(-50%);
  width: 400px;
  background: #f9fdad;
  border: 2px solid black;
  border-radius: 20px;
  padding: 15px;
  text-align: center;
  z-index: 1000;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.popup-content {
  font-family: 'Victor Mono', serif;
  font-size: 18px;
  letter-spacing: 1.2px;
}


</style>