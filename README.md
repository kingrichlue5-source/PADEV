# PADEV

PADEV is a Django content management website for Partners in Development.

## Local development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the public site and `/admin/` for the CMS.

## Railway deployment

1. Create a Railway project and attach a PostgreSQL database.
2. Connect the GitHub repository.
3. Add `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`, `DJANGO_ALLOWED_HOSTS`, and `DJANGO_CSRF_TRUSTED_ORIGINS`.
4. Add the Cloudinary `CLOUDINARY_URL` variable, or add `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET`.
5. Railway uses `Procfile` and `start.sh` to migrate the database, collect static files, and start Gunicorn.
6. Create a Django admin user with `railway run python manage.py createsuperuser` or through the Railway shell.

Never commit `.env`, database files, Cloudinary credentials, or Django secret keys.