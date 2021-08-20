Building composition {dev/prod}
```shell
docker-compose -f .docker/docker-compose{/.prod}.yml build
```
Launching built composition
```
docker-compose -f .docker/docker-compose{/.prod}.yml up
```
Executing a command inside specific container
```
docker-compose -f .docker/docker-compose{/.prod}.yml exec backend python manage.py shell
```
Getting inside the database shell
```
docker-compose -f .docker/docker-compose{/.prod}.yml exec database psql -U dbuser
```
Gracefully stop composition [or container_name]
```
docker-compose -f .docker/docker-compose{/.prod}.yml stop [container_name]
```

Full composition logs or logs for the container, if specified
```shell
docker-compose -f .docker/docker-compose.yml logs [container_name]
```
Also worth of mentioning that "services" tab inside jetbrains ide could be a good assistant

List of nice optional flags:
```
--detach -- detaching console after command execution
```


Feel free to message us if something is unclear for you.
