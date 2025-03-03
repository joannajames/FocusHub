<template>
  <router-view/>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App'
});
</script>

<style>
@import '@fontsource/rubik-doodle-shadow';

body {
  background: #fdfde3;
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  box-sizing: border-box;
}
</style>
