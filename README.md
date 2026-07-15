# Commerce – Online Auction Platform

This project is a full-stack online auction platform built with Django as part of the CS50 Web Programming course. I built it to understand how real web applications work by implementing user authentication, database relationships, and dynamic web pages.

## Features

- User registration, login, and authentication
- Create, edit, and manage auction listings
- Place bids with validation
- Comment system for each listing
- Personal watchlist
- Category-based browsing
- Responsive user interface using HTML and CSS

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- Django ORM

## What I Learned

This project helped me understand how different parts of a Django application work together.

- URL routing
- Views and request handling
- Django ORM
- Database relationships using ForeignKey and Many-to-Many
- Authentication and session management
- CRUD operations
- Template inheritance
- Form handling and validation

## Project Structure

```text
commerce/
├── auctions/
├── templates/
├── static/
├── manage.py
└── db.sqlite3
```

## Running the Project

```bash
python manage.py migrate
python manage.py runserver
```

Then open:

```
http://127.0.0.1:8000/
```

## About

This is one of the projects I'm most proud of because it was the first time I built a complete database-driven web application. It helped me move beyond simple websites and understand how authentication, database design, business logic, and templates come together to build a real full-stack application.
