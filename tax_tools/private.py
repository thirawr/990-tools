import os
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.parse(os.getenv('TAX_TOOLS_DB_URL')),
    '990s': dj_database_url.parse(os.getenv('TAX_RETURN_DB_URL'))
}
