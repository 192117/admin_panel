# Сервис Admin Panel (сервиса для управления контентом).

_Основа онлайн-кинотеатра — это его фильмы. Поэтому в этой части представлены сервисы, которые позволяют загрузить фильмы
на сервер и получить их._

В [schema_design](https://github.com/192117/admin_panel/tree/master/schema_design) представлена схема для реляционного
хранилища для фильмов PostgreSQL. С помощью которой можно создать базу данных.

В [movies_admin](https://github.com/192117/admin_panel/tree/master/movies_admin) представлен интерфейс администратора 
на основе Django. После этого этапа работа коллекция фильмов может уже пополняться, пока происходит доработка остальных 
частей онлайн-кинотеатра. Но и этот процесс можно ускорить, если взять уже заполненную базу данных и перелив содержимое
в БД нашего сервиса. 

В [sqlite_to_postgres](https://github.com/192117/admin_panel/tree/master/sqlite_to_postgres) представлен скрипт для 
заполения хранилища фильмами (перенос из готовой базы SQLite в нашу БД PostgreSQL). 

В [postgres_to_es](https://github.com/192117/admin_panel/tree/master/postgres_to_es) реализован ETL 
(Extract-Transform-Load) процесс для загрузки данных о фильмах и связанных с ними людях, данных о жанрах и данных о 
людях, принимающих участие в создании фильмов, в поисковый движок Elasticsearch.

## Стек:

- Django
- Elasticsearch

## Styleguide:

- isort
- flake8
- flake8-blind-except
- flake8-bugbear
- flake8-builtins
- flake8-class-attributes-order
- flake8-cognitive-complexity
- flake8-commas
- flake8-comprehensions
- flake8-debugger
- flake8-functions
- flake8-isort
- flake8-mutable
- flake8-print
- flake8-pytest
- flake8-pytest-style
- flake8-quotes
- flake8-string-format
- flake8-variables-names

## Пакетный менеджер:

- Poetry

## Установка

Перед началом установки убедитесь, что у вас установлен Python 3.11 и Poetry (пакетный менеджер для Python).

1. Склонируйте репозиторий:

`git clone https://github.com/192117/admin_panel.git`

2. Перейдите в директорию:

`cd admin_panel`

## Запуск приложения c использованием Docker Compose (после пункта "Установка")

1. Создайте переменные окружения:

_Создайте файл .env.docker (в movies_admin/config) на основе .env.example для запуска с Docker. Файл содержит 
переменные окружения, которые требуются для настройки приложения._

2. Запустите сборку docker-compose:

`docker compose up -d --build`

3. Доступ к приложению: 

[Django Admin](http://127.0.0.1:8000/admin)

[Elasticsearch](http://127.0.0.1:9203)  (открыт для того, чтобы можно было покапаться через бразуер) # не для production
