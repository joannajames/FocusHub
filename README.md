# FocusHub

FocusHub is a student-built web application designed to help both ourselves and our peers locate the most optimal study spaces on campus for a range of individual needs and ultimately augment productivity.
Inspired by the principle of crowdsourcing, much like platforms such as Reddit and TripAdvisor, FocusHub relies on user-generated content-ratings to build a trustworthy, community-curated archive of study spaces.
Its content is regulated by its community: each user is able to flag inappropriate reviews, and to ensure authenticity, every user is limited to one review per study spot (or possibly one per time interval in future iterations). 
Users can browse listings, read and leave star-rated reviews, filter spaces by key features (e.g. outlet availability, food options, seat capacity), and save their favourites. FocusHub also recommends study spaces to users according to preferences configured in the user’s profile — making the experience both personal and purposeful.

## Features

- **Study space discovery** with descriptive filters and smart suggestions
- **Preference-based recommendations** powered by user profile attributes
- **Crowdsourced reviews & tagging**, with quality regulated through flagging
- **Favourites system** for quick access to saved locations
- **One-review-per-user** mechanism to preserve authenticity
- **Secure login** using Google Authentication
- **Custom illustrations, and icons** to enhance visual identity

## Technologies Used

- **Frontend**: Vue.js 3  
- **Styling**: Tailored via `global.css` with custom fonts and icons  
- **Backend**: Python (FastAPI)  
- **Database**: MySQL  
- **Authentication**: Google OAuth 2.0  
- **Deployment**: Currently local; planned for cloud deployment via Google Cloud  
- **Version Control**: Git & GitHub  

## Project Structure (Simplified)

```
├── frontend/
│   ├── public/                 # Static files, images, and metadata
│   ├── filters/                # Vue components for filtering functionality
│   ├── icons/                  # Custom UI icons
│   ├── images/                 # User-selected and branded imagery
│   ├── src/
│   │   ├── assets/             # Global styles including global.css
│   │   ├── components/         # Vue pages e.g. Home, Reviews, Profile
│   │   └── App.vue             # Root Vue instance
│
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── models.py               # SQLAlchemy models for database tables
│   └── database.py             # DB connection setup and session management
│
├── Tags.js                     # Attribute and contact tag logic
├── README.md                   # Project overview and documentation
```

## Setup Instructions

### Local Development

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/focushub.git
   cd focushub
   ```

2. **Start frontend**
   ```bash
   cd frontend
   npm install
   npm run serve
   ```

3. **Start backend**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

4. Visit: [http://localhost:3000](http://localhost:3000)

## Future Potential

FocusHub has significant scope for future development:

- Location filtering to expand beyond campus spaces
- Live occupancy predictions to help students avoid overcrowded spots
- Study group connections — match students based on shared courses and study preferences
- Messaging features for students to communicate and coordinate sessions
- Business partnerships with local cafés or libraries, offering exclusive deals to FocusHub users
- Booking system for reservable spaces

## Contributors

- **Raeesa Dhoda** – UI/UX Design Lead & Frontend Development  
- **Joanna James** – Testing, Deployment & Backend Development
- **Christal Philip** – Database Architecture & Backend Integration
- **Zahra Al-Quraish** – Backend Development & Authentication Security  

## Learn More

Visit the in-app Constitution Page to discover FocusHub’s values, user expectations, and community vision.
