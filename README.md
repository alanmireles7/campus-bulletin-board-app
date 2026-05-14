# CampusNOW - Django Version

## Project Description
CampusNOW is a social-based web application that allows students to share
announcements and campus-related information. The app follows the CRUD model,
allowing users to create, read, update, and delete posts.

Students can use the platform to share study groups, housing notices, events,
clubs, campus activities, and general campus announcements.

## Team Members
- Alan Mireles
- Demetrio Villarreal
- Nedved Olivarez

## Objective
The objective of this project is to practice the Software Development Life
Cycle (SDLC), Agile methodology, version control with GitHub, and documentation.

---

## Project Overview
CampusNOW is a web-based bulletin board application designed specifically for
UTRGV students. The goal of the platform is to provide a centralized digital
space where students can post and view important campus-related information
such as study groups, housing opportunities, events, and student organizations.

## Problem Statement
UTRGV students often rely on multiple disconnected platforms such as social
media, group chats, or word of mouth to find information about events, housing,
and study groups. CampusNOW solves this problem by offering one centralized
platform where students can quickly create and view campus posts.

## Target Users
- UTRGV students
- Student organizations
- Study groups
- Students seeking housing or campus resources

---

## Tech Stack
- Python
- Django 6.0.5
- SQLite (via Django ORM)
- HTML/CSS
- Git / GitHub

## Agile Planning

### Sprint 1
- Create GitHub repository
- Set up development environment
- Write project description
- Create README file
- Define project scope

### Sprint 2
- Design UI prototype
- Define user stories
- Create home page
- Start user management

### Sprint 3
- Implement create and view posts
- Connect database

### Sprint 4
- Implement edit and delete posts
- User authentication system
- Testing and debugging
- Final documentation

---

## Functional Requirements
- View all campus posts on the homepage
- Filter posts by category (Study Groups, Events, Housing, Clubs, General)
- Create new posts (requires login)
- Categorize posts when creating
- View timestamps and post author on each post
- Edit your own posts (requires login)
- Delete your own posts (requires login)
- User registration with password validation
- User login and logout
- Posts are tied to the user who created them
- React to posts with emojis 👍❤️😂😮😢 (requires login)
- Reactions toggle on/off without page refresh
- Comment on posts (requires login)
- Delete your own comments (requires login)
- Comments shown in collapsible dropdown per post
- Page stays on current post after commenting, editing, or deleting

---

## Non-Functional Requirements
- Easy to use interface
- Fast loading
- Modern design
- Browser compatibility

---

## User Stories
- As a UTRGV student, I want to create a post so I can share information with others.
- As a UTRGV student, I want to view posts so I can stay updated on campus activities.
- As a UTRGV student, I want to filter posts by category so I can find relevant content faster.
- As a UTRGV student, I want to edit my post so I can correct or update information.
- As a UTRGV student, I want to delete my post so I can remove outdated information.
- As a UTRGV student, I want to categorize my post so others can easily find it.
- As a UTRGV student, I want to register an account so my posts are tied to my identity.
- As a UTRGV student, I want to login so I can manage my own posts securely.
- As a UTRGV student, I want to react to posts so I can engage with campus content.
- As a UTRGV student, I want to comment on posts so I can start conversations.
- As a UTRGV student, I want to delete my comments so I can remove things I posted.

---

## CRUD Features
- **Create** → Fill out form to post a campus announcement (login required)
- **Read** → Homepage displays all posts newest first, visible to everyone
- **Update** → Edit your own post's title, category, and content (login required)
- **Delete** → Remove your own post with confirmation prompt (login required)

---

## User Management System
CampusNOW includes a fully working user management system.

### Implemented Features
- User registration with password validation
- User login and logout
- Session-based authentication (Django built-in)
- Post ownership — users can only edit/delete their own posts
- Comment ownership — users can only delete their own comments
- Non-logged-in users are redirected to login if they try to create a post
- Each post displays the author's username and timestamp
- Reactions and comments require login

### Social Features
- Emoji reactions (👍❤️😂😮😢) with toggle on/off — no page refresh
- Collapsible comment sections per post
- Category filter bar to browse posts by topic
- Page anchors keep user in place after actions
---

## Home View
The home view displays:
- UTRGV logo and CampusNOW branding
- Login/Register buttons when logged out
- Username and Logout button when logged in
- Welcome section with Create Post button
- Recent posts with category badges, author, and timestamps
- Edit/Delete buttons only on posts you own

## Create Post Page
The create post page allows users to:
- Enter a post title
- Select a category
- Enter post content
- Submit a new post

---

## Admin Panel
Django's built-in admin panel is available at `http://localhost:8000/admin`
- Allows full database management without touching code
- Username: admin
- Password: password

---

## How to Run
1. Clone the repository

2. Navigate into the project folder

3. Make sure you are on the `main` branch

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Create migrations for the `board` app:

   ```bash
   python manage.py makemigrations board
   ```

6. Apply migrations:

   ```bash
   python manage.py migrate
   ```

7. Start the Django server:

   ```bash
   python manage.py runserver
   ```

8. Open the app in your browser:

   ```text
   http://127.0.0.1:8000/
   ```