For building composition please run
```bash
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
Also worth of mentioning that "services" tab inside jetbrains ide could be a good assistant

Feel free to message us if something is unclear for you.
