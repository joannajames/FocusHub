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
              Error: you’ve already posted a review for this spot
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

          <div v-if="listing" class="listing-box" :key="listing.id">
            <div class="listing-image-wrapper">
              <img :src="`/images/${listing.default_img}`"
                   :alt="listing.image"
                    class="listing-image" />
            </div>
              <div class="listing-content-wrapper">
                <div class="listing-header">
                  <p class="listing-title">{{ listing.name }}</p>
                  <img
                    :src="favourites.has(listing.id) ? '/icons/Full_Heart.png' : '/icons/Heart.png'"
                    alt="Favourite"
                    class="favourite-icon"
                    @click="toggleFavourite(listing.id)"
                  />
                </div>
                <p class="listing-address">{{ listing.address }} • {{ formatOpeningHours(listing, currentDay) }}</p>
                <div class="listing-footer-wrapper">
                  <div class="listing-tags">
                    <span
                        v-for="tag in (Array.isArray(listing.tags) ? listing.tags : []).sort((a, b) => a.localeCompare(b))"
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
const spotId = parseInt(route.params.id);
import {onMounted, ref} from "vue";
import '@/assets/global.css';
import { favourites, toggleFavourite } from '@/store/favourites';
import {attributeTags, flagTags, tagColors} from "@/constants/Tags";
import { signOut} from "firebase/auth";
import {auth} from "@/firebase";
import {loginWithGoogle} from "@/services/authService";
import {useAuthStatus} from "@/store/authStatus";
import { onAuthStateChanged } from 'firebase/auth';

const username = ref('Name');
const selectedTag = ref('');
const flagOptions = flagTags;
const { isLoggedIn, setLoggedIn } = useAuthStatus();
import router from "@/router";
const listing = ref();
const topTagsPerSpot = ref({});

function secondsToHHMM(seconds) {
  const date = new Date(seconds * 1000);
  return date.toISOString().substring(11, 16); // "HH:MM"
}

