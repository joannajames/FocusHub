// Study Spot Tags — used in TheHub, Profile, etc.
export const attributeTags = [
  'aesthetic',
  'bike parking',
  'BYOF',
  'car parking',
  'courtyard',
  'early hours',
  'H20 stations',
  'indie (non-chain)',
  'late hours',
  'low-light',
  'low-traffic',
  'pet friendly',
  'quiet',
  'smiley service',
  'student dealz',
  'vegans welcome',
];

// Contact Form Tags — used in ChatToUs.vue
export const contactTags = [
  'add a spot',
  'edit my review',
  'feedback for us',
  'login',
  'remove a spot',
  'report bug',
  'partnerships',
];

// Combined tag-colour mapping
export const tagColors = {
  'aesthetic': 'pink',
  'bike parking': 'orange',
  'BYOF': 'yellow',
  'car parking': 'green',
  'courtyard': 'blue',
  'early hours': 'pink',
  'H20 stations': 'orange',
  'indie (non-chain)': 'yellow',
  'late hours': 'green',
  'low-light': 'blue',
  'low-traffic': 'pink',
  'pet friendly': 'orange',
  'quiet': 'yellow',
  'smiley service': 'green',
  'student dealz': 'blue',
  'vegans welcome': 'pink',

  'add a spot': 'pink',
  'edit my review': 'orange',
  'feedback for us': 'green',
  'login': 'blue',
  'remove a spot': 'pink',
  'report bug': 'orange',
  'partnerships': 'green',
};

// Export a combined list
export const allTags = [...attributeTags, ...contactTags];