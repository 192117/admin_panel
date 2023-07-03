# Интерфейс администратора

Представлен интерфейс на основе стандартных средств Django, который позволит создавать и редактировать записи в базе 
данных.

- Описание API в [openapi-файле](https://github.com/192117/admin_panel/blob/master/movies_admin/example_openapi.yaml)💾
- Коллекция тестов в [Postman](https://github.com/192117/admin_panel/blob/master/movies_admin/example_api_postman_collection.json)💾

## API:

- [Список фильмов с пагинацией](https://127.0.0.1:8000/api/v1/movies/)
- [Информация по фильму](https://127.0.0.1:8000/api/v1/movies/<uuid:pk>/)