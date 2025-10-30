# User Profile Management System (Django)

A simple user profile management system built with Django. Features:

- User registration with validation (unique username and email, password confirmation)
- Profile view for any user at `/profile/<username>/`
- Edit profile (bio, birth date, location, avatar upload with 2MB limit)
- Change password (validates current password, password strength, different from current)
- Delete account (with confirmation and logout)
- Social authentication integration (django-allauth) with Bootstrap-styled account pages

## Project structure

- Single active templates folder: `templates/`
  - App pages: `templates/user_profile/*`
  - Allauth overrides: `templates/account/*`
- Old app-level templates were backed up to `templates_backup/user_profile/` and are not used.

## Setup (macOS/zsh)

```zsh
# 1) Create/activate virtual env (if you don't have one)
python3 -m venv .venv
source .venv/bin/activate

# 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3) Apply migrations
python3 manage.py migrate

# 4) Run server
python3 manage.py runserver
```

Optional:
```zsh
# Create admin user
python3 manage.py createsuperuser
```

## Pages

- `/register/` — registration
- `/profile/<username>/` — profile view
- `/profile/edit/` — edit profile
- `/profile/change-password/` — change password
- `/profile/delete/` — delete account
- `/accounts/login/`, `/accounts/signup/`, `/accounts/email/` — allauth pages (overridden)

## Media files

- Uploaded avatars are served in development via `MEDIA_URL=/media/` and stored in `media/`.

## Social auth (django-allauth)

- Providers included: Google, Facebook (see `settings.py`).
- To enable fully, add Social Applications in the Django admin with your client ID/secret and link them to `SITE_ID=1`.

## Notes

- Only project-level templates are active (see `user_profile_management_system/settings.py`, `TEMPLATES` with `APP_DIRS=False`).
- If you want to completely remove the old app-level templates, delete the folder `user_profile/templates/user_profile/` (a backup is in `templates_backup/user_profile/`).
