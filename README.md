![project status baidge](https://github.com/aenika/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# проект Foodgram
Данный проект создан для создания рецептов. Авторизированные пользователи могут писать рецепты, а также подписываться на других авторов, добавлять рецепты в избранное и на основе выбранных рецептов создавать список покупок, состоящий из ингредиентов, необходимых для выбранных рецептов.

## Адрес проекта на сервере:
http://158.160.99.0

## Шаблон наполнения env-файла

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=...
POSTGRES_PASSWORD=...
DB_HOST=db
DB_PORT=...
SECRET_KEY=...
DEBUG=False
 

## Запуск приложения в конейнерах:

Для корректной работы проекта необходимо (все команды начинать с "sudo", если Вы работаете на Ubuntu):

* Выполните нижеследующую команду:
```
sudo docker-compose up
```
* Выполните миграции
```
docker-compose exec web python manage.py migrate
```
* Создайте суперпользователя
```
docker-compose exec web python manage.py createsuperuser
```
* Подгрузите статику для проекта:
```
docker-compose exec web python manage.py collectstatic --no-input
```
* Заполните разддел ингредиенты для проекта:
```
docker-compose exec web python manage.py fill_sql
```
* Готово! 


## Автор проекта 

https://github.com/Aenika