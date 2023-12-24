# Бот для кафе
## Описание
Бот позволяет резервировать столы и сеты на определенные дни в кафе.

## Технологии
- Python 3.11
- Django 4.2.7
- Django REST Framework 3.14.0
- Aiogram 3.1.1
- PostgreSQL 13.0
- Nginx 1.21.3
- Docker
- Docker-compose
- Docker Hub
- SunriseSunset.io API

# Установка
## Копирование репозитория
Клонируем репозиторий и переходим в директорию infra:
```
~ git clone git@github.com:Studio-Yandex-Practicum-Hackathons/cafe_azu_bot_2.git
~ cd ./cafe_azu_bot_2/infra/
```
Требуется изменить server_name и listen в ./infra/nginx/default.conf, ports в docker-compose.yml

## Подготовка боевого сервера:
1. Перейдите на боевой сервер:
```
ssh username@server_address
```
2. Обновите индекс пакетов APT:
```
sudo apt update
```
и обновите установленные в системе пакеты и установите обновления безопасности:
```
sudo apt upgrade -y
```
Создайте папку `nginx`:
```
mkdir nginx
``` 
Скопируйте файлы docker-compose.yaml, nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml, home/<ваш_username>/nginx/default.conf соответственно:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
Установите Docker и Docker-compose:
```
sudo apt install docker.io
```
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```
Проверьте правильность установки Docker-compose:
```
sudo  docker-compose --version
```
На боевом сервере создайте файл .env:
```
touch .env
```
и заполните переменные окружения
```
nano .env
- TOKEN = <Токен бота, можно получить у BotFather>
- ADMIN_ID = <ID телеграмм-аккаунта админа>
- PROVIDER_TOKEN = <Токен платежной системы>
- SECRET_KEY=<SECRET_KEY>


- POSTGRES_DB = postgres
- POSTGRES_USER = postgres
- POSTGRES_PASSWORD = postgres
- POSTGRES_HOST = db
- POSTGRES_PORT = 5432

- WEB_HOST = <ip сервера>
- WEB_PORT = <Порт сервера>
- WEB_PROTOKOL = <Протокол сервера>
```

## Развертывание проекта с помощью Docker:
Разворачиваем контейнеры в фоновом режиме из папки infra:
```
sudo docker compose up -d
```
При первом запуске выполняем миграции:
```
sudo docker compose exec backend python manage.py migrate
```
И собираем статику:
```
sudo docker compose exec backend python manage.py collectstatic --no-input
```
Создаем суперпользователя:
```
sudo docker compose exec backend python manage.py createsuperuser
```
Загружаем данные из csv-таблиц в базу данных:
```
sudo docker compose exec backend python manage.py load_data 
```

# Адресные пути
- [Документация к API базе данных](http://127.0.0.1:8000/redoc)
- [Админ-панель базы данных](http://127.0.0.1:8000/admin)
# Авторы
[Людмила Давлетова](https://github.com/luydmila-davletova),
[Владимир Захаров](https://github.com/zakharovvladimir),
[Мадина Муминова](https://github.com/madina-zvezda),
[Дмитрий Коломейцев](https://github.com/Certelen),
[Константин Гашев](https://github.com/Gashev1989)
