# Админка-Django ⭐

Данный проект содержит административную панель для управления контентом онлайн-кинотеатра. Система позволяет добавлять, редактировать и удалять кинопроизведения, управлять авторами, жанрами и другими связанными данными.

### Возможности ✨

- Управление каталогом фильмов: создание, редактирование и удаление информации о фильмах. 
- Управление жанрами: добавление новых жанров и привязка их к фильмам. 
- Управление авторами (режиссёрами, сценаристами, актёрами): добавление информации об авторах и их участие в фильмах. 
- Поиск и фильтрация данных для удобного администрирования. 
- Интуитивно понятный интерфейс, основанный на Django Admin.

### Стек используемых технологий 🏗️

Проект построен с использованием:
- Python
- PostgreSQL
- Django
- Docker
- Elasticsearch
- Redis
- Nginx

### Запуск 🍾

Необходимо завести файлик переменных окружения `.env` со следующими переменными:
```
DEBUG=True
SECRET_KEY=<ваш ключ>

ENGINE=django.db.backends.postgresql
POSTGRES_USER=<пользователь>
POSTGRES_PASSWORD=<пароль>
POSTGRES_DBNAME=<база>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_OPTIONS=-c search_path=public,content

# данные суперпользователя для входа в админку
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@test.com
DJANGO_SUPERUSER_PASSWORD=1234

REDIS_HOST=redis
REDIS_PORT=6379

ELASTIC_HOST=elasticsearch
ELASTIC_PORT=9200
```

Клонируем проект в рабочую директорию
```bash
git clone https://github.com/taaylor/admin_panel.git
```

Для старта **админки** достаточно иметь на своей махине [Docker](https://www.docker.com/)
```bash
docker-compose up --build
```

С перечнем модулей можно ознакомиться в файлике `requirements.txt`
