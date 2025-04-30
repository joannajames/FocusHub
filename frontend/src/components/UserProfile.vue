<template>
  <div class="page-frame">
    <div class="container">
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
          <img :src="isLoggedIn ? '/icons/Account_Logged_In.png' : '/icons/Account_Signed_Out.png'"
               alt="Profile Icon" class="login-icon" @click="handleProfileClick"/>
          <img src="/icons/FocusHub_Logo.png" alt="FocusHub Logo" class="logo-icon" @click="navigateTo('/')" />
        </div>
      </header>

      <div class="main-content left-margin">
        <h1 class="title">profile</h1>

        <div class="card profile-card user-card">
          <img
              :src="profilePicture"
              alt="Profile Picture"
              class="avatar"
              @click="triggerFileInput"
          />
          <input
              type="file"
              accept="image/*"
              ref="fileInput"
              @change="handleImageUpload"
              style="display: none;"
          >
          <div class="info">
            <h2>
              {{ username }}
            </h2>
            <br>
            <p class="grad-info" v-if="!showAcademicForm">
              {{ academicLevel }} • {{ college }} • {{ degree }}
              <img
                  src="/icons/Pen.png"
                  alt="Edit Academic Info"
                  class="pen-icon-grad"
                  @click="toggleAcademicForm"
              />
            </p>

            <div v-else class="grad-wrapper">
              <input type="text"
                     v-model="tempAcademicLevel"
                     placeholder="academic level..."
                     list="academicLevels"
                     class="grad-input" />
              <span class="dot">•</span>
              <input type="text"
                     v-model="tempCollege"
                     placeholder="college..."
                     list="colleges"
                     class="grad-input" />
              <span class="dot">•</span>
              <input type="text"
                     v-model="tempDegree"
                     placeholder="degree..."
                     class="grad-input" />
              <img src="/icons/Save.png"
                   class="save-icon"
                   @click="saveGradInfo" />

              <datalist id="academicLevels">
                <option value="Undergrad"></option>
                <option value="Grad"></option>
                <option value="PhD"></option>
              </datalist>
              <datalist id="colleges">
                <option value="CAS"></option>
                <option value="COM"></option>
                <option value="ENG"></option>
                <option value="MET"></option>
                <option value="CFA"></option>
                <option value="CGS"></option>
                <option value="SAR"></option>
                <option value="CDS"></option>
                <option value="SHA"></option>
                <option value="Pardee"></option>
                <option value="Questrom"></option>
                <option value="Kilachand"></option>
                <option value="Wheelock"></option>
              </datalist>
            </div>
            <div class="tags">
              <span v-if="selectedTags.length === 0" class="tag pink">tell</span>
              <span v-if="selectedTags.length === 0" class="tag yellow">us</span>
              <span v-if="selectedTags.length === 0" class="tag blue">your</span>
              <span v-if="selectedTags.length === 0" class="tag green">study</span>
              <span v-if="selectedTags.length === 0" class="tag orange">preferences</span>
              <span
                v-else
                v-for="(tag, i) in selectedTags"
                :key="i"
                :class="['tag', tagClasses[tag]]"
              >
                {{ tag }}
              </span>
              <img
                src="/icons/Pen.png"
                alt="Pen"
                class="pen-icon"
                @click="toggleForm"
              />
            </div>
          </div>
        </div>

        <div v-if="showForm" class="form-popup">
          <form class="attributes-form" @submit.prevent>
            <div class="submit-icon-wrapper">
              <img
                src="/icons/Save.png"
                alt="Save"
                class="save-icon"
                @click="submitForm"
              />
            </div>

            <div class="field">
              <div class="tags">
                <span
                  v-for="tag in studyPreferences"
                  :key="tag"
                  :class="{ tag: true, active: selectedTags.includes(tag), [tagClasses[tag]]: true }"
                  @click="toggleTag(tag)"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </form>
        </div>

        <div class="grid">
          <div class="left">

            <div class="card">
              <h3>my favourite spots:</h3>

              <div>
                <div v-if="favouriteSpots.length">
                  <div
                      v-for="listing in favouriteSpots"
                      :key="listing.id"
                      class="listing-box"
                  >
                    <img
                        :src="`/images/${listing.default_img}`"
                        :alt="listing.image"
                        class="fav-image"
                    />
                    <div class="listing-content">
                      <h3 class="listing-title">{{ listing.name }}</h3>
                      <p class="listing-address">{{ listing.address }}</p>
                      <div class="listing-tags">
                        <span
                            v-for="(tag, i) in listing.attributes"
                            :key="i"
                            :class="['tag', tag.color]"
                        >
                          {{ tag.name }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-else class="no-favourites">
                  You haven't favourited any study spots yet!
                </div>
              </div>
            </div>

            <div class="card">
              <h3>my reviews:</h3>

              <div>
                <div v-if="myReviews.length">
                  <div
                      v-for="review in myReviews"
                      :key="review.id"
                      class="user-review-card"
                    >
                      <div class="user-review-left">
                        <p class="spot-name">{{ review.spot_name }}</p>
                        <p class="review-text">{{ review.content }}</p>
                      </div>
                      <div class="user-review-right">
                        <div class="stars">
                          <img
                            v-for="(icon, index) in getStarIcons(review.rating)"
                            :key="index"
                            :src="icon"
                            class="star-icon"
                            alt="rating star"
                          />
                        </div>
                        <p class="review-date">({{ formatTimeAgo(review.timestamp) }})</p>
                      </div>
                    </div>

                </div>
                <div v-else class="no-reviews">
                  You haven't posted any reviews yet!
                </div>
              </div>
            </div>
          </div>
          <div class="right">
            <div class="card">
              <h3>my recommended spots:</h3>

              <div v-if="recommendedSpots.length">
                <div
                    v-for="listing in recommendedSpots"
                    :key="listing.id"
                    class="listing-box"
                >
                  <img
                      :src="`/images/${listing.default_img}`"
                      :alt="listing.image"
                      class="image"
                  />
                  <div class="listing-content">
                    <h3 class="listing-title">{{ listing.name }}</h3>
                    <p class="listing-address">{{ listing.address }}</p>
                    <div class="listing-tags">
                      <span
                          v-for="(tag, i) in listing.tags"
                          :key="i"
                          class="tag"
                      >
                        {{ tag }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="no-recommendations">
                No recs yet. Tell us your study preferences to get some!
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref, watch, computed} from 'vue';
import '@/assets/global.css';
import {attributeTags, tagColors} from "@/constants/Tags";

import { onAuthStateChanged } from 'firebase/auth';
import {signOut} from "firebase/auth";
import {auth} from "@/firebase";
import {loginWithGoogle} from "@/services/authService";
import { useAuthStatus } from '@/store/authStatus';
import { useRouter } from 'vue-router';
import { apiFetch } from '@/services/api';

const router = useRouter();
const { isLoggedIn, setLoggedIn } = useAuthStatus();
const showDropdown = ref(false);
const showForm = ref(false);
const selectedTags = ref(JSON.parse(localStorage.getItem('selectedTags') || '[]'));
const studyPreferences = attributeTags;
const tagClasses = tagColors;
const favouriteSpots = ref([]);
const username = ref(localStorage.getItem('username') || 'Name');


const academicLevel = ref(localStorage.getItem('academicLevel') || '');
const college = ref(localStorage.getItem('college') || '');
const degree = ref(localStorage.getItem('degree') || '');

const showAcademicForm = ref(false);

const toggleAcademicForm = () => {
  showAcademicForm.value = !showAcademicForm.value;
};

const goToProfile = () => {
  showDropdown.value = false;
  router.push(isLoggedIn.value ? '/profile' : '/unavailable');
};

watch(selectedTags, (newVal) => {
  localStorage.setItem('selectedTags', JSON.stringify(newVal));
}, { deep: true });

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const toggleForm = () => {
  showForm.value = !showForm.value;
};

const toggleTag = (tag) => {
  const index = selectedTags.value.indexOf(tag);
  if (index > -1) {
    selectedTags.value.splice(index, 1); // remove
  } else {
    selectedTags.value.push(tag); // add
  }
};

const submitForm = async () => {
  showForm.value = false;

  try {
    const res = await apiFetch('/users/me');
    const userId = res.user_id;

    await apiFetch(`/users/${userId}/complete_profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        degree: degree.value,
        academic_level: academicLevel.value,
        bu_college: college.value,
        personal_tags: selectedTags.value.join(',')
      })
    });

    console.log('Tags and profile info updated in DB');
  } catch (error) {
    console.error('Failed to update profile in DB:', error);
  }
};


const navigateTo = (path) => {
  router.push(path);
  showDropdown.value = false;
};

function formatTimeAgo(dateString) {
  const now = new Date();
  const posted = new Date(dateString);
  const diff = Math.floor((now - posted) / (1000 * 60 * 60 * 24));

  if (diff === 0) return 'today';
  if (diff === 1) return '1 day ago';
  return `${diff} days ago`;
}


async function handleProfileClick() {
  if (isLoggedIn.value) {
    await signOut(auth);
    setLoggedIn(false);
    return;
  }
  await loginWithGoogle();

  setLoggedIn(true);

  const response = await apiFetch('/users/me');
  const { is_new_user } = response;
  if (is_new_user) {
      router.push('/profile');
  } else {
      router.push('/the_hub');
  }
}

watch(isLoggedIn, (val) => {
  if (!val) {
    router.push('/unavailable');
  }
});

const profilePicture = ref(localStorage.getItem('profilePicture') || '/images/Default_Profile.png');
const fileInput = ref();

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleImageUpload = (e) => {
  const file = e.target.files[0];
  if (file && file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        profilePicture.value = reader.result;
        localStorage.setItem('profilePicture', reader.result);
      }
    };
    reader.readAsDataURL(file);
  }
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


const myReviews = ref([]);

const tempAcademicLevel = ref('');
const tempCollege = ref('');
const tempDegree = ref('');

const saveGradInfo = () => {
  if (tempAcademicLevel.value) academicLevel.value = tempAcademicLevel.value;
  if (tempCollege.value) college.value = tempCollege.value;
  if (tempDegree.value) degree.value = tempDegree.value;

  // Save to localStorage
  localStorage.setItem('academicLevel', academicLevel.value);
  localStorage.setItem('college', college.value);
  localStorage.setItem('degree', degree.value);

  showAcademicForm.value = false;
};

onMounted(() => {
  onAuthStateChanged(auth, async (user) => {
    if (!user || !user.email.endsWith('@bu.edu')) {
      console.warn("Not signed in with BU email");
      router.push('/unavailable');
      return;
    }

    setLoggedIn(true);
    try {
      const res = await apiFetch('/users/me');
      const userInfo = res.user_info;
      const user_id = res.user_id;

      username.value = userInfo.user_name;
      academicLevel.value = userInfo.academic_level || '';
      college.value = userInfo.bu_college || '';
      degree.value = userInfo.degree || '';

      if (userInfo.personal_tags) {
        selectedTags.value = userInfo.personal_tags.split(',').map(tag => tag.trim());
      }

      const reviewRes = await apiFetch(`/users/${user_id}/reviews`);
      myReviews.value = reviewRes.reviews || [];

      // Load listings
      const spotsData = await apiFetch('/study_spots');
      localStorage.setItem('allListings', JSON.stringify(spotsData.data));

      const favRes = await apiFetch(`/favorites/user/${user_id}`);
      favouriteSpots.value = favRes.data || [];
    } catch (err) {
      console.error('Failed to load favourites:', err);
    }
  });
});



const recommendedSpots = computed(() => {
  const allListings = JSON.parse(localStorage.getItem('allListings') || '[]');

  if (selectedTags.value.length === 0) {
    return [];
  }

  return allListings.filter(listing => {
    const listingTags = listing.tags || [];
    return selectedTags.value.every(tag => listingTags.includes(tag));
  });
});

</script>

<style>
.grid {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.left, .right {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 20px;
}

.profile-card {
  position: relative;
  padding: 15px;
  margin-top: 30px;
  margin-bottom: 20px;
  font-family: 'Sansation Light', serif;
  background: #fdfde3;
  border: 2px solid black;
  border-radius: 20px;
}

.card {
  font-family: 'Sansation Light', serif;
  background: #fdfde3;
  border: 2px solid black;
  border-radius: 20px;
}

.user-card {
  display: flex;
  position: relative;
  align-items: flex-start;
  gap: 20px;
  font-size: 14px;
}

.grad-info {
  font-size: 17px;
  font-family: 'Sansation Light', serif;
  font-style: italic;
  margin-top: -5px;
}

.review-card {
  display: flex;
  flex-direction: column;
  background: #fdfde3;
  border: 2px solid black;
  border-radius: 20px;
  padding: 16px;
  margin-bottom: 20px;
  font-family: 'Victor Mono', serif;
}

.review-left {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.listing-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review-stars {
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.review-content-wrapper {
  margin-top: 10px;
}

.review-content {
  font-size: 16px;
  color: #444;
}

.review-date {
  margin-top: 8px;
  font-size: 14px;
  color: #777;
  font-style: italic;
}

.star-icon {
  width: 24px;
  height: 24px;
  margin-right: 3px;
}

.listing-title {
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 5px;
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

.review-date{
  font-family: 'Sansation Light', serif;
  width: fit-content;
  font-size: 13px;
  letter-spacing: normal;
  word-spacing: normal;
  margin-top: -5px;
  /*border: 2px dashed orangered;*/
}

.avatar {
  object-fit: cover;
  width: 120px;
  aspect-ratio: 1 / 1;
  border: 1px solid black;
  border-radius: 20px;
}

.info h2 {
  margin-bottom: 5px;
  font-family: 'Sansation Light', serif;
  font-size: 28px;
}

.card h3{
  margin-left: 20px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.tag{
  cursor: default;
}

.tag.active {
  font-family: 'Sansation Bold', serif;
  border: 2px solid black;
  box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.pen-icon {
  width: 30px;
  margin-top: -10px;
  margin-left: 10px;
  cursor: pointer;
}

.pen-icon-grad {
  width: 30px;
  margin-top: -5px;
  margin-left: 10px;
  display: inline-block;
  vertical-align: middle;
  cursor: pointer;
}

.form-popup {
  position: absolute;
  width: 100px;
  height: auto;
  top: 180px;
  left: 50%;
  padding: 20px;
  margin-top: 20px;
  background: #f9fdad;
  border: 2px solid black;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transform: translateX(-50%);
}

.save-icon{
  width: 40px;
  margin-left: 15px;
  cursor: pointer;
}

.no-recommendations, .no-favourites, .no-reviews {
  font-family: 'Victor Mono', serif;
  font-size: 16px;
  margin: 20px;
  color: #555;
  opacity: 0.8;
}

.grad-wrapper {
  display: flex;
  width: 655px;
  align-items: center;
  justify-content: center;
  background: #fdfdba;
  border: 2px solid black;
  border-radius: 25px;
}

.grad-input {
  font-family: 'Sansation Light', serif;
  text-align: center;
  width: 160px;
  height: 8px;
  padding: 20px 20px;
  margin: 20px 10px;
  border: 1px solid black;
  border-radius: 50px;
  background: #fdfde3;
  font-style: italic;
  font-size: 15px;
  box-sizing: border-box;
}

.dot {
  font-size: 24px;
  margin: 0 5px;
}

.user-review-card {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px 20px;
  margin: 15px 0;
  border: 1.5px solid black;
  border-radius: 25px;
  background-color: #fdfde3;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
  font-family: 'Sansation Light', serif;
}

.user-review-left {
  max-width: 72%;
}

.user-review-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: space-between;
  min-width: 130px;
}

.spot-name {
  font-family: 'Rubik One', sans-serif;
  font-size: 18px;
  margin-bottom: 5px;
}

.review-text {
  font-family: 'Sansation Light', serif;
  font-size: 16.5px;
  letter-spacing: 0.5px;
  word-spacing: 1px;
  color: #444;
  line-height: 1.5;
}


.review-date {
  font-family: 'Sansation Light', serif;
  font-size: 13px;
  color: #777;
  font-style: italic;
  margin-top: 4px;
}


.stars {
  display: flex;
  margin-bottom: 6px;
}

.star-icon {
  width: 20px;
  height: 20px;
  margin-left: 2px;
}
.fav-image {
  width: 100px;
  height: 80px;
  object-fit: cover;
  border-radius: 12px;
  border: 1px solid black;
  margin-right: 10px;
}

</style>