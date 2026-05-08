# INFO3180 Final Project – JamDate

## Group Members
1. Kyle Peart
2. Raheem Williams
3. Kyval Waysome
4. Daniel Coore
5. Kamal McMillan

---

# Project Description

JamDate is a matchmaking and social interaction web application built using Vue.js on the frontend and Flask on the backend. 

The application allows users to:
- Register and authenticate securely
- Create detailed dating profiles
- Upload profile photos
- Add personal interests and preferences
- Search and filter profiles
- Favourite users
- View compatible matches
- Send and receive messages in real time-like conversations

The system uses a compatibility-based matching algorithm that compares shared profile characteristics and interests.

---

# Technologies Used

## Frontend
- Vue 3
- Vue Router
- Vite
- JavaScript
- CSS

## Backend
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Flask-Migrate
- SQLAlchemy
- SQLite

---

# Features Implemented

## Authentication
- User Registration
- User Login
- JWT Authentication
- Secure Password Hashing
- Logout Functionality

## Profiles
- Profile Creation
- Profile Retrieval
- Profile Image Uploads
- Biography and Preference Storage

## Interests System
- Many-to-Many Interest Relationships
- Shared Interest Matching
- Dynamic Interest Creation

## Matching System
- Compatibility Matching
- Shared Interest Scoring
- Favourite Users
- Match Recommendations

## Search and Filtering
- Search by Name
- Search by Gender/Sex
- Search by Race
- Search by Birth Year
- Sorting by:
  - Name
  - Parish
  - Age

## Messaging System
- Send Messages
- Retrieve Conversations
- Message Persistence
- Timestamped Messages

---

# Project Structure

```text
info3180-project/
│
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── uploads/
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md