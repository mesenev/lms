We are strongly advice you to use pycharm during development process.

Create a file `imcslms/settings.py` with content:

```from imcslms.default_settings import *```

You may want to define following variables as well
```python
CATS_URL = '<cats-url>'
CATS_LOGIN = '<your-cats-account>'
CATS_PASSWD = '<your-cats-password>'
```
#### database
Create database inside the composition.

Launch the database container:
```shell
docker compose -f .docker/docker-compose.yml up database
```

Postgres should create default database during the initial launch
with use `.docker/conf/common.env` variables.

In case if it's not created automatically for some reason
then read logs and create it manually
using any approach that's suits for you (pgAdmin, pycharm, terminal).

When it's done backend should start without errors:

```shell
docker compose -f .docker/docker-compose.yml up backend
```


#### migrations
Apply migrations and create superuser
```shell
docker compose -f .docker/docker-compose.yml exec backend python manage.py migrate
docker compose -f .docker/docker-compose.yml exec backend python manage.py createsuperuser
```
Add superuser to 'teacher' group in admin-panel.

You are ready to launch composition
```shell
docker compose -f .docker/docker-compose.yml up
```

#### frontend
Install Node.js & install frontend dependencies via command
```shell
npm install
```
Now you should be able to run frontend application
```shell
npm run serve
```
