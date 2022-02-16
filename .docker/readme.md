Building composition {dev/prod}
```shell
docker-compose -f .docker/docker-compose{/.prod}.yml build
```
Launching built composition
```shell
docker-compose -f .docker/docker-compose{/.prod}.yml up
```
Executing a command inside specific container
```shell
docker-compose -f .docker/docker-compose{/.prod}.yml exec backend python manage.py shell
```
Getting inside the database shell
```shell
docker-compose -f .docker/docker-compose{/.prod}.yml exec database psql -U dbuser
```
Gracefully stop composition [or container_name]
```shell
docker-compose -f .docker/docker-compose{/.prod}.yml stop [container_name]
```

Full composition logs [or logs for the container_name]
```shell
docker-compose -f .docker/docker-compose.yml logs [container_name]
```
Also worth of mentioning that "services" tab inside jetbrains ide could be a good assistant

List of nice optional flags:
```shell
--detach -- detaching console after command execution
```
Run container commands ( migrations, etc )
```shell
docker-compose -f .docker/docker-compose.yml run [container name] ..command...
```
### Database
Database `maindb`, user `dbuser` should be created automatically with "Initialization script" mechanic
[link](https://hub.docker.com/_/postgres) at the time of initial container deployment.

It might not happen with some hosts/configurations,
so you have to create db/user pair manually with tools of your preference (pgadmin/psql/etc).

Usage of the following commands assumes that the database, and the corresponding user already exists.

#### Database dump/restore
Restore `maindb` from the `dump.sql` file
```shell
docker-compose -f .docker/docker-compose.yml exec -T database pg_restore -cC --disable-triggers -U dbuser --dbname=maindb < dump.sql
```
Create full dump for restoring database from scratch
```shell
docker-compose -f .docker/docker-compose.yml exec -T database pg_dump -Fc -cC --disable-triggers -U dbuser --dbname=maindb > dump.sql
```

#### Data only commands
Create `data.sql` dump with data inserts only
```shell
docker-compose -f .docker/docker-compose.yml exec database pg_dump --user dbuser --column-inserts --data-only maindb > data.sql
```
Apply `data.sql` dump on existing database.
We assume that schemas of source and target should be identical.
```shell
cat data.sql | docker-compose -f .docker/docker-compose.yml exec -T database psql -U dbuser --dbname=maindb
```

Feel free to message us if something is unclear for you.
