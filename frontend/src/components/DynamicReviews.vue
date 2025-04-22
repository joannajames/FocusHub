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
              @click="toggleForm"
            />
          </h1>

          <div v-if="showForm" class="form-popup">
            <form class="attributes-form" @submit.prevent>
              <div class="submit-icon-wrapper">
                <img src="/icons/Send.png"
                     alt="Submit"
                     class="submit-icon"
                     :class="{ rotated: isPlusRotated }"
                     @click="submitForm" />
              </div>

              <div class="field">
                <span class="pop-up-listing-title">{{ listing.name }}</span>
                <br>
                <br>
                <span class="pop-up-user-name">Anastasia</span>
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
                    <div class="tag-grid">
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
              <img :src="`/images/${listing.default_img_url}`"
                   :alt="listing.image"
                    class="listing-image" />
            </div>
              <div class="listing-content-wrapper">
                <div class="listing-header">
                  <p class="listing-title">
                    {{ listing.name }}
                  </p>
                  <img
                    :src="favourites.has(listing.id) ? '/icons/Full_Heart.png' : '/icons/Heart.png'"
                    alt="Favourite"
                    class="favourite-icon"
                    @click="toggleFavourite(listing.id)"
                  />
                </div>
                <p class="listing-address">{{ listing.address }} • {{ selectedDay}}</p>
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

          <div class="reviews-section">
            <div v-for="(review, i) in reviews" :key="i" class="review-card">
              <div class="listing-image-wrapper">
                <img :src="review.image"
                     alt="Review Image"
                     class="review-image" />
              </div>
                <div class="listing-content-wrapper">
                  <div class="listing-header">
                    <p class="user-name" style="grid-area: name">Anastasia</p>
                    <div class="review-stars">
                      <img v-for="(icon, j) in getStarIcons(review.rating)"
                           :key="j"
                           :src="icon"
                           alt="Star"
                           class="star-icon" />
                    </div>
                    <p class="date">({{ formatTimeAgo(review.date) }})</p>
                    <img :src="flags.has(review.id) ? '/icons/Full_Flag.png' : '/icons/Flag.png'"
                         alt="Flag Post"
                         class="flag-icon"
                         @click="() => { toggleFlag(review.id); toggleFlagPopup(); }"
                    />
                  </div>
                    <p class="user-degree"
                       style="grid-area: degree">Undergraduate • College of Arts & Sciences  • Sociology
                    </p>
                    <div class="tags-vertical">
                      <span v-for="(tag, j) in review.tags"
                            :key="j"
                            :class="['tag', tagClasses[tag]]">
                        {{ tag }}
                      </span>
                    </div>
                    <p class="message" style="grid-area: message">{{ review.message }}</p>
                </div>
            </div>
          </div>

           <div v-if="showFlagPopup" class="form-popup">
             <form class="attributes-form" @submit.prevent>
              <div class="submit-icon-wrapper">
                <img src="/icons/Send.png"
                     alt="Submit"
                     class="submit-icon"
                     @click="submitFlagForm"/>
              </div>
              <div class="field">
                <span class="pop-up-user-name">post by: Anastasia</span>
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

const selectedTag = ref('');
const flagOptions = flagTags;
const { isLoggedIn, setLoggedIn } = useAuthStatus();
import router from "@/router";
const listing = ref();

const fetchListings = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/spots');
    const rawData = await res.json();
    const spots = rawData.data || [];

    const mapped = spots.map((spot) => ({
      id: spot.spot_id,
      name: spot.spot_name,
      address: spot.address,
      rating: parseFloat(spot.avg_rating) || 0,
      default_img_url: spot.default_img,
      opening_hours: {
        Sunday: `${spot.sunday_open?.slice(0, 5)}–${spot.sunday_close?.slice(0, 5)}`,
        Monday: `${spot.monday_open?.slice(0, 5)}–${spot.monday_close?.slice(0, 5)}`,
        Tuesday: `${spot.tuesday_open?.slice(0, 5)}–${spot.tuesday_close?.slice(0, 5)}`,
        Wednesday: `${spot.wednesday_open?.slice(0, 5)}–${spot.wednesday_close?.slice(0, 5)}`,
        Thursday: `${spot.thursday_open?.slice(0, 5)}–${spot.thursday_close?.slice(0, 5)}`,
        Friday: `${spot.friday_open?.slice(0, 5)}–${spot.friday_close?.slice(0, 5)}`,
        Saturday: `${spot.saturday_open?.slice(0, 5)}–${spot.saturday_close?.slice(0, 5)}`
      }
    }));

    listing.value = mapped.find((s) => s.id === spotId);
  } catch (err) {
    console.error('Failed to fetch listings:', err);
  }
};

