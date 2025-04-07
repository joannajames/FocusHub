import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import AccountPage from '@/components/AccountPage.vue';
import ReviewsPagePage from '@/components/ReviewsPage.vue';
import TheHubPagePage from '@/components/TheHubPage.vue';
import ContactUsPage from '@/components/ContactUsPage.vue';

const routes = [
  { path: '/', component: HomePage },
  { path: '/account', component: AccountPage },
  { path: '/reviews/:id', name: 'reviews', component: ReviewsPagePage },
  { path: '/the_hub', component: TheHubPagePage },
  { path: '/contact_us', component: ContactUsPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
