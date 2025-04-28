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
                        class="image"
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
                      class="listing-box"
                  >
                    <p class="listing-title">{{ review.content }}</p>
                    <div class="stars">
                      <img
                          v-for="(icon, index) in getStarIcons(review.rating)"
                          :key="index"
                          :src="icon"
                          class="star-icon"
                          alt="rating star"
                      />
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
import { favouriteListings } from '@/store/favourites';
import '@/assets/global.css';
import {attributeTags, tagColors} from "@/constants/Tags";

import {signOut} from "firebase/auth";
import {auth} from "@/firebase";
import {loginWithGoogle} from "@/services/authService";
import { useAuthStatus } from '@/store/authStatus';
import router from "@/router";

const { isLoggedIn, setLoggedIn } = useAuthStatus();
const showDropdown = ref(false);
const showForm = ref(false);
const selectedTags = ref(JSON.parse(localStorage.getItem('selectedTags') || '[]'));
const studyPreferences = attributeTags;
const tagClasses = tagColors;
const favouriteSpots = favouriteListings;
const username = ref(localStorage.getItem('username') || 'Name');
const userId = localStorage.getItem('userId') || '';
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

const submitForm = () => {
  console.log('Selected tag:', selectedTags);
  showForm.value = false;
};

const navigateTo = (path) => {
  window.location.href = path;
  showDropdown.value = false;
};

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

onMounted(async () => {
  const storedUsername = localStorage.getItem('username')?.trim();
  if (!storedUsername) {
    console.error('No username found in localStorage');
    return;
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/users');
    const usersData = await res.json();
    const users = usersData.data;

    const matchedUser = users.find(user => user.user_name === storedUsername);

    if (matchedUser) {
      username.value = matchedUser.user_name;
      academicLevel.value = matchedUser.academic_level || '';
      college.value = matchedUser.bu_college || '';
      degree.value = matchedUser.degree || '';
    } else {
      console.error(`No matching user found for username: ${storedUsername}`);
    }
  } catch (err) {
    console.error('Failed to fetch user details:', err);
  }

  try {
    const spotsRes = await fetch('http://127.0.0.1:8000/study_spots');
    const spotsData = await spotsRes.json();
    localStorage.setItem('allListings', JSON.stringify(spotsData.data));
  } catch (error) {
    console.error('Failed to fetch all listings:', error);
  }

  const allReviews = JSON.parse(localStorage.getItem('allReviews') || '[]');
  myReviews.value = allReviews.filter(review => review.userId === userId);

  const favourites = JSON.parse(localStorage.getItem('favourites') || '[]');
  const allListings = JSON.parse(localStorage.getItem('allListings') || '[]');
  favouriteSpots.value = allListings.filter(listing => favourites.includes(listing.id));
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

</style>
