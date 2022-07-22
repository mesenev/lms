
###Win
1)Установить PyChram Proffesional + Docker

2)Установить ядра под докер ( если попросит )

3)Склонировать проект в удобную папку

4)Открыть папку через PyCharm

5)Создать фаил под именование Setting.py в папке imcslms

6)В фаил добавить строчку '''from imcslms.default_settings import *'''

7)Создать базу данных maindb в окне Pycharm Database (окно находится по тсандарту справа сверху рядом с кнопкной сверунть карту )

8)Накатить плагины которые предложии Pycharm. Данные для создание бд
```shell
Name – maindb@localhost
User – dbuser
Passowrd – dbpassword
Database -- maindb
```
9)В консоль вводим
```shell
docker-compose -f \.docker\docker-compose.yml up -d database
```
10)В консоль вводим
```shell
docker-compose -f \.docker\docker-compose.yml up -d backend
```
11)В консоль вводим
```shell
docker-compose -f \.docker\docker-compose.yml run /bin/bash
```
(если не запускается то нужно запустить его ручками в приложении docker, после войти в контейнер и выполнить все команды описаные ниже, вход осуществляется через команду docker exec -it ваш_контейнер bash
)
Так же можно попробовать запустить контейнер ручками ( команда docker-compose -f .\.docker\docker-compose.yml run backend /bin/bash ) Если на данном шаге что то не получается, значит где то накосячили до этого .
12)Внутри контейнера вводим :
```shell
python manage.py migrate
python manage.py createsuperuser ( admin , admin)
python manage.py registergroups
```
13) В папке frontend вводим в консоли :
```shell
Npm i
Npm run serve
```


###Linux
Примечание : Все команды описанные ниже используются сразу под админ-правами ( sudo ), что бы в дальнейшем докер мог нормально работать нужно посмотреть гайд как запускать докер non-root . https://docs.docker.com/engine/security/rootless/ ссылка на документацию
1)Установить PyChram Proffesional + Docker
2)Склонировать проект в удобную папку
3)Открыть папку через PyCharm
4)Создать фаил под именование Setting.py в папке imcslms
5)В фаил добавить строчку
'''shell
from imcslms.default_settings import *
'''
6)Создать базу данных maindb в окне Pycharm Database (окно находится по сандарту справа сверху рядом с кнопкной сверунть)
7)Накатить плагины которые предложии Pycharm
Параметры для бд
Name – maindb
User – dbuser
Passowrd – dbpassword
Database -- maindb

8)В консоль вводим
```shell
docker-compose -f .docker/docker-compose.yml up -d database
```
9)В консоль вводим
```shell
docker-compose -f .docker/docker-compose.yml up -d backend
```
10)В консоль вводим
```shell
docker-compose -f .docker/docker-compose.yml run /bin/bash
```
11)Внутри контейнера вводим :
```shell
python manage.py migrate
python manage.py createsuperuser ( admin , admin)
python manage.py registergroups
```
12) В папке frontend вводим в консоли :
```shell
Npm i
Npm run serve
```


###EngVer

1)Install PyChram Proffesional + Docker

2)Install kernels under docker (If system need it)

3)Clone a project to a folder

4)Open Project in PyCharm

5)Create a file for naming Setting.py in the imcslms folder

6)Add ```from imcslms.default_settings import *```to the file

7)Create maindb in the Pycharm Database window (the window is located on the top right side next to the collapse map button)

8)Install plugins that Pycharm offers. Source to create a DB
```
Name – maindb@localhost
User – dbuser
Passowrd – dbpassword
Database -- maindb
```
9)In the shell
```shell
docker-compose -f \.docker\docker-compose.yml up -d database
```
10)In the shell
```shell
docker-compose -f \.docker\docker-compose.yml up -d backend
```
11)In the shell|
```shell
docker-compose -f \.docker\docker-compose.yml run /bin/bash
```
>if it does not start then you need to run it with handles in the docker application, after entering the container and executing all the commands described below, the login is done through the command docker exec -it your_container bash) You can also try to run the container with handles (command docker-compose -f.\.docker\docker-compose.yml run backend /bin/bash) If something does not work at this step, then somewhere they screwed up before that.

12)In the docker conteiner:
```shell
python manage.py migrate
python manage.py createsuperuser ( admin , admin)
python manage.py registergroups
```
13) In the folder of  frontend shell it :
```shell
Npm i
Npm run serve
```


###Linux
> Note: All the commands described below are used immediately under the admin rights (sudo), so that in the future the docker could work normally you need to see the guide how to run the non-root docker. https://docs.docker.com/engine/security/rootless/ a link to the documentation

1)Install PyChram Proffesional + Docker

2)Clone folder

3)Open project into PyChram Prof

4)Create a file for naming Setting.py in the imcslms folder

5)Add a line to the file

```shell
from imcslms.default_settings import *
```

6)Create maindb in the Pycharm Database window (the window is located on the top right side next to the collapse map button)

7)Install all plugins that  Pycharm is needed

DB settings
```
Name – maindb
User – dbuser
Passowrd – dbpassword
Database -- maindb
```

8)In the Terminal
```shell
docker-compose -f .docker/docker-compose.yml up -d database
```
9)In the Terminal
```shell
docker-compose -f .docker/docker-compose.yml up -d backend
```
10)In the Terminal
```shell
docker-compose -f .docker/docker-compose.yml run /bin/bash
```
11)In the docker container:
```shell
python manage.py migrate
python manage.py createsuperuser ( admin , admin)
python manage.py registergroups
```
12) In the folder frontend , input it In the Terminal :
```shell
Npm i
Npm run serve


