# SecureTix - Secure Concert Booking System

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-6.0.6-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![OWASP](https://img.shields.io/badge/OWASP-Compliant-red)

A secure web application for booking concert tickets and managing live events, built with **Django 6.0.6** and designed to satisfy strict **OWASP Top 10** security requirements for the IKB21503 Mini Project.

---

## Table of Contents

1. [Project Description](#1-project-description)
2. [Repository Structure](#2-repository-structure)
3. [Security Features](#3-security-features)
4. [Installation Steps](#4-installation-steps)
5. [How to Run the App](#5-how-to-run-the-app)
6. [Dependencies](#6-dependencies)
7. [Screenshots](#7-screenshots)

---

## 1. Project Description

**SecureTix** is a role-based concert ticket booking platform where:

- **Admin users** manage events (create, edit, delete concerts and posters) and review system audit logs.
- **Normal users** register, log in, browse available concerts, securely book tickets, and manage their personal booking history.

Every layer of the application is built with security in mind - from the file upload validation down to the UUID database models.

### Key Modules

| Module | Description |
|---|---|
| `core` | Project configuration, environment variable management, and ASGI/WSGI setup. |
| `tickets` | Core application handling Concerts, Bookings, and Audit Logging. |
| `accounts` | Registration, login, logout, and profile tracking (integrated into tickets app). |
| `admin` | Secure dashboard for managing database records and tracking security logs. |

---

## 2. Repository Structure

    SecureTix/
    ├── docs/
    │   └── screenshots/            # Application screenshots
    │       ├── admin.png
    │       ├── concert_detail.png
    │       ├── homepage.png
    │       ├── login.png
    │       ├── profile.png
    │       └── register.png
    ├── src/
    │   ├── core/                   # Project settings & routing
    │   │   ├── settings.py         # Environment-based configuration
    │   │   ├── urls.py             # Root URL dispatcher
    │   │   ├── asgi.py             # ASGI entry point
    │   │   └── wsgi.py             # WSGI entry point
    │   ├── tickets/                # Main application
    │   │   ├── migrations/         # Database migration files
    │   │   ├── admin.py            # Admin dashboard configuration
    │   │   ├── apps.py             # App configuration
    │   │   ├── forms.py            # User registration & edit forms
    │   │   ├── models.py           # Concert, Booking, AuditLog models
    │   │   ├── urls.py             # URL routing for tickets app
    │   │   └── views.py            # Business logic & security checks
    │   ├── templates/              # HTML templates
    │   │   ├── base.html           # Master layout with Tailwind & nav
    │   │   ├── index.html          # Concert listing (homepage)
    │   │   ├── concert_detail.html # Concert info & booking page
    │   │   ├── login.html          # Secure login form
    │   │   ├── register.html       # Secure registration form
    │   │   ├── profile.html        # User profile & ticket history
    │   │   └── receipt.html        # Booking receipt
    │   ├── posters/                # Uploaded concert poster images
    │   ├── manage.py               # Django management script
    │   └── db.sqlite3              # SQLite database (local dev)
    ├── .env.example                # Environment variable template
    ├── .gitignore                  # Git ignore rules
    ├── requirements.txt            # Python dependencies
    └── README.md                   # Project documentation

---

## 3. Security Features

* **IDOR Prevention:** Uses `UUIDField` instead of sequential integers for database models, preventing attackers from guessing ticket IDs.
* **File Upload Security:** Custom validation on Concert posters limits file size (max 5MB) and restricts extensions (`.jpg`, `.jpeg`, `.png`) to prevent RCE attacks.
* **Audit Logging:** Automatically logs critical actions (e.g., ticket booking) with Timestamp, Action, User, and IP Address (`REMOTE_ADDR`).
* **Access Control:** Enforces strict Role-Based Access Control (RBAC) using `@login_required` to protect sensitive views.
* **CSRF Protection:** All state-changing HTML forms require Django's `{% csrf_token %}` to prevent Cross-Site Request Forgery.
* **Environment Security:** Utilizes `django-environ` to keep `SECRET_KEY` and `DEBUG` variables out of version control.
* **Injection-Free:** Built heavily upon Django's ORM and parameterized queries to block SQL Injection.

---

## 4. Installation Steps

### Prerequisites
* Python 3.10+
* Git

### Step 1: Clone the repository
    git clone [https://github.com/your-username/securetix.git](https://github.com/your-username/securetix.git)
    cd securetix

### Step 2: Create and activate a virtual environment
    python -m venv venv

    # On Windows:
    venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate

### Step 3: Install Dependencies
    pip install -r requirements.txt

---

## 5. How to Run the App

### Step 1: Environment Variables
Create a file named `.env` inside the `src` directory and add your secrets:

    DEBUG=True
    SECRET_KEY=your-secure-random-secret-key-here

### Step 2: Apply Migrations
Initialize the SQLite3 database and create the tables:

    cd src
    python manage.py migrate

### Step 3: Create an Admin Account
Set up your superuser to access the admin dashboard:

    python manage.py createsuperuser

### Step 4: Run the Server

    python manage.py runserver

Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 6. Dependencies

| Package | Version | Purpose |
|---|---|---|
| Django | 6.0.6 | Core Web framework |
| django-environ | 0.11.2 | `.env` secrets management |
| tzdata | 2026.2 | Timezone data |
| Tailwind CSS | CDN | Frontend styling (loaded via standard script tag) |

*Install all Python dependencies with:*

    pip install django django-environ

---

## 7. Screenshots

### Homepage — Upcoming Concerts
![Homepage](docs/screenshots/homepage.png)

### Login Page
![Login](docs/screenshots/login.png)

### Registration Page
![Register](docs/screenshots/register.png)

### Concert Detail & Booking
![Concert Detail](docs/screenshots/concert_detail.png)

### User Profile & Ticket History
![Profile](docs/screenshots/profile.png)

### Admin Dashboard
![Admin Dashboard](docs/screenshots/admin.png)