onMounted(async () => {
  const storedUsername = localStorage.getItem('username');
  if (storedUsername) {
    username.value = storedUsername;
  }

  const storedUserId = localStorage.getItem('userId');
  if (storedUserId) {
    userId.value = storedUserId;
  }

  try {
    const spotRes = await fetch(`http://127.0.0.1:8000/study_spots/${spotId}`);
    const spotData = await spotRes.json();
    const spot = spotData.data;

    listing.value = {
      id: spot.spot_id,
      name: spot.spot_name,
      address: spot.address,
      default_img: spot.default_img,
      rating: parseFloat(spot.avg_rating) || 0,
      has_outlets: spot.has_outlets === 1 || spot.has_outlets === "Yes",
      has_food: spot.has_food === 1 || spot.has_food === "Yes",
      has_printing: spot.has_printing === 1 || spot.has_printing === "Yes",
      has_prayer_space: spot.has_prayer_space === 1 || spot.has_prayer_space === "Yes",
      has_spacious_seating: spot.has_spacious_seating === 1 || spot.has_spacious_seating === "Yes",
      has_meeting_rooms: spot.has_meeting_rooms === 1 || spot.has_meeting_rooms === "Yes",
      on_campus: spot.on_campus === 1 || spot.on_campus === "Yes",
      hours: (spot.hours || []).reduce((acc, hour) => {
        acc[hour.day] = {
          opens: secondsToHHMM(hour.opens),
          closes: secondsToHHMM(hour.closes),
        };
        return acc;
      }, {})
    };

    // Fetch the top tags separately (optional if you want them per listing)
    const tagsRes = await fetch('http://127.0.0.1:8000/study_spots/top_tags');
    const tagsData = await tagsRes.json();
    topTagsPerSpot.value = tagsData.data;
    listing.value.tags = topTagsPerSpot.value[listing.value.id] || [];

    const reviewsRes = await fetch(`http://127.0.0.1:8000/reviews/${spotId}`);
    const reviewsData = await reviewsRes.json();

    reviews.value = reviewsData.data.map(review => ({
      id: review.review_id,
      userId: review.user_id,
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

    onAuthStateChanged(auth, (user) => {
  if (user) {
    isLoggedIn.value = true;
    localStorage.setItem('userId', user.uid);
    userId.value = user.uid;
  } else {
    isLoggedIn.value = false;
    localStorage.removeItem('userId');
    userId.value = null;
  }
});

  } catch (err) {
    console.error("Data fetch failed:", err);
  }
});

function formatOpeningHours(listing, currentDay) {
  const hours = listing.hours?.[currentDay];
  if (!hours) return 'Closed';
  return `${hours.opens}-${hours.closes}`;
}

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

const userId = ref(localStorage.getItem('userId') || null);

const checkIfCanSubmit = async () => {
  isPlusRotated.value = !isPlusRotated.value;

  if (showLoginPopup.value || alreadyReviewedPopup.value || showForm.value) {
    showLoginPopup.value = false;
    alreadyReviewedPopup.value = false;
    showForm.value = false;
    return;
  }

  if (!isLoggedIn.value) {
    showLoginPopup.value = true;
    return;
  }

  userId.value = localStorage.getItem('userId');
  if (!userId.value) {
    showLoginPopup.value = true;
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/reviews/${spotId}/user/${userId.value}`);
    if (response.ok) {
      alreadyReviewedPopup.value = true;
    } else if (response.status === 404) {
      showForm.value = true;
    } else {
      console.error('Unexpected server response:', response.status);
    }
  } catch (err) {
    console.error('Error checking if review exists:', err);
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
const currentDay = ref(new Date().toLocaleDateString('en-US', { weekday: 'long' }));
const showPreferenceCard = ref(false);

const reviewTagsKey = `reviewTags-${spotId}`;
const reviewKey = `reviews-${spotId}`;

const selectedReviewTags = ref(JSON.parse(localStorage.getItem(reviewTagsKey) || '[]'));
const tempSelectedReviewTags = ref([...selectedReviewTags.value]);

const reviews = ref([]);

const toggleTempTag = (tag) => {
  const index = tempSelectedReviewTags.value.indexOf(tag);
  if (index > -1) tempSelectedReviewTags.value.splice(index, 1);
  else tempSelectedReviewTags.value.push(tag);
};

const updateReviewTags = () => {
  selectedReviewTags.value = [...tempSelectedReviewTags.value];
  showPreferenceCard.value = false;
};

const submitForm = () => {
  const newReview = {
    id: crypto.randomUUID(),
    tags: [...selectedReviewTags.value],
    message: reviewText.value,
    date: new Date().toISOString(),
    image: uploadedImage.value,
    rating: rating.value,
  };
  isPlusRotated.value = !isPlusRotated.value;
  reviews.value = [newReview];
  localStorage.setItem(reviewTagsKey, JSON.stringify(selectedReviewTags.value));
  localStorage.setItem(reviewKey, JSON.stringify(reviews.value));
  reviewText.value = '';
  uploadedImage.value = '';
  rating.value = 0;
  hoverRating.value = 0;
};

function formatTimeAgo(dateString) {
  const now = new Date();
  const past = new Date(dateString);
  const diffMs = now - past;

  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(diffMs / (1000 * 60));
  const hours = Math.floor(diffMs / (1000 * 60 * 60));
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const months = Math.floor(days / 30);
  const years = Math.floor(days / 365);

  if (seconds < 60) return 'just now';
  if (minutes < 60) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  if (days < 30) return `${days} day${days > 1 ? 's' : ''} ago`;
  if (months < 12) return `${months} month${months > 1 ? 's' : ''} ago`;
  return `${years} year${years > 1 ? 's' : ''} ago`;
}

async function handleProfileClick() {
  if (isLoggedIn.value) {
    await signOut(auth);
    setLoggedIn(false);
    localStorage.removeItem('userId');
    userId.value = null;
  } else {
    try {
      await loginWithGoogle();
      const user = auth.currentUser;
      if (user) {
        localStorage.setItem('userId', user.uid);
        userId.value = user.uid;
        setLoggedIn(true);
        window.location.reload();
      } else {
        console.error('Login succeeded but no user info found.');
      }
    } catch (error) {
      console.error('Login failed:', error);
    }
  }
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
