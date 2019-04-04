# 990 Tools

## Production Deployment
From project root:
1. Install dependencies
```sh
pip install -r requirements.txt
```
2. Migrate database models
```sh
./bin/migrate.sh
```
3. Collect static files
```sh
python manage.py collectstatic
```
4. Run webserver
```sh
./bin/gunicorn_start.sh
```
