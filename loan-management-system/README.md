# Loan Management System

A Django-based web application for managing loans, users, and installments. This project provides a robust platform for tracking loans, repayments, and user accounts with
multi-language support and a modern Dockerized deployment setup.

![Screenshot](screenshots/screenshot-1-min.png)

---

## Features

- User authentication and custom user model (email-based login)
- Loan creation, management, and tracking
- Installment calculation and payment tracking
- Multi-language support (English, Persian, Arabic)
- Admin dashboard for managing users, loans, and payments
- Contact form and static informational pages (About, Privacy)
- Jalali date support for Persian users
- Responsive UI (Django templates)
- Logging and error handling
- Dockerized for easy deployment
- Nginx reverse proxy configuration

## Technology Stack

- **Backend:** Django 5.0
- **Database:** PostgreSQL (default), SQLite (for development)
- **Frontend:** Django Templates, HTML5, CSS3
- **Containerization:** Docker, Docker Compose
- **Web Server:** Gunicorn, Nginx
- **Other Libraries:**
    - django-phonenumber-field
    - django-rosetta (translation)
    - jdatetime, jalali_core (Jalali date support)
    - psycopg2 (PostgreSQL driver)
    - python-dotenv (env management)
    - redis (optional, for caching)

## Requirements

- Docker & Docker Compose (recommended)
- Or, for manual setup:
    - Python 3.10+
    - PostgreSQL (or SQLite for development)
    - pip (Python package manager)

## Quick Start (with Docker)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/masoudkaarimi/django-mini-projects/tree/master/loan-management-system
   cd loan-management-system
   ```
2. **Configure environment variables:**
    - Copy `.env.example` to `.env` and set your secrets (DB, Django, etc).
3. **Build and run the containers:**
   ```bash
   docker compose up --build
   ```
4. **Access the app:**
    - Web: http://localhost:8000
    - Admin: http://localhost:8000/admin/

## Manual Setup (without Docker)

1. Create and activate a virtual environment:
   ```bash
   cd src
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   cd src
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set your secrets (DB, Django, etc).
4. Run migrations, create a superuser, and load initial data:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py load_data   
    ```
5. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Docker Compose Services

- **django:** Main application (Gunicorn)
- **postgres:** Database
- **nginx:** Reverse proxy
- **redis:** (optional, for caching)

## Screenshots

See the [`screenshots/`](screenshots/) directory for UI examples.

## License

This project is licensed under the MIT License.

