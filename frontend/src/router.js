import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import UserProfile from '@/components/UserProfile.vue';
import DynamicReviews from '@/components/DynamicReviews.vue';
import TheHub from '@/components/TheHub.vue';
import ChatToUs from '@/components/ChatToUs.vue';
import OurConstitution from "@/components/OurConstitution.vue";
import NotVisible from "@/components/NotVisible.vue";

const routes = [
  { path: '/', component: HomePage },
  { path: '/profile', component: UserProfile },
  { path: '/reviews/:id', component: DynamicReviews },
  { path: '/the_hub', component: TheHub },
  { path: '/chat_to_us', component: ChatToUs },
  { path: '/our_constitution', component: OurConstitution },
  { path: '/unavailable', component: NotVisible }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
