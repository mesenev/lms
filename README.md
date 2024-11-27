![develop branch current status](https://bb.mesenev.ru/plugins/badges/lmsci.svg)

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
docker compose up database
```

Postgres should create default database during the initial launch
with use `.docker/conf/common.env` variables.

In case if it's not created automatically for some reason
then read logs and create it manually
using any approach that's suits for you (pgAdmin, pycharm, terminal).

When it's done you should apply migrations

```shell
docker compose run backend python manage.py migrate
```
```shell
docker compose run backend python manage.py createsuperuser
```

You are ready to launch composition
```shell
docker compose up
```

Don't forget to add superuser to 'teacher' group in admin-panel.

You can run tests with
```shell
docker compose exec backend python manage.py test
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