onMounted(() => {
  fetchListings();
});

const goToProfile = () => {
  showDropdown.value = false;
  router.push(isLoggedIn.value ? '/profile' : '/unavailable');
};

const showDropdown = ref(false);
const toggleDropdown = () => {showDropdown.value = !showDropdown.value;};
const navigateTo = (path) => {window.location.href = path; showDropdown.value = false;};

const showForm = ref(false);
const toggleForm = () => {
  showForm.value = !showForm.value;
  isPlusRotated.value = !isPlusRotated.value;
};
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

const rating = ref(0);          // final selected rating
const hoverRating = ref(0);     // temporary preview on hover

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
  const stars = [];
  const fullStar = '/icons/Full_Star.png';
  const halfStar = '/icons/Half_Star.png';
  const emptyStar = '/icons/Star.png';

  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5;
  const empty = 5 - full - (half ? 1 : 0);

  for (let i = 0; i < full; i++) stars.push(fullStar);
  if (half) stars.push(halfStar);
  for (let i = 0; i < empty; i++) stars.push(emptyStar);

  return stars;
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
const selectedDay = ref(new Date().toLocaleDateString('en-US', { weekday: 'long' }));
const showPreferenceCard = ref(false);

const reviewTagsKey = `reviewTags-${spotId}`;
const reviewKey = `reviews-${spotId}`;

const selectedReviewTags = ref(JSON.parse(localStorage.getItem(reviewTagsKey) || '[]'));
const tempSelectedReviewTags = ref([...selectedReviewTags.value]);

const reviews = ref(JSON.parse(localStorage.getItem(reviewKey) || '[]'));

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
  showForm.value = false;
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

function handleProfileClick() {
  if (isLoggedIn.value) {
    signOut(auth).then(() => {
      setLoggedIn(false); // Updates both ref + localStorage
    });
  } else {
    loginWithGoogle().then(() => {
      setLoggedIn(true);  // Not strictly needed if onAuthStateChanged is set up
    });
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
  align-items: flex-start;
  border: 1.5px solid black;
  border-radius: 30px;
  background: #fdfde3;
  padding: 15px;
  margin: 20px 0;
  box-shadow: 2px 2px 6px rgba(0, 0, 0, 0.1);
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

.tag-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  flex-grow: 1;
}

.tags-vertical {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
  margin-top: 15px;
}

.tag{
  cursor: pointer;
}

.date{
  font-family: 'Sansation Light', serif;
  font-size: 15px;
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
  display: flex;
  justify-content: flex-end;
  width: 40px;
  height: auto;
  margin-top: -10px;
  cursor: pointer;
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
}

.review-card .review-image,
.listing-box .listing-image {
  width: 155px;
  height: 135px;
  object-fit: cover;
  border-radius: 20px;
  border: 1px solid black;
}

.listing-content-wrapper {
  flex: 1;
  flex-direction: column;
  justify-content: flex-start;
  display: grid;
  grid-template-areas:
  "name date"
  "degree degree"
  "message message";
}

.listing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  line-height: 10%;
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

.user-name{
  display: flex;
  justify-content: space-between;
  align-items: center;
  line-height: 10%;
  margin: 15px 25px;
  font-family: 'Sansation Regular', serif;
  font-size: 26px;
}

.user-degree{
  margin: 15px 25px;
  font-family: 'Sansation Light', serif;
  font-size: 16px;
  font-style: italic;
}

.message{
  font-family: 'Sansation Light', serif;
  font-size: 16px;
}

</style>
