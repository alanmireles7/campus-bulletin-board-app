# CampusNOW - Django Version

## About This Branch
This branch contains a Django implementation of CampusNOW, built as part of
the Software Engineering final project for UTRGV Spring 2026.
The `django-nedved` branch explores Django as an alternative to the team's
original Flask implementation.

## Team Members
- Alan Mireles
- Demetrio Villarreal
- Nedved Olivarez

## What's in This Branch
- Full Django project setup with virtual environment
- Post model with database migrations
- Complete CRUD: Create, Read, Update, Delete posts
- Django admin panel integration
- URL routing and views
- HTML templates with UTRGV orange branding

## Tech Stack
- Python
- Django 6.0.5
- SQLite (via Django ORM)
- HTML/CSS

## How to Run
1. Navigate to the project folder
2. Activate virtual environment:
   - Windows: `virt\Scripts\activate`
3. Install dependencies: `pip install django`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`
6. Open: `http://localhost:8000`

## CRUD Features
- **Create** → Fill out form to post a campus announcement
- **Read** → Homepage displays all posts newest first
- **Update** → Edit any post's title, category, and content
- **Delete** → Remove a post with confirmation prompt

## Admin Panel
Access Django's built-in admin at `http://localhost:8000/admin`
- Username: admin
- Password: password