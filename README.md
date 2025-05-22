# 📝 Lead Management Application

This is a Django REST Framework-based backend system that allows public users (prospects) to submit their contact details and resumes. Internally, attorneys can review and track leads through an authenticated API. The application also sends automated email notifications to both the prospect and the assigned attorney upon submission.

---

## 🚀 Features

- ✅ Public API to create a new lead (`first_name`, `last_name`, `email`, `resume`)
- ✅ Resume upload support (`.pdf`, `.docx`, etc.)
- ✅ Emails sent to:
  - The **prospect** (confirmation)
  - The **attorney** (lead notification with resume attached)
- ✅ Internal API (with auth) to:
  - List all leads
  - View single lead
  - Manually mark a lead as **REACHED_OUT** (with timestamp update)
- ✅ Swagger UI documentation
- ✅ Redoc documentation
- ✅ PostgreSQL database support

---

## 📁 Tech Stack

- Python 3.10+
- Django 4+
- Django REST Framework
- PostgreSQL
- Swagger (drf-yasg)
- Docker (optional)

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/xaydarovmaqsud/leads_project
cd leads_project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Set up environment variables
Rename the `.env.example` file to `.env` and adjust the keys inside to your own. Create a database in **PostgreSQL** and specify the settings in `.env`
### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```
### 7. Run the server

```bash
python manage.py runserver
```
### 8. Access the API
http://127.0.0.1:8000/swagger/
