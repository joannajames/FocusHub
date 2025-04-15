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
              <a href="#" @click="navigateTo('/profile')">
                -&nbsp;&nbsp;&nbsp;profile
                <img src="/icons/Account.png" class="dropdown-icon" alt="Profile Icon" />
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
          <img src="/icons/Account.png" alt="Profile Icon" class="login-icon" @click="navigateTo('/profile')" />
          <img src="/icons/FocusHub_Logo.png" alt="FocusHub Logo" class="logo-icon" @click="navigateTo('/')" />
        </div>
      </header>

      <div class="main-content left-margin">
        <h1 class="title">profile</h1>

        <div class="card profile-card user-card">
          <img src="/images/Anastasia.jpg" alt="Anastasia" class="avatar" />
          <div class="info">
            <h2>
              Anastasia
            </h2>
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
              </div>
            </div>

            <div class="card">
              <h3>my reviews:</h3>
            </div>
          </div>

          <div class="right">
            <div class="card">
              <h3>recommended spots:</h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, watch} from 'vue';
import '@/assets/global.css';
import {attributeTags, tagColors} from "@/constants/Tags";

const showDropdown = ref(false);
const showForm = ref(false);
const selectedTags = ref(JSON.parse(localStorage.getItem('selectedTags') || '[]'));
const studyPreferences = attributeTags;
const tagClasses = tagColors;

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

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
  cursor: pointer;
}

.tag.active {
  font-family: 'Sansation Bold', serif;
  border: 2px solid black;
  box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.pen-icon {
  width: 35px;
  height: 35px;
  margin-top: -10px;
  margin-left: 5px;
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
  margin-right: -5px;
  cursor: pointer;
}

</style>
