<template>
  <div class="page-frame">
    <div class="container">
      <header class="header">
          <div class="nav-container">
          <img src="/icons/Menu_Burger.png" alt="Menu" class="menu-icon" @click="toggleDropdown"/>
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

      <div class="left-margin">
        <br>
        <br>
        <h1 class="title">our constitution</h1>

        <div class="main-content">
          <h2 class="opener">we've already met.</h2>
          <h2 class="opener">but now we've gotta set some boundaries...</h2>
          <br>
          <div class="rule-line orange">
            <div class="rule-label">#1:</div>
            <p> Only Boston University students and faculty can participate. A drag, we knooow. But we’re
              small-scale, college-focused and we really really value the privacy of our users.
              (Feel free to try to change our minds tho).
            </p>
          </div>

          <div class="rule-line green">
            <div class="rule-label">#2:</div>
            <p>
              Here’s an easy one. Be RESPECTFUL and be TRUTHFUL. Simple as.
              Or we’ll revoke your account. Yes, that WAS a threat.
            </p>
          </div>

          <div class="rule-line blue">
            <div class="rule-label">#3:</div>
            <p> For the sake of authenticity and restraining 'scorned' customers, we’re restricting posts to one
              per study spot. If you’ve seriously changed your mind about a place, shoot us a request and we’ll
              help ya out.
            </p>
          </div>

          <div class="rule-line pink">
            <div class="rule-label">#4:</div>
            <p>
              Honestly guys, we’re just 4 people. And we can’t screen every review by ourselves. So help us to do
              so! This is a community: engage with one another, flag posts for inaccuracy and save spots for that
              next study sesh of yours.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

import '@/assets/global.css';
import {ref} from "vue";

const showDropdown = ref(false);

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const navigateTo = (path) => {
  window.location.href = path;
  showDropdown.value = false; // hide after click
};

</script>

<style>

.opener {
  margin-top: -10px;
  font-family: 'Sansation Light', serif;
  font-size: 27px;
}

.rule-line {
  display: flex;
  gap: 30px; /* adds a little space between h3 and p */
  border: 2px solid black;
  border-radius: 50px;
  padding: 5px 20px;
}

.rule-line + .rule-line {
  margin-top: 22px;
}

.rule-line.green .rule-label { background: #c5f3af; }
.rule-line.blue  .rule-label { background: #badafb; }
.rule-line.pink  .rule-label { background: #ffbbbc; }

.rule-label {
  align-content: center;
  margin-left: 15px;
  font-family: 'Rubik Doodle Shadow', serif;
  font-size: 40px;
}


.rule-line p {
  align-content: center;
  font-family: 'Sansation Light', serif;
  font-size: 18px;
  line-height: 1.5;
  word-spacing: 1px;
}

</style>