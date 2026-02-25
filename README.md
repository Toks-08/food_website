# Chuks Kitchen Backend API

A robust Django-based backend for a food delivery and kitchen management system. This project features custom user authentication, an OTP (One-Time Password) verification system, and a referral program.



## Technical Stack
* **Framework:** Django 4.2+
* **API:** Django REST Framework (DRF)
* **Authentication:** Token-based Authentication
* **Database:** SQLite (Development)

##  Features
* **Custom User Model:** Login via `email` instead of `username`.
* **OTP Verification:** Automatic 6-digit code generation upon registration.
* **Role-Based Access:** Distinguish between Customers, Kitchen Staff, Managers, and Riders.
* **Referral System:** Automated unique referral code generation for every new user.

---

## Setup and Installation

### 1. Clone and Environment
```bash
# Clone the repository
git clone <your-repo-url>

# Navigate to project
cd chuks_kitchen

# Activate your virtual environment
source tenv/bin/activate  # Mac/Linux
# tenv\Scripts\activate   # Windows

2. Database Initialization
Ensure your models are synced with the database:

Bash
python manage.py makemigrations accounts
python manage.py migrate

3. Create Admin Access
Because the system uses an OTP flow, manually create a superuser to access the admin dashboard:

Gemini said
It looks like the formatting got scrambled when it was pasted. For a README.md file to look professional on GitHub or in VS Code, it needs specific Markdown symbols (like # for headers and triple backticks for code blocks).

Here is the clean, copy-paste ready version.

How to use this:
Create a file named README.md in your main chuks_kitchen folder.

Open it in VS Code.

Paste the text below exactly as it is.

Markdown
# 🥘 Chuks Kitchen Backend API

A robust Django-based backend for a food delivery and kitchen management system. This project features custom user authentication, an OTP (One-Time Password) verification system, and a referral program.



## 🚀 Technical Stack
* **Framework:** Django 4.2+
* **API:** Django REST Framework (DRF)
* **Authentication:** Token-based Authentication
* **Database:** SQLite (Development)

## 🛠 Features
* **Custom User Model:** Login via `email` instead of `username`.
* **OTP Verification:** Automatic 6-digit code generation upon registration.
* **Role-Based Access:** Distinguish between Customers, Kitchen Staff, Managers, and Riders.
* **Referral System:** Automated unique referral code generation for every new user.

---

## 🏗 Setup and Installation

### 1. Clone and Environment
```bash
# Clone the repository
git clone <your-repo-url>

# Navigate to project
cd chuks_kitchen

# Activate your virtual environment
source tenv/bin/activate  # Mac/Linux
# tenv\Scripts\activate   # Windows
2. Database Initialization
Ensure your models are synced with the database:

Bash
python manage.py makemigrations accounts
python manage.py migrate

3. Create Admin Access
Because the system uses an OTP flow, manually create a superuser to access the admin dashboard:
python manage.py createsuperuser

4. Run the Server
Bash
python manage.py runserver

Endpoint,Method,Description

api/auth//signup/ ,POST ,Register user & generate OTP
api/auth/verify/ ,POST, Activate account using 6-digit code
api/auth/login/ ,POST ,Authenticate and obtain Auth Token
/admin/ ,GET, Django Admin Dashboard