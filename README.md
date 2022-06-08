
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
docker-compose -f \.docker\docker-compose.yml up -d database
```
9)В консоль вводим
```shell
docker-compose -f \.docker\docker-compose.yml up -d backend
```
10)В консоль вводим
```shell
docker-compose -f \.docker\docker-compose.yml run /bin/bash
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



