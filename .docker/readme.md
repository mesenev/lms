For building composition please run
```shell
docker-compose -f .docker/docker-compose.yml build
```
For launching built composition please run
```
docker-compose -f .docker/docker-compose.yml up
```
For executing a command inside specific container please run
```
docker-compose -f .docker/docker-compose.dev.yml exec backend python manage.py shell
```
For getting inside the database shell please run
```
docker-compose -f .docker/docker-compose.yml exec database psql -U dbuser
```
For stopping the composition gracefully please run
```
docker-compose -f .docker/docker-compose.yml stop
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
