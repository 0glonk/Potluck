# Potluck — Recipe Sharing Platform

A recipe-sharing social platform built with Django. Users create accounts, publish recipes with images, like and bookmark recipes, and search for recipes and other users.

**Team capstone project**, College of DuPage, Spring 2025, designed and built over 16 weeks by a four-person team: Mike Adams, Ece Basar, Mayah K, and Daniel Nguyen. The original team repository is private; this is my copy of our project, published for portfolio purposes.

## Features

- User accounts with multiple permission levels and a custom email-based login
- Email confirmation required to activate new accounts
- Password reset via emailed token
- Create and share recipes with images and a variable number of ingredient and instruction fields
- Built-in image cropping tool for recipe photos
- Likes and bookmarks, with like counts tracked per recipe
- Personal views for your uploaded recipes and your bookmarked recipes
- Search for both users and recipes
- Random recipe selection populating the home page carousel and grid
- Responsive Bootstrap 5 layout with dynamically rendered navigation and footer

## Tech stack

- Python, Django 5.1
- SQLite for local development
- Media storage configured for AWS S3 (django-storages + boto3, see `home/aws_settings_template.py`)
- Bootstrap 5 and jQuery on the front end
- SMTP email for account verification and password reset

## Run it locally

Create and activate a virtual environment:

```
py -m venv .venv
.venv\Scripts\activate.bat
```

(Mac: `python -m venv .venv` then `source .venv/bin/activate`)

Install dependencies and start the server:

```
pip install -r requirements.txt
py manage.py runserver
```

The site runs on port 8000.

## Notes on this copy

- The original `SECRET_KEY` and the email app password were removed from `potluckSite/settings.py` before publishing. Generate your own secret key and set your own email credentials to enable the email features.
- This was the team's first Django project, built for a class. As the original README put it, it is a learning project and is not recommended for production use.

## About

Ece Basar — B.S. Computer Science candidate, Lewis University (expected May 2027). See also my Home Care Operations Dashboard project (PostgreSQL + Power BI) on this profile.
