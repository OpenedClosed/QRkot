# Приложение QRKot

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

### Технологии
* Python 3.8.8
* FastApi 0.78.0

### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd app
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Применить миграции создав новую БД либо можно воспользоваться тестовой:

```
alembic upgrade head
```

Запуск проекта:

```
uvicorn app.main:app --reload
```
