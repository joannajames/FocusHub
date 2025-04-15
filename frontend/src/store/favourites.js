import { ref, computed, watch } from 'vue';

// 1. FAVOURITES - persisted set
const storedFavourites = JSON.parse(localStorage.getItem('favourites') || '[]');
export const favourites = ref(new Set(storedFavourites));

watch(favourites, (newVal) => {
  localStorage.setItem('favourites', JSON.stringify([...newVal]));
}, { deep: true });

// 2. TOGGLE AND CHECK
export const toggleFavourite = (id) => {
  if (favourites.value.has(id)) {
    favourites.value.delete(id);
  } else {
    favourites.value.add(id);
  }
};

export const isFavourited = (id) => favourites.value.has(id);

// 3. ALL LISTINGS - globally shared (populated on fetch in TheHub.vue)
export const allListings = ref([]);

// 4. FAVOURITE LISTINGS - computed, reactive
export const favouriteListings = computed(() =>
  allListings.value.filter(listing => favourites.value.has(listing.id))
);
